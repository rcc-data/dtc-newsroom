# DTC Newsroom — update runbook

This file is the procedure scheduled runs follow. The page is built from `template.html` + `data/*.csv` + `library.py` by `python3 build.py`, which writes `dtc-newsroom.html` (published to the artifact) and `index.html` (the GitHub Pages site, https://dtcnewsroom.com/). Always commit both.

- Live page (claude.ai Artifact): https://claude.ai/artifact/YJdE49u9nVWATDWNyQC9GR
- Local copy for Ryan: `~/Documents/Claude/Projects/Meta Ads/northbeam-research/` (dtc-newsroom.html + data/)
- Repo: https://github.com/rcc-data/dtc-newsroom

## Rules
- Only add figures read from the source. Never estimate a missing figure; leave the cell blank and note it.
- Every new figure needs a `library.py` entry (id, date, src, title, url, stats, data, q quotes, pub) so the source drawer can show it.
- Read pages with the built-in browser on Ryan's computer (the weekly index is an image table; X needs his signed-in session). Do not type passwords; if X is signed out, skip X and say so in the summary.
- After editing: `python3 build.py`, then `node tests/shot.js` (needs Chart.js locally: `npm pack chart.js@4.4.1` and extract to /tmp/cj) and confirm `errors []` and no overflow.
- Then `node tests/sweep.js normal` and `node tests/sweep.js dead`. Both must print `errors none blank none`. Never publish if either fails. (The sweep clicks every toggle, dropdown and chart on every page; `dead` simulates a viewer that pauses animation frames.)
- Never replace Chart.js default objects wholesale (e.g. `Chart.defaults.animation = {...}`); set individual properties. Colour animations stay off (`Chart.defaults.animations.colors=false`).
- Publish: Artifact publish with `url` = the live page above and `file_path` = a copy of `dtc-newsroom.html`. Then commit and push to `main`, and copy `dtc-newsroom.html` + changed CSVs to the local folder.
- Finish with a 3–5 line summary for Ryan: what was added, the biggest moves, anything skipped.

## Daily (weekdays, 12:00 Vancouver) — the one scheduled run
This replaces the old weekly run. Every weekday do steps 1–4; on the days in step 5 also do that desk's capture from its section below.

1. **Inbox.** Gmail (connected inbox ryan.clarke@jdcanada.ca; newsletters arrive addressed to the ryanclarke@jdcanada.ca alias) since the previous run: `newer_than:4d (from:northbeam OR from:beehiiv OR from:commonthreadco.com OR from:foxwelldigital OR from:triplewhale OR from:haus.io OR from:motionapp OR from:runneth OR from:modernretail.co OR from:2pml OR from:graphite.io OR from:dtcnewsletter OR subject:(thumbstop OR "media buyer" OR "whale mail" OR "dtc index" OR "digital download" OR "dtc newsletter"))`. Read each newsletter in full (get_thread). Emails with no web archive (CTC DTC Index, Foxwell Digital Download, Whale Mail) are sources in their own right: log them in the inventory with the email's "view in browser" link if it has one, otherwise skip the row but still extract figures (library entry url = the brand's newsletter page, src="Newsletter").
   If a newsletter that should be arriving (Northbeam The Media Buyer, DTC Newsletter, 2PM; Ryan subscribed to DTC Newsletter and the Northbeam newsletter on 30 Oct 2026) has never arrived, say so in the summary: the subscription may not have confirmed.
2. **Sites.** Run the collectors in tools/collect.md for every source (SINCE = that publisher's newest date in data/wire_articles.csv), save each result to tools/inbox/<CODE>.txt, then `python3 tools/wire_inventory.py --clear-inbox`. CTC sits behind a Cloudflare check: if the page shows "Just a moment…", skip CTC today and say so. Never try to get round it.
3. **Figures.** Open every new item that looks data-bearing (titles with numbers, "data", "benchmark", "survey", "report", "index", CPM/ROAS/CAC/CVR, BFCM, earnings; any Northbeam newsletter; Haus research reports). Add only figures stated in the source: append to the matching CSV (Northbeam weekly index → mbi_new.csv; Meta weekly charts → meta_cpm_weekly_approx.csv / meta_weekly_h1.csv; CTC → ctc_*.csv; Foxwell → fox_*.csv; Haus → haus_*.csv; Triple Whale → tw_*.csv; Motion → motion_*.csv; X posts → nb_x_posts.csv), and add a library.py entry (id, pub, date, src, title, url, stats, data, q) for each. The inventory marks the article DATA automatically once its URL is in the library. A new kind of figure that fits no CSV gets a new CSV + REG entry in build.py + a chart or table on the publisher's desk.
4. **Insights.** The Wire page computes its own takeaways. If the new figures change the story, rewrite the front-page lead (`#v-front` h2 + dek), the relevant desk headline/dek, the `STORIES` items and the ticker; check the Trends desk still reads correctly. Say what changed in the summary.
5. **Heavy captures on their days:** Thursday (or the first run after a new issue): Northbeam Media Buyer Index; Monday: Motion / Runneth top ads (32 lists) and Triple Whale benchmarks snapshot; first weekday of the month: CTC DTCCI; Haus, Northbeam and Bryan Bumgardner on X, and Curtis Howland on LinkedIn, every run if signed in. 24 Nov – 2 Dec also do BFCM Live (its own scheduled runs cover it; don't duplicate rows).
6. Build, test (all three: both sweeps and tests/nav.js), publish, commit and push (`git pull --rebase` first), copy to the local folder, as in Rules. If nothing new was found anywhere, change nothing and say so.
7. Summary (push notification, no em dashes): new articles by source, figures added, story changes, anything skipped.

## Weekly (Thursday) — Northbeam Media Buyer Index
1. Open https://themediabuyer.northbeam.io/archive and find issues published since the newest `week_end` in `data/mbi_new.csv`.
2. Each issue has the weekly platform table (image): CPM, CTR, CPC, CAC, CVR, ROAS week-over-week %, budget share % and share Δ (pp) for Meta, All other, Google, TikTok, YouTube, AppLovin, Microsoft, Snapchat, Pinterest, Vibe. Transcribe to new rows at the **top** of `data/mbi_new.csv` (newest first) with `week_start,week_end` as printed. Zoom screenshots to read every digit; re-check sums of share ≈ 100.
3. Also check https://x.com/northbeam for posts with charts since the last run; add any data to a CSV + library entry.
4. Rewrite the front-page lead (`<h2>` + dek in `#v-front`) and the `STORIES` array Channels / Share items to reflect the new week. Update the ticker `extra` list if a headline number changed.
5. Update the `mb-weekly` library entry stats (weeks transcribed count, latest issue date).

## Weekly — Motion / Runneth "Top ads this week" (32 lists)
1. Lists come from https://motionapp.com/trending/sitemap.xml (main page + 31 industry slugs). In the built-in browser on motionapp.com, fetch each `/trending/<slug>/` and parse `brandName`, `aspectRatio`, `activeForDays` from the page's `self.__next_f` payload (first 30 per list).
2. Append rows to `data/motion_trending.csv`: `snapshot,list,rank,brand,aspect,active_days` (snapshot = today, list = `all` or the slug). Keep older snapshots. Fix escapes (`\u0026` → `&`).
3. Check https://runneth.com/sitemap-index.xml for new `/thumbstop-pulse/` or `/research/` pages; add new reports as data + library entries (`pub="Motion"`).

## Weekly — Triple Whale benchmarks snapshot
1. Open https://benchmark.triplewhalelabs.com/benchmarks/health_and_wellness/ in the built-in browser and note the `/api/cohort?...&dateStart=…&dateEnd=…` request the page makes (trailing 30 days ending today).
2. For the 12 industries already in `data/tw_benchmarks_weekly.csv`, request that same cohort view (gmvBand=1m-10m, aovBand=any, the page's own date window) and append rows: `snapshot,window_start,window_end,industry,gmv_band,channel,cohort_size,metric,p25,median,p75` for `total` (channel `all`) and each `byChannel` entry, metrics roas,cpa,cpm,cpc,ctr,cvr,aov,ncPercent,addToCartRate,discountRate.
3. Never request past date windows: Triple Whale's history is a modelled seasonal index, not weekly data.

## Weekly — Haus and Northbeam on X
1. Search X (signed-in built-in browser) for `from:oliviaakory filter:media`, `from:HausAnalytics filter:media`, `from:northbeam filter:media` and `from:BryanBumgardner filter:media` since the last run. For posts with data charts, open the image (`pbs.twimg.com/media/<id>.jpg?name=large`), transcribe to a CSV (state "read from chart (approx)" where values aren't labelled), and add a library entry with the post URL and an exact short quote.
2. Check https://haus.io/blog-categories/research-reports for new reports.

## Every run — Curtis Howland on LinkedIn (added 30 Oct 2026)
1. Needs Ryan's signed-in LinkedIn session in the built-in browser. Open https://www.linkedin.com/in/curtishowland/recent-activity/all/ ; if it lands on the authwall / "Join LinkedIn", skip and say so (never type a password).
2. Keep posts that carry an insight with a chart, image of data, or video (skip reshares with no commentary, hiring and event posts). First capture: take every such post back to 1 Jan 2026; after that, posts since the newest date in `data/li_howland_posts.csv`.
3. Log each to `data/li_howland_posts.csv` (`date,type,headline,figure,url`, type ∈ chart/video/insight) and add a library.py entry (pub="Curtis Howland", src="LinkedIn", exact short quote, figures only as stated; chart readings labelled approx). Video posts: record the stated takeaway, not a transcript.
4. The first capture also creates the desk: REG entry in build.py, `PUBDESKS` + `#deskMenu` item, a table of the posts; then `node tests/nav.js`.

## Daily 24 Nov – 2 Dec 2026 — BFCM Live
1. Look for new BFCM 2026 figures: Northbeam (X, blog, newsletter), Triple Whale live BFCM page / report, Adobe Digital Insights and Shopify press releases, Haus.
2. Append rows to `data/bfcm2026_live.csv`: `date,day,source,metric,value,note,url`. For Northbeam-style YoY by day use `day` ∈ {Tue-Thu (pre-BF), Black Friday, Saturday, Sunday, Cyber Monday} and `metric` ∈ {spend, revenue, mer, cac} with a numeric YoY %. Other headlines: `day` = Cyber Week, `metric` = short label, `value` = text.
3. Rebuild, check, publish.

## Quarterly — Meta earnings (next: Q4 2026, late Jan 2027)
1. From Meta's release: ad revenue ($bn), ad impressions YoY %, average price per ad YoY %, next-quarter revenue guidance. Regional price per ad (US & Canada, Asia-Pacific) from the earnings slides / coverage.
2. Append a row to `data/meta_earnings.csv`, add a `meta-qN-YY` library entry, and update the `#v-mkt` headline, `mkRead` text and KPI strip in `renderMkt`.

## Common Thread Collective (weekly check, monthly data)
- DTCCI: open dtcci.co in the built-in browser, read `window.infographicData` (entities[*].props.chartData.data[0]) and append any new month to data/ctc_dtcci.csv. New reading lands early each month.
- Research pages: check commonthreadco.com/sitemap.xml lastmod for /pages/*benchmark* and research.commonthreadco.com. New quarter = new ctc_mix/ctc_tier/ctc_mer rows plus a library entry.
- Blog and podcast: scan /blogs/ecommerce-playbook and /blogs/coachs-corner for posts since last run that publish portfolio data (DTC Index, CPM, BFCM, incrementality). Add figures with a library entry per figure; never estimate.
- Meta CPM: if CTC publishes a new portfolio CPM month, append to data/ctc_meta_cpm.csv.
- The weekly DTC Index email has no public archive. Skip unless a Gmail source is set up.

## Trends desk (no separate capture)
- Built entirely from the other desks' CSVs. When you add a week or month anywhere, check the Trends page renders and the KPI strip and "What the long view says" sentences still read correctly (they are computed from the latest rows).
- Quarter scoreboard drops any quarter with fewer than 2 Northbeam weeks; the current quarter is never colour-compared with last year.

## Foxwell Digital (weekly check)
- List new posts: fetch https://www.foxwelldigital.com/blog?format=json in the built-in browser (items[].publishOn, title). Look for surveys (agency benchmark, Q4 outlook with Northbeam) and member field reports with figures.
- New survey: add rows to data/fox_q4_2026_survey.csv (new question/answer rows; new year → new file or a year column) or data/fox_agency_survey.csv, only figures stated in text. Library entry pub="Foxwell".
- Dated member reports with figures: append to data/fox_field_reports.csv.
- The Foxwell Digital Download email has no archive. Skip.

## Wire headlines
- data/wire_headlines.csv is no longer maintained by hand: the Wire inventory (below) supersedes it. Leave it as is.

## Varos
- Stopped publishing ecommerce benchmarks in 2025 (varos.com is now an AI business-analyst product). Nothing to capture. data/varos_meta_cpm_archive.csv is a fixed archive.

## Front page and nav
- Front page lead is cross-source (Northbeam, Meta, CTC, Foxwell). Refresh its headline/dek when the story changes; the chart, KPI strip and "From the desks" tiles compute from the data automatically (tiles show each publisher's newest library entry, excluding cadence entries).
- New publisher desks go in the Desks dropdown (`#deskMenu`) and in `PUBDESKS`. Run `node tests/nav.js` after nav changes.

## Wire inventory
- data/wire_articles.csv: `date,pub,title,url,type,topics`, one row per article since 1 Jan 2026, newest first. Built by tools/wire_inventory.py (collectors in tools/collect.md). Library entries dated 2026+ are added automatically. Topics are keyword tags from the TOPICS list in the script: add a topic there, not by hand.
- The Wire page (`renderWire`) shows KPIs, computed takeaways, output by month, topic share by month and the searchable table. Modern Retail is off the volume chart by default (it outnumbers the operator sources).
- Runneth's blog has no publish dates and is not listed; Motion research enters via the library.

## Northbeam Meta desk (weekly)
- Log every Northbeam / Bryan Bumgardner post with Meta or market data in data/nb_x_posts.csv (date, account, headline, figure, feeds, url).
- When Northbeam republishes a weekly Meta chart (CPM/YoY, CPC, CTR/CVR, CAC/ROAS), digitise it week by week rather than by month: load the pbs.twimg.com image (?format=png&name=large) in the built-in browser, read line pixels per column on a canvas, calibrate y from the axis label rows and x from the month labels, then pin the chart's annotated values exactly. Update data/meta_cpm_weekly_approx.csv (CPM + YoY) or data/meta_weekly_h1.csv. Mark interpolated weeks.
- Northbeam's public weekly index (Media Buyer Index) starts w/e 3 Jan 2026; nothing earlier was published. The weekly Meta CPM chart is the longest weekly series (from Jan 2025).
- Share of wallet: Northbeam has not published Q3 2025. The share page computes Q2-Q4 2026 from the weekly index (all-tracked basis from w/c 3 May). Replace with a published quarterly figure if one appears.
