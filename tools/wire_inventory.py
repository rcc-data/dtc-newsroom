"""Merge article listings into data/wire_articles.csv (the Wire inventory).

Inputs (all optional, run from the repo root):
  tools/inbox/<SRC>.txt  first line "@@SRC:<SRC>", then one article per line:
                         date|title|url[|extra]   date as YYYY-MM-DD, "Oct 22, 2026" or "October 22, 2026"
  library.py LIB         every 2026+ library entry is added (so X posts, earnings and reports are listed)
  data/wire_headlines.csv

Existing rows in data/wire_articles.csv are kept; new rows are added by normalised URL.
Inbox files are left in place (re-running is idempotent). Usage: python3 tools/wire_inventory.py [--clear-inbox]
"""
import csv, glob, html, os, re, sys
from datetime import datetime

sys.path.insert(0, '.')
from library import LIB

OUT = 'data/wire_articles.csv'
SINCE = '2026-01-01'
HEADER = ['date', 'pub', 'title', 'url', 'type', 'topics']
NOTE = ('# Wire inventory: every article, newsletter issue, report, podcast and post from the tracked sources since 1 Jan 2026. '
        'Built by tools/wire_inventory.py from tools/inbox listings, the library and wire headlines; topics are keyword tags. '
        'Undated pages (Runneth blog) and sponsored posts are excluded.')

SRC = {  # inbox source code -> (publisher, default type)
    'NBNL': ('Northbeam', 'Newsletter'), 'NBBLOG': ('Northbeam', 'Blog'), 'NBX': ('Northbeam', 'X'),
    'CTC': ('CTC', 'Blog'), 'FOX': ('Foxwell', 'Blog'), 'HAUS': ('Haus', 'Blog'), 'TW': ('Triple Whale', 'Blog'),
    'MO': ('Motion', 'Newsletter'), 'MR': ('Modern Retail', 'News'), '2PM': ('2PM', 'Memo'), 'META': ('Meta', 'Earnings'),
    'VAROS': ('Varos', 'Report'), 'GRAPHITE': ('Graphite', 'Report'),
}

TOPICS = [
    ('Meta', r'\bmeta\b|facebook|instagram|andromeda|advantage\+|\bgem\b|reels'),
    ('TikTok', r'tiktok'), ('Google', r'google|youtube|pmax|performance max|\bdemand gen'),
    ('Amazon', r'amazon|prime day|prime big deal'), ('AppLovin', r'applovin'),
    ('AI', r'\bai\b|\baeo\b|\bgeo\b|parametric|prompt|agentic|llm|chatgpt|moby|claude|gemini|agents?\b'),
    ('Measurement', r'attribution|incremental|\bmmm\b|mix model|lift|geo|measure|view-?through|causal'),
    ('Creative', r'creative|\bugc\b|\bads? that|hook|thumbstop|video'),
    ('BFCM / Q4', r'bfcm|black friday|cyber|holiday|\bq4\b|peak season|q5'),
    ('Benchmarks', r'benchmark|data:|index|\bcpm|\broas|\bcac\b|\bcpa\b|\bcvr|\bctr\b|survey|report|year in review|h1 2026|q[1-4] 20'),
    ('Tariffs / policy', r'tariff|de minimis|\blaw\b|\bact\b|executive order|regulat|ban'),
    ('Earnings', r'earnings|results|quarter'),
    ('Retail', r'retail|store|walmart|target|wholesale|cpg'),
]


def norm(u):
    u = (u or '').strip().split('#')[0].split('?')[0].rstrip('/').lower()
    return re.sub(r'^https?://(www\.)?', '', u)


def pdate(s):
    s = s.strip()
    for f in ('%Y-%m-%d', '%b %d, %Y', '%B %d, %Y'):
        try:
            return datetime.strptime(s[:10] if f == '%Y-%m-%d' else s, f).strftime('%Y-%m-%d')
        except ValueError:
            pass
    return ''


def topics(title, extra=''):
    t = (title + ' ' + extra).lower()
    return ';'.join(k for k, rx in TOPICS if re.search(rx, t))


def mr_type(cats):
    c = cats.lower()
    if 'podcast' in c: return 'Podcast'
    return 'News'


def guess_type(pub, dflt, title, extra):
    t = title.lower()
    if pub == 'Modern Retail': return mr_type(extra)
    if pub == 'Graphite': return 'Guide' if re.search(r'^how (to|do)|playbook|guide', t) else 'Report'
    if pub == 'CTC' and extra:
        b = {'research': 'Report', 'thread': 'Newsletter', 'dtc-hotline': 'Podcast', 'taylor-reacts': 'Podcast', 'bridges-live': 'Podcast', 'outliers': 'Podcast'}.get(extra)
        if b: return b
    if pub == 'Northbeam' and dflt == 'Blog' and 'whitepaper' in extra.lower(): return 'Report'
    if re.search(r'podcast|episode|\bep\.? ?\d', t): return 'Podcast'
    if re.search(r'webinar|workshop|recap', t): return 'Event'
    if re.search(r"what'?s new in|product update|introducing|announcing|meet |launch", t): return 'Product'
    if re.search(r'survey|benchmark|report|index|whitepaper|year in review|data:', t): return 'Report'
    return dflt


def main():
    rows = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            for r in csv.DictReader(l for l in f if not l.startswith('#')):
                rows[norm(r['url'])] = r

    def add(date, pub, title, url, typ, extra=''):
        if not date or date < SINCE or not url: return
        k = norm(url)
        title = re.sub(r'\s+', ' ', html.unescape(title)).strip()
        if k in rows:
            r = rows[k]
            if not r.get('title'): r['title'] = title
            return
        rows[k] = dict(date=date, pub=pub, title=title, url=url.strip(), type=typ, topics=topics(title, extra))

    for fn in sorted(glob.glob('tools/inbox/*.txt')):
        lines = open(fn).read().splitlines()
        code = lines[0][6:].strip() if lines and lines[0].startswith('@@SRC:') else os.path.basename(fn)[:-4]
        pub, dflt = SRC.get(code, (code, 'Article'))
        for ln in lines[1:]:
            if not ln or ln.startswith('#'): continue
            p = ln.split('|')
            if len(p) < 3: continue
            d, t, u = pdate(p[0]), p[1], p[2]
            extra = p[3] if len(p) > 3 else ''
            if pub == 'Modern Retail' and not u.startswith('http'):
                u = 'https://www.modernretail.co/' + u
            if pub == 'Triple Whale' and (not t or t == 'Triple Whale blog'): continue
            add(d, pub, t, u, guess_type(pub, dflt, t, extra), extra)

    for e in LIB:
        if e.get('date', '') < SINCE or e.get('src') in ('Weekly', 'Tool', 'Monthly', 'Site'): continue
        typ = {'X': 'X', 'Newsletter': 'Newsletter', 'Blog': 'Blog', 'Report': 'Report', 'Podcast': 'Podcast',
               'Earnings': 'Earnings', 'Survey': 'Report', 'Analysis': 'News'}.get(e.get('src'), e.get('src', 'Article'))
        add(e['date'], e.get('pub', 'Northbeam'), e['title'], e['url'], typ, ' '.join(e.get('tags', [])))

    if os.path.exists('data/wire_headlines.csv'):
        with open('data/wire_headlines.csv') as f:
            for r in csv.DictReader(l for l in f if not l.startswith('#')):
                add(r['date'], r['pub'], r['title'], r['url'], 'News' if r['pub'] == 'Modern Retail' else 'Article')

    out = sorted(rows.values(), key=lambda r: (r['date'], r['pub'], r['title']), reverse=True)
    with open(OUT, 'w', newline='') as f:
        f.write(NOTE + '\n')
        w = csv.DictWriter(f, fieldnames=HEADER, extrasaction='ignore')
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(len(out), 'rows', dict(Counter(r['pub'] for r in out)))
    if '--clear-inbox' in sys.argv:
        for fn in glob.glob('tools/inbox/*.txt'): os.remove(fn)


if __name__ == '__main__':
    main()
