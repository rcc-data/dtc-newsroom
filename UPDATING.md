# DTC Newsroom — update runbook

This file is the procedure scheduled runs follow. The page is built from `template.html` + `data/*.csv` + `library.py` by `python3 build.py`, which writes `dtc-newsroom.html` (published to the artifact) and `index.html` (the GitHub Pages site, https://rcc-data.github.io/dtc-newsroom/). Always commit both.

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

## Weekly — Motion / Runneth "Top ads this week"
1. Open https://motionapp.com/trending/ . In the page, the ad list is in `self.__next_f` (fields `brandName`, `aspectRatio`, `activeForDays`).
2. Append 30 rows to `data/motion_trending.csv` with `snapshot` = today's date (YYYY-MM-DD), keeping older snapshots.
3. Check https://runneth.com/sitemap-index.xml for new `/thumbstop-pulse/` or `/research/` pages; add any new report as data + library entries (`pub="Motion"`).

## Daily 24 Nov – 2 Dec 2026 — BFCM Live
1. Look for new BFCM 2026 figures: Northbeam (X, blog, newsletter), Triple Whale live BFCM page / report, Adobe Digital Insights and Shopify press releases, Haus.
2. Append rows to `data/bfcm2026_live.csv`: `date,day,source,metric,value,note,url`. For Northbeam-style YoY by day use `day` ∈ {Tue-Thu (pre-BF), Black Friday, Saturday, Sunday, Cyber Monday} and `metric` ∈ {spend, revenue, mer, cac} with a numeric YoY %. Other headlines: `day` = Cyber Week, `metric` = short label, `value` = text.
3. Rebuild, check, publish.

## Quarterly — Meta earnings (next: Q4 2026, late Jan 2027)
1. From Meta's release: ad revenue ($bn), ad impressions YoY %, average price per ad YoY %, next-quarter revenue guidance. Regional price per ad (US & Canada, Asia-Pacific) from the earnings slides / coverage.
2. Append a row to `data/meta_earnings.csv`, add a `meta-qN-YY` library entry, and update the `#v-mkt` headline, `mkRead` text and KPI strip in `renderMkt`.
