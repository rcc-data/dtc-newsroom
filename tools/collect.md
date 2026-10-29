# Wire collectors (built-in browser)

Each snippet runs with the Claude Browser `javascript_tool` on the named origin (navigate there first) and returns text that starts with `@@SRC:<CODE>` followed by `date|title|url[|extra]` lines. Save the returned text as `tools/inbox/<CODE>.txt` (a large result is spilled to a tool-results file: copy the `text` value from it), then run `python3 tools/wire_inventory.py --clear-inbox`. Set `SINCE` to the newest date already in `data/wire_articles.csv` for that publisher (the merge de-duplicates by URL, so overlap is harmless).

Long loops: keep the tab fronted (`tabs_select`), or timers throttle. If a call times out, the script keeps running in the page; poll a `window._x` variable instead of re-running.

## NBNL: Northbeam newsletter, https://themediabuyer.northbeam.io/archive
```js
const out=[];for(let p=1;p<=3;p++){const d=new DOMParser().parseFromString(await (await fetch('/archive?page='+p)).text(),'text/html');const seen=new Set(out.map(o=>o[2]));let n=0;d.querySelectorAll('a[href*="/p/"]').forEach(a=>{const u=a.href.split('?')[0];if(seen.has(u))return;const m=a.innerText.match(/([A-Z][a-z]{2}) (\d{1,2}), (\d{4})/);const t=((a.querySelector('h2,h3')||a).textContent).trim().replace(/\s+/g,' ');seen.add(u);n++;out.push([m?m[0]:'',t,u])});if(!n)break}'@@SRC:NBNL\n'+out.map(o=>o.join('|')).join('\n')
```

## NBBLOG: Northbeam blog, https://www.northbeam.io/blog
Cards carry "Month D, YYYY / TYPE / Title"; the featured whitepaper sits above the grid. Parse `a[href*="/blog/"]`, walk up to the element whose text has the date, and follow `a[href*="_page="]` pagination links.

## CTC: Common Thread Collective, https://commonthreadco.com
Shopify blogs: coachs-corner, ecommerce-playbook, outliers, tactics, sharpen-your-skills, million-dollar-challenge, taylor-reacts, dtc-hotline, thread, upgrade-your-culture, research, bridges, bridges-live. Fetch `/blogs/<blog>?page=N` **2.5 s apart** (fast fetches trigger a Cloudflare check; if the page title is "Just a moment…", stop and skip CTC today, never try to get around it). Each card has `time[datetime]` and `a.article__heading-link`. Stop a blog when half a page is older than SINCE. The `.atom` feeds ignore `?page`.

## FOX: Foxwell, https://www.foxwelldigital.com/blog
```js
let items=[],url='/blog?format=json';for(let i=0;i<5&&url;i++){const j=await (await fetch(url)).json();items.push(...(j.items||[]));const l=j.items&&j.items[j.items.length-1];if(!l||new Date(l.publishOn)<new Date(SINCE))break;url=j.pagination&&j.pagination.nextPage?j.pagination.nextPageUrl+'&format=json':null}
'@@SRC:FOX\n'+items.filter(x=>new Date(x.publishOn)>=new Date(SINCE)).map(x=>new Date(x.publishOn).toISOString().slice(0,10)+'|'+x.title.replace(/\|/g,'/')+'|https://www.foxwelldigital.com'+x.fullUrl).join('\n')
```

## HAUS: Haus, https://www.haus.io/blog
The listing HTML holds every card: `[fs-cmssort-field="date"]` next to `a[href^="/blog/"] h3`. Undated `/resources/` pages are skipped.

## TW: Triple Whale, https://www.triplewhale.com/blog
No dates on the listing. Take `/sitemap.xml` `<url>` entries under `/blog/` with `lastmod` ≥ SINCE, fetch each (8 at a time) and read `meta[property="article:published_time"]` and the `h1`.

## MR: Modern Retail and 2PM (WordPress REST)
```js
// on https://www.modernretail.co (code MR; drop posts in Sponsored/Awards/Partner categories; extra = category names)
// on https://2pml.com (code 2PM)
const all=[];for(let p=1;p<=10;p++){const r=await fetch(`/wp-json/wp/v2/posts?after=${SINCE}T00:00:00&per_page=100&page=${p}&_fields=date,link,title,categories`);if(!r.ok)break;const j=await r.json();if(!j.length)break;all.push(...j)}
```
For Modern Retail, strip `https://www.modernretail.co/` from the link (the merge script adds it back).

## Not collected
- Runneth (Motion) blog: pages carry no publish date. New Motion reports go in via the library.
- X posts and Meta earnings: added through `library.py` entries, which the merge picks up automatically.
