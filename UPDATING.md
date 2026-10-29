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

## Weekly (Thursday evening UK) — Northbeam Media Buyer Index
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
1. Search X (signed-in built-in browser) for `from:oliviaakory filter:media`, `from:HausAnalytics filter:media` and `from:northbeam filter:media` since the last run. For posts with data charts, open the image (`pbs.twimg.com/media/<id>.jpg?name=large`), transcribe to a CSV (state "read from chart (approx)" where values aren't labelled), and add a library entry with the post URL and an exact short quote.
2. Check https://haus.io/blog-categories/research-reports for new reports.

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

## Wire headlines (weekly)
- Replace data/wire_headlines.csv with the latest ~12 items: Modern Retail (https://www.modernretail.co/feed/, strip utm params), 2PM (https://2pml.com/feed/), Foxwell blog, CTC Coach's Corner (sitemap lastmod). Real article URLs only.

## Varos
- Stopped publishing ecommerce benchmarks in 2025 (varos.com is now an AI business-analyst product). Nothing to capture. data/varos_meta_cpm_archive.csv is a fixed archive.

## Front page and nav
- Front page lead is cross-source (Northbeam, Meta, CTC, Foxwell). Refresh its headline/dek when the story changes; the chart, KPI strip and "From the desks" tiles compute from the data automatically (tiles show each publisher's newest library entry, excluding cadence entries).
- New publisher desks go in the Desks dropdown (`#deskMenu`) and in `PUBDESKS`. Run `node tests/nav.js` after nav changes.
