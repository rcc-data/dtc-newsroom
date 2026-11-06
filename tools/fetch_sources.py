"""Fetch new items from the tracked news sources without a browser (runs in GitHub Actions).

Writes tools/inbox/<CODE>.txt in the collect.md format ("@@SRC:<CODE>" then date|title|url|extra lines)
and the readable text of every new item to notes/fetched/<CODE>/<slug>.txt, so the morning cloud pass can
merge the Wire and pull figures without reaching the sites itself.
SINCE for each publisher = its newest date in data/wire_articles.csv (overlap is harmless: the merge
de-duplicates by URL). Respects robots.txt; skips a site that answers with a bot check.
Usage: python3 tools/fetch_sources.py   (needs requests + beautifulsoup4)
"""
import csv, json, os, re, sys, time, urllib.robotparser
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

UA = 'Mozilla/5.0 (compatible; DTCNewsroomBot/1.0; +https://dtcnewsroom.com/)'
S = requests.Session()
S.headers.update({'User-Agent': UA, 'Accept-Language': 'en'})
LOG = []
ROBOTS = {}
PUB = {'NBNL': 'Northbeam', 'NBBLOG': 'Northbeam', 'CTC': 'CTC', 'HAUS': 'Haus', 'TW': 'Triple Whale', 'MR': 'Modern Retail',
       '2PM': '2PM', 'GRAPHITE': 'Graphite', 'DTCNL': 'Direct to Consumer', 'HWSS': 'Curtis Howland'}


def since_for(pub, default='2026-10-01'):
    best = ''
    with open('data/wire_articles.csv') as f:
        next(f)
        for r in csv.DictReader(f):
            if r['pub'] == pub and r['date'] > best:
                best = r['date']
    d = best or default
    return (datetime.strptime(d, '%Y-%m-%d') - timedelta(days=2)).strftime('%Y-%m-%d')


def allowed(url):
    p = urlparse(url)
    base = f'{p.scheme}://{p.netloc}'
    if base not in ROBOTS:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = S.get(base + '/robots.txt', timeout=20)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except Exception:
            rp.parse([])
        ROBOTS[base] = rp
    return ROBOTS[base].can_fetch(UA, url)


def get(url, delay=0.6, as_json=False):
    if not allowed(url):
        raise RuntimeError('robots.txt disallows ' + url)
    time.sleep(delay)
    r = S.get(url, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f'HTTP {r.status_code} for {url}')
    if 'Just a moment' in r.text[:3000] and not as_json:
        raise RuntimeError('bot check at ' + url)
    return r.json() if as_json else r.text


def text_of(html):
    soup = BeautifulSoup(html, 'html.parser')
    for t in soup(['script', 'style', 'nav', 'footer', 'header', 'form', 'noscript']):
        t.decompose()
    main = soup.find('article') or soup.find('main') or soup.body or soup
    txt = re.sub(r'\n{3,}', '\n\n', main.get_text('\n', strip=True))
    return txt[:30000]


def pdate(s):
    s = (s or '').strip()
    for f in ('%Y-%m-%d', '%b %d, %Y', '%B %d, %Y', '%b. %d %Y', '%b %d %Y'):
        try:
            return datetime.strptime(s[:10] if f == '%Y-%m-%d' else s, f).strftime('%Y-%m-%d')
        except ValueError:
            pass
    return ''


def save(code, items, fetch_text=True):
    """items: list of (date, title, url, extra); writes inbox + article text for each."""
    os.makedirs('tools/inbox', exist_ok=True)
    items = [i for i in items if i[0]]
    seen, out = set(), []
    for i in items:
        if i[2] in seen:
            continue
        seen.add(i[2])
        out.append(i)
    if not out:
        LOG.append(f'{code}: nothing new')
        return
    with open(f'tools/inbox/{code}.txt', 'w') as f:
        f.write(f'@@SRC:{code}\n' + '\n'.join('|'.join([d, t.replace('|', '/'), u] + ([x] if x else [])) for d, t, u, x in out) + '\n')
    n = 0
    if fetch_text:
        os.makedirs(f'notes/fetched/{code}', exist_ok=True)
        for d, t, u, x in out:
            slug = re.sub(r'[^a-z0-9]+', '-', urlparse(u).path.lower()).strip('-')[-90:] or 'index'
            path = f'notes/fetched/{code}/{d}-{slug}.txt'
            if os.path.exists(path):
                continue
            try:
                body = x if (x and x.startswith('\n')) else text_of(get(u if u.startswith('http') else 'https://www.modernretail.co/' + u))
                with open(path, 'w') as f:
                    f.write(f'{t}\n{u}\n{d}\n\n{body.strip()}\n')
                n += 1
            except Exception as e:
                LOG.append(f'{code}: text failed for {u}: {e}')
    LOG.append(f'{code}: {len(out)} items, {n} texts saved')


def run(code, fn):
    try:
        fn(since_for(PUB[code]))
    except Exception as e:
        LOG.append(f'{code}: SKIPPED ({e})')


DATE_RE = re.compile(r'([A-Z][a-z]{2,8}\.? \d{1,2},? \d{4})')


def nbnl(since):
    soup = BeautifulSoup(get('https://themediabuyer.northbeam.io/archive'), 'html.parser')
    items = []
    for a in soup.select('a[href*="/p/"]'):
        m = DATE_RE.search(a.get_text(' '))
        h = a.find(['h2', 'h3'])
        d = pdate(m.group(1).replace(',', ', ').replace(',  ', ', ')) if m else ''
        if d >= since:
            items.append((d, (h or a).get_text(' ', strip=True), urljoin('https://themediabuyer.northbeam.io', a['href'].split('?')[0]), ''))
    save('NBNL', items)


def nbblog(since):
    soup = BeautifulSoup(get('https://www.northbeam.io/blog'), 'html.parser')
    items = []
    for a in soup.select('a[href*="/blog/"]'):
        el, d = a, ''
        for _ in range(6):
            m = DATE_RE.search(el.get_text(' ')) if el else None
            if m:
                d = pdate(m.group(1))
                break
            el = el.parent
        title = a.get_text(' ', strip=True)
        title = re.sub(r'^.*?\b(BLOG|WHITEPAPER|REPORT|GUIDE|NEWS)\b\s*', '', title)[:160]
        if d >= since and title:
            items.append((d, title, urljoin('https://www.northbeam.io', a['href'].split('?')[0]), ''))
    save('NBBLOG', items)


def ctc(since):
    items = []
    for blog in ['coachs-corner', 'ecommerce-playbook', 'outliers', 'tactics', 'research', 'thread', 'dtc-hotline', 'taylor-reacts', 'bridges-live']:
        soup = BeautifulSoup(get(f'https://commonthreadco.com/blogs/{blog}', delay=2.6), 'html.parser')
        for a in soup.select('a.article__heading-link'):
            el, d = a, ''
            for _ in range(6):
                t = el.find('time', attrs={'datetime': True}) if el else None
                if t:
                    d = t['datetime'][:10]
                    break
                el = el.parent
            if d >= since:
                items.append((d, a.get_text(' ', strip=True), urljoin('https://commonthreadco.com', a['href']), blog))
    # listing titles are truncated: take the h1 from each article page while saving its text
    full = []
    for d, t, u, b in items:
        try:
            h = BeautifulSoup(get(u, delay=2.6), 'html.parser').find('h1')
            full.append((d, h.get_text(' ', strip=True) if h else t, u, b))
        except Exception:
            full.append((d, t, u, b))
    save('CTC', full)


def haus(since):
    soup = BeautifulSoup(get('https://www.haus.io/blog'), 'html.parser')
    items = []
    for el in soup.select('[fs-cmssort-field="date"]'):
        d = pdate(el.get_text(strip=True))
        p = el
        for _ in range(6):
            p = p.parent
            a = p.select_one('a[href^="/blog/"]') if p else None
            if a:
                h = a.find('h3') or p.find('h3')
                if d >= since:
                    items.append((d, (h or a).get_text(' ', strip=True), urljoin('https://www.haus.io', a['href']), ''))
                break
    save('HAUS', items)


def tw(since):
    x = BeautifulSoup(get('https://www.triplewhale.com/sitemap.xml'), 'xml')
    items = []
    for u in x.find_all('url'):
        loc, lm = u.find('loc').text, (u.find('lastmod').text if u.find('lastmod') else '')
        if '/blog/' in loc and lm[:10] >= since:
            soup = BeautifulSoup(get(loc), 'html.parser')
            m = soup.find('meta', attrs={'property': 'article:published_time'})
            d = m['content'][:10] if m else ''
            h = soup.find('h1')
            if d >= since:
                items.append((d, h.get_text(' ', strip=True) if h else loc, loc, ''))
    save('TW', items)


def wp(code, base, since, drop=()):
    items, cats = [], {}
    for page in range(1, 6):
        r = S.get(f'{base}/wp-json/wp/v2/posts', params={'after': since + 'T00:00:00', 'per_page': 100, 'page': page,
                  '_fields': 'date,link,title,categories'}, timeout=30)
        if r.status_code != 200:
            break
        j = r.json()
        if not j:
            break
        for p in j:
            for c in p['categories']:
                if c not in cats:
                    try:
                        cats[c] = S.get(f'{base}/wp-json/wp/v2/categories/{c}', timeout=20).json().get('name', '')
                    except Exception:
                        cats[c] = ''
            cn = ';'.join(cats[c] for c in p['categories'])
            if any(x in cn for x in drop):
                continue
            title = BeautifulSoup(p['title']['rendered'], 'html.parser').get_text()
            items.append((p['date'][:10], title, p['link'], cn))
        time.sleep(0.6)
    save(code, items, fetch_text=(code != 'MR'))


def graphite(since):
    x = BeautifulSoup(get('https://graphite.io/sitemap.xml'), 'xml')
    known = open('data/wire_articles.csv').read()
    items = []
    for loc in [l.text for l in x.find_all('loc') if re.search(r'/research/[^/]+$', l.text)]:
        if loc.split('graphite.io')[-1] in known or 'state-of-chatgpt-ads-report' in loc:
            continue
        html = get(loc)
        m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
        h = BeautifulSoup(html, 'html.parser').find('h1')
        d = m.group(1)[:10] if m else ''
        if d >= since:
            items.append((d, h.get_text(' ', strip=True) if h else loc, loc, 'research'))
    save('GRAPHITE', items)


def dtcnl(since):
    soup = BeautifulSoup(get('https://www.directtoconsumer.co/newsletters'), 'html.parser')
    items = []
    for a in soup.select('a[href*="/newsletter/"]'):
        el, d = a, ''
        for _ in range(5):
            m = DATE_RE.search(el.get_text(' ')) if el else None
            if m:
                d = pdate(m.group(1))
                break
            el = el.parent
        if d < since:
            continue
        u = urljoin('https://www.directtoconsumer.co', a['href'])
        page = BeautifulSoup(get(u), 'html.parser')
        title = re.sub(r'\s*[-–|]\s*DTC Newsletter.*$', '', page.title.get_text() if page.title else '')
        title = re.sub(r'^[^\w]+\s*-\s*', '', title).strip()
        body = '\n---\n'.join(e.get_text('\n', strip=True) for e in page.select('.newsletter_section.w-dyn-item .w-richtext'))
        items.append((d, title, u, 'newsletter', body))
    out = [(d, t, u, x) for d, t, u, x, b in items]
    save('DTCNL', out, fetch_text=False)
    os.makedirs('notes/fetched/DTCNL', exist_ok=True)
    for d, t, u, x, b in items:
        with open(f"notes/fetched/DTCNL/{d}-{u.rstrip('/').split('/')[-1]}.txt", 'w') as f:
            f.write(f'{t}\n{u}\n{d}\n\n{b}\n')


def hwss(since):
    j = get('https://newsletter.curtishowland.com/api/v1/archive?sort=new&limit=20', as_json=True)
    # Substack sometimes wraps the archive in an object ({"posts": [...]}) instead of a bare list.
    if isinstance(j, dict):
        j = j.get('posts') or j.get('items') or j.get('data') or []
    items = []
    os.makedirs('notes/fetched/HWSS', exist_ok=True)
    for p in j:
        if not isinstance(p, dict) or not p.get('post_date') or not p.get('slug'):
            continue
        d = p['post_date'][:10]
        if d < since:
            continue
        u = p.get('canonical_url') or f"https://newsletter.curtishowland.com/p/{p['slug']}"
        items.append((d, p['title'], u, 'newsletter'))
        try:
            full = get(f"https://newsletter.curtishowland.com/api/v1/posts/{p['slug']}", as_json=True)
            body = text_of(full.get('body_html') or '')
            with open(f"notes/fetched/HWSS/{d}-{p['slug']}.txt", 'w') as f:
                f.write(f"{p['title']}\n{u}\n{d}\n{p.get('subtitle') or ''}\n\n{body}\n")
        except Exception as e:
            LOG.append(f'HWSS: text failed for {u}: {e}')
    save('HWSS', items, fetch_text=False)


RUNNETH_CATS = ['apparel', 'sports-fitness', 'retail', 'accessories']


def runneth_brands(html):
    """Ranked brand names from a Runneth trending page (Next.js payload; quotes may be escaped)."""
    names = re.findall(r'\\?"brandName\\?"\s*:\s*\\?"((?:[^"\\]|\\.)*?)\\?"', html)
    out = []
    for n in names:
        n = n.replace('\\u0026', '&').replace('\\', '').strip()
        if n:
            out.append(n)
    return out[:30]


def runneth_watch():
    """Daily check of Runneth's four Weekly Trending lists. Flags the day they change (Ryan, 6 Nov 2026).
    Baseline = the newest week captured in data/runneth_trending_ads.csv, then the last state seen here."""
    os.makedirs('notes/fetched/RUNNETH', exist_ok=True)
    sp = 'notes/fetched/RUNNETH/state.json'
    state = json.load(open(sp)) if os.path.exists(sp) else {}
    if not state:  # seed from the last Monday capture
        cap = {}
        with open('data/runneth_trending_ads.csv') as f:
            rows = [r for r in csv.DictReader(l for l in f if not l.startswith('#'))]
        wk = max(r['week'] for r in rows)
        for r in sorted((r for r in rows if r['week'] == wk), key=lambda r: int(r['rank'])):
            cap.setdefault(r['category'], []).append(r['brand'])
        state = {c: {'brands': b[:30], 'since': wk, 'source': 'capture ' + wk} for c, b in cap.items()}
    today = datetime.utcnow().strftime('%Y-%m-%d')
    changed, unchanged, failed = [], [], []
    for c in RUNNETH_CATS:
        html, err = None, None
        for base in ('https://runneth.com', 'https://motionapp.com'):
            try:
                html = get(f'{base}/trending/{c}/', delay=1.0)
                break
            except Exception as e:
                err = e
        brands = runneth_brands(html) if html else []
        if len(brands) < 10:
            failed.append(f'{c} ({err or "could not read the ranked list"})')
            continue
        old = state.get(c, {}).get('brands', [])
        moved = sum(1 for i, b in enumerate(brands[:30]) if i >= len(old) or old[i] != b)
        new_brands = len(set(brands[:30]) - set(old[:30])) if old else 30
        if old and new_brands < 5 and moved < 15:
            # Same list with a few ranks swapped: a reshuffle, not Runneth's weekly turnover
            unchanged.append(c)
            if moved:
                LOG.append(f'RUNNETH: {c} reshuffled ({moved} ranks moved, {new_brands} new brands), not a weekly update')
        else:
            changed.append((c, new_brands, brands[:3]))
            state[c] = {'brands': brands, 'since': today, 'source': 'watch'}
    json.dump(state, open(sp, 'w'), ensure_ascii=False, indent=1)
    lines = []
    if changed:
        lines.append('RUNNETH: UPDATED ' + '; '.join(f'{c} ({m} of 30 brands new, new top 3: {", ".join(t)})' for c, m, t in changed))
    if unchanged:
        lines.append('RUNNETH: unchanged ' + ', '.join(f'{c} (same since {state[c]["since"]})' for c in unchanged))
    if failed:
        lines.append('RUNNETH: could not check ' + ', '.join(failed) + '; the laptop pass checks it in the browser')
    LOG.extend(lines)
    hp = 'notes/fetched/RUNNETH/history.csv'
    new = not os.path.exists(hp)
    with open(hp, 'a') as f:
        if new:
            f.write('date,category,status,detail\n')
        for c, m, t in changed:
            f.write(f'{today},{c},updated,"{m} of 30 brands new; top 3 {" / ".join(t)}"\n')
        for c in unchanged:
            f.write(f'{today},{c},unchanged,since {state[c]["since"]}\n')
        for c in failed:
            f.write(f'{today},{c.split(" ")[0]},failed,\n')


def tw_capture():
    """Triple Whale benchmarks straight from GitHub's servers (added 6 Nov 2026). Runs only once the laptop pass
    has written tools/tw_api.json: {"url_template": "...{industry}...{band}...{start}...{end}...",
    "industries": [...], "bands": [...]}. Saves the raw JSON for the morning pass to turn into CSV rows.
    Mondays and Thursdays only, trailing 30 days ending today (never past windows)."""
    cfg_p = 'tools/tw_api.json'
    if not os.path.exists(cfg_p):
        LOG.append('TWAPI: waiting for tools/tw_api.json from the laptop pass')
        return
    if datetime.utcnow().weekday() not in (0, 3):
        return
    cfg = json.load(open(cfg_p))
    end = datetime.utcnow().strftime('%Y-%m-%d')
    start = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
    out = f'notes/fetched/TW-API/{end}'
    os.makedirs(out, exist_ok=True)
    ok = bad = 0
    for ind in cfg.get('industries', []):
        for band in cfg.get('bands', ['1m-10m']):
            url = cfg['url_template'].format(industry=ind, band=band, start=start, end=end)
            try:
                j = get(url, delay=1.0, as_json=True)
                json.dump(j, open(f'{out}/{ind}__{band}.json', 'w'))
                ok += 1
            except Exception as e:
                bad += 1
                LOG.append(f'TWAPI: {ind} {band} failed: {e}')
    LOG.append(f'TWAPI: {ok} cohorts saved for {start} to {end}' + (f', {bad} failed' if bad else ''))


if __name__ == '__main__':
    run('NBNL', nbnl)
    run('NBBLOG', nbblog)
    run('CTC', ctc)
    run('HAUS', haus)
    run('TW', tw)
    run('MR', lambda s: wp('MR', 'https://www.modernretail.co', s, drop=('Sponsored', 'Awards', 'Partner')))
    run('2PM', lambda s: wp('2PM', 'https://2pml.com', s))
    run('GRAPHITE', graphite)
    run('DTCNL', dtcnl)
    run('HWSS', hwss)
    try:
        tw_capture()
    except Exception as e:
        LOG.append(f'TWAPI: SKIPPED ({e})')
    try:
        runneth_watch()
    except Exception as e:
        LOG.append(f'RUNNETH: SKIPPED ({e})')
    os.makedirs('notes/fetched', exist_ok=True)
    with open('notes/fetched/LAST_RUN.txt', 'w') as f:
        f.write(datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC') + '\n' + '\n'.join(LOG) + '\n')
    print('\n'.join(LOG))
