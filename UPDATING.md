# DTC Newsroom — update runbook

This file is the procedure scheduled runs follow. The page is built from `template.html` + `data/*.csv` + `library.py` by `python3 build.py`, which writes `dtc-newsroom.html` (published to the artifact) and `index.html` (the GitHub Pages site, https://dtcnewsroom.com/). Always commit both.

- Live page (claude.ai Artifact): https://claude.ai/artifact/YJdE49u9nVWATDWNyQC9GR
- Local copy for Ryan: `~/Documents/Claude/Projects/Meta Ads/northbeam-research/` (dtc-newsroom.html + data/)
- Repo: https://github.com/rcc-data/dtc-newsroom

## Rules
- Only add figures read from the source. Never estimate a missing figure; leave the cell blank and note it.
- Every new figure needs a `library.py` entry (id, date, src, title, url, stats, data, q quotes, pub) so the source drawer can show it.
- Read pages with the built-in browser on Ryan's computer (the weekly index is an image table; X needs his signed-in session). Do not type passwords; if X is signed out, skip X and say so in the summary.
- The page opens behind a passcode wall (code 1738, remembered per browser; for fun, not security). Tests skip it with `window.__NOGATE=1`; `node tests/gate.js` checks the wall itself.
- After editing: `python3 build.py`, then `node tests/shot.js` (needs Chart.js locally: `npm pack chart.js@4.4.1` and extract to /tmp/cj) and confirm `errors []` and no overflow.
- Then `node tests/sweep.js normal` and `node tests/sweep.js dead`. Both must print `errors none blank none`. Never publish if either fails. (The sweep clicks every toggle, dropdown and chart on every page; `dead` simulates a viewer that pauses animation frames.)
- Never replace Chart.js default objects wholesale (e.g. `Chart.defaults.animation = {...}`); set individual properties. Colour animations stay off (`Chart.defaults.animations.colors=false`).
- Publish: Artifact publish with `url` = the live page above and `file_path` = a copy of `dtc-newsroom.html`. Then commit and push to `main`, and copy `dtc-newsroom.html` + changed CSVs to the local folder.
- Finish with a 3–5 line summary for Ryan: what was added, the biggest moves, anything skipped.

## Two daily passes (from 5 Nov 2026)
Ryan's laptop is off until after 9am, so the day is split:
- **Source fetch, about 7:23 every day (GitHub Actions, `.github/workflows/fetch-sources.yml`).** `tools/fetch_sources.py` reads Northbeam newsletter and blog, Common Thread, Haus, Triple Whale, Modern Retail, 2PM, Graphite, Direct to Consumer and Curtis Howland's Substack from GitHub's servers, writes `tools/inbox/<CODE>.txt` and the text of every new item to `notes/fetched/<CODE>/`, logs to `notes/fetched/LAST_RUN.txt` and commits "Fetch sources <date>". A 7:53 backup schedule re-runs it only if the 7:23 run didn't happen (GitHub sometimes drops scheduled runs; it did on 6 Nov). No browser, laptop or approval needed. Foxwell's robots.txt disallows bots: the laptop pass covers it.
- **Morning cloud pass, 8:17 every day (no laptop, no web access).** `git pull`; if `notes/fetched/LAST_RUN.txt` isn't from today, trigger the workflow (GitHub `actions_run_trigger`, workflow `fetch-sources.yml`, ref `main`) and wait for it. Then Gmail newsletters, `python3 tools/wire_inventory.py --clear-inbox`, figures from the saved texts, build, tests, publish, push, and the Slack digest. Never use WebFetch or a browser in this pass: unattended runs can't answer permission prompts.
- **Laptop pass, 11:37 weekdays (built-in browser on Ryan's computer).** Only what needs a signed-in or real browser: X (Northbeam, Haus, Olivia Kory, Bryan Bumgardner), Curtis Howland LinkedIn posts and their media, Foxwell, Runneth/Motion trending lists, Triple Whale benchmarks, Northbeam weekly index images, CTC if the cloud pass was blocked. No Slack message: anything new goes into the next morning's digest.

## Daily steps (both passes; the digest only in the morning pass)
This replaces the old weekly run. Every weekday do steps 1–4; on the days in step 5 also do that desk's capture from its section below.

1. **Inbox.** Gmail (connected inbox ryan.clarke@jdcanada.ca; newsletters arrive addressed to the ryanclarke@jdcanada.ca alias) since the previous run: `newer_than:4d (from:northbeam OR from:beehiiv OR from:commonthreadco.com OR from:foxwelldigital OR from:triplewhale OR from:haus.io OR from:motionapp OR from:runneth OR from:modernretail.co OR from:2pml OR from:graphite.io OR from:directtoconsumer.co OR from:dtcnewsletter OR subject:(thumbstop OR "media buyer" OR "whale mail" OR "dtc index" OR "digital download" OR "dtc newsletter"))`. Read each newsletter in full (get_thread). Emails with no web archive (CTC DTC Index, Foxwell Digital Download, Whale Mail) are sources in their own right: log them in the inventory with the email's "view in browser" link if it has one, otherwise skip the row but still extract figures (library entry url = the brand's newsletter page, src="Newsletter").
   If a newsletter that should be arriving (Northbeam The Media Buyer, DTC Newsletter, 2PM; Ryan subscribed to DTC Newsletter and the Northbeam newsletter on 30 Oct 2026) has never arrived, say so in the summary: the subscription may not have confirmed.
2. **Sites.** Run the collectors in tools/collect.md for every source (SINCE = that publisher's newest date in data/wire_articles.csv), save each result to tools/inbox/<CODE>.txt, then `python3 tools/wire_inventory.py --clear-inbox`. CTC sits behind a Cloudflare check: if the page shows "Just a moment…", skip CTC today and say so. Never try to get round it.
3. **Figures.** Open every new item that looks data-bearing (titles with numbers, "data", "benchmark", "survey", "report", "index", CPM/ROAS/CAC/CVR, BFCM, earnings; any Northbeam newsletter; Haus research reports). Add only figures stated in the source: append to the matching CSV (Northbeam weekly index → mbi_new.csv; Meta weekly charts → meta_cpm_weekly_approx.csv / meta_weekly_h1.csv; CTC → ctc_*.csv; Foxwell → fox_*.csv; Haus → haus_*.csv; Triple Whale → tw_*.csv; Motion → motion_*.csv; X posts → nb_x_posts.csv), and add a library.py entry (id, pub, date, src, title, url, stats, data, q) for each. The inventory marks the article DATA automatically once its URL is in the library. A new kind of figure that fits no CSV gets a new CSV + REG entry in build.py + a chart or table on the publisher's desk.
4. **Front page and analysis (every run).** "Today in the newsroom" builds itself from the Wire (latest headlines) and new library entries (new charts and data); add a line to the `extra` list in `renderToday` when you create a new chart or desk section. When two or more sources move the same way (e.g. Meta CPMs, BFCM timing, discounting), write or refresh a cross-source piece in `data/analysis.json` (kicker, title, dek, 3 to 5 body paragraphs with only sourced numbers, sources with URLs, link to the desk). Keep the newest 3 to 4 pieces; rewrite a piece when its numbers move rather than adding a near-duplicate.
5. **BFCM (every run until mid-December).** Add every new BFCM figure (forecasts, surveys, platform changes, live results) to `data/bfcm2026_outlook.csv` (or `bfcm2026_live.csv` from 24 Nov) with publisher, date and URL, and update `data/bfcm2026_briefing.json` when a takeaway's numbers change. Search Adobe, Salesforce, Shopify, NRF, Bain, Deloitte, RCC, Triple Whale, Northbeam, Klaviyo, Attentive, Common Thread and TikTok newsrooms each run.
6. **Insights.** The Wire page computes its own takeaways. If the new figures change the story, rewrite the front-page lead (`#v-front` h2 + dek), the relevant desk headline/dek, the `STORIES` items and the ticker; check the Trends desk still reads correctly. Say what changed in the summary.
7. **Heavy captures on their days:** Thursday (or the first run after a new issue): Northbeam Media Buyer Index; Monday: Motion / Runneth top ads (32 lists) and Triple Whale benchmarks snapshot; first weekday of the month: CTC DTCCI; Haus, Northbeam and Bryan Bumgardner on X, and Curtis Howland on LinkedIn, every run if signed in; Curtis Howland newsletter every run. 24 Nov – 2 Dec also do BFCM Live (its own scheduled runs cover it; don't duplicate rows).
8. Build, test (both sweeps, tests/nav.js and tests/gate.js), publish, commit and push (`git pull --rebase` first), copy to the local folder, as in Rules. If nothing new was found anywhere, change nothing and say so.
9. Summary (push notification, no em dashes): new articles by source, figures added, story changes, anything skipped.
10. Morning Slack digest (every run, after publishing; aim to send by 9:15 Vancouver). See "Morning Slack digest" below.

## Morning Slack digest
- One Slack DM to Ryan (user U0ADD8B569Z, slack_send_message), sent at the end of the daily run so it includes everything the run just found. A separate 9:15 fallback task sends it from the published data if the daily run hasn't by then; before sending, read the DM and never send twice in a day (if the fallback already sent, post only items it missed, as a short "Also this morning" follow-up).
- Pick 5 to 8 items new since the previous digest (read the DM history to avoid repeats): newsroom analysis pieces first, then data-bearing items (figures, benchmarks, platform changes, earnings, BFCM), then the strongest operator takes. Modern Retail only for big news. Fewer than 3 new items: say "Quiet night" and add the 2 to 3 most important current stories, labelled still current.
- Format: first line `*DTC Newsroom · <weekday d Mon>*`, then one bullet per item: `• *Headline* (Source): hot take in one or two short sentences, our words, why it matters to a DTC buyer on Meta and Google, only figures the source states. <url|Read it>`; last line `Full newsroom: https://dtcnewsroom.com/`. Quotes under 15 words. No em dashes.
- Time zone: America/Vancouver. B.C. has been on permanent daylight time (UTC-7) since 8 Mar 2026; clocks no longer change.

## This week's headlines tab (#headlines, added 6 Nov 2026)
Ryan's brief: a whole tab for the week's news that gives new insights room, Northbeam first, newest at the top, and deep dives on the big reports.
- Data: `data/headlines.json` = `{weeks:[{id,start,end,title,dek,items:[...]}], features:[...]}`. Weeks run Monday to Sunday (id = the Monday). On the first run of a new week, add a new week object; older weeks stay as the archive.
- Every run, for each new data-bearing or decision-changing item (anything that earns a library entry, plus big platform news), add an item to the current week: `id, date (the day it landed), pub, impact (3 = changes what a buyer should do this week, 2 = worth acting on soon, 1 = context), topics (Meta, Google, BFCM, Measurement, AI, Creative, Benchmarks, Amazon), lib (the library id), headline (ours, max ~14 words, the finding not the title), take (2 to 3 sentences, only stated figures), figs (2 to 3 short chips), why (one or two sentences: what a DTC buyer on Meta and Google should do), url, optional to (desk) and feature (deep-dive id)`. Refresh the week's `title` and `dek` when the story changes.
- Ranking is automatic: Northbeam first, then impact, then date. "Just in" shows the four newest; items under 36 hours old get a NEW badge.
- Deep dives (`features`): write one for any major report (every Northbeam long-form issue or guide, big platform or industry reports). Schema as in `tools/make_headlines_2026_11_02.py`: kicker, title, dek, byline, url, kpis, quote (exact, under 15 words), headlines (the report broken into 6 to 10 headline + explanation pairs, our words), analysis (what it's really saying, read against the newsroom's other data), actions (dated what-to-do list for a DTC buyer), pushback (where we disagree or it falls short), checklist, optional index table and related links. Link it from the item with `feature`. Opens at `#hl-deep/<id>`.
- The site's "what it means" is written for a DTC buyer on Meta and Google. Never put JD Sports or client specifics on the site; those go to Ryan in chat.

## Runneth weekly-performers watch (daily, added 6 Nov 2026)
- `tools/fetch_sources.py` → `runneth_watch()` reads Runneth's four Weekly Trending lists (apparel, sports-fitness, retail, accessories) every morning from GitHub Actions and compares the ranked brands with the last state (`notes/fetched/RUNNETH/state.json`, seeded from the newest week in `data/runneth_trending_ads.csv`). It logs `RUNNETH: UPDATED ...`, `RUNNETH: unchanged ...` or `RUNNETH: could not check ...` to `notes/fetched/LAST_RUN.txt` and appends to `notes/fetched/RUNNETH/history.csv`.
- Morning pass: if LAST_RUN says UPDATED, put it in the digest and tell Ryan the lists turned over (which lists, new top 3), then capture the new week per "Weekly (Monday) — Runneth" even if it isn't Monday. If it says "could not check", the weekday laptop pass checks the lists in the browser and records the result in history.csv.

## Weekly (Thursday) — Northbeam Media Buyer Index
1. Open https://themediabuyer.northbeam.io/archive and find issues published since the newest `week_end` in `data/mbi_new.csv`.
2. Each issue has the weekly platform table (image): CPM, CTR, CPC, CAC, CVR, ROAS week-over-week %, budget share % and share Δ (pp) for Meta, All other, Google, TikTok, YouTube, AppLovin, Microsoft, Snapchat, Pinterest, Vibe. Transcribe to new rows at the **top** of `data/mbi_new.csv` (newest first) with `week_start,week_end` as printed. Zoom screenshots to read every digit; re-check sums of share ≈ 100.
3. Also check https://x.com/northbeam for posts with charts since the last run; add any data to a CSV + library entry.
4. Rewrite the front-page lead (`<h2>` + dek in `#v-front`) and the `STORIES` array Channels / Share items to reflect the new week. Update the ticker `extra` list if a headline number changed.
5. Update the `mb-weekly` library entry stats (weeks transcribed count, latest issue date).

## Weekly (Monday) — Runneth Weekly Trending Ads (desk "Runneth", tab #mo-trend)
Runneth says only "Updated weekly" and gives no day; on Wed 4 Nov 2026 its lists still matched the Monday 2 Nov capture rank for rank.
1. Source: Ryan's Supabase project jd-bfcm-swipe-file (cymkcvdsxoneojfisjgk), table `tr_ads` (week, category, rank, brand, age, kind, video_s, poster_s, images_s, logo_s), filled every Monday from Runneth's apparel, sports-fitness, retail and accessories lists; media in the public `trending` bucket.
2. For each new `week` not yet in `data/runneth_trending_ads.csv`: query the rows with the Supabase connector. This cloud session can't reach supabase.co directly, so pull the media in the built-in browser: fetch each poster/first image (and second carousel image) and logo, re-encode on a canvas to webp (420px wide, q 0.74; logos 64px), return ≤200KB per call, and write them to `rn/<week>/<category>-<rank>-<poster|img1|img2|logo>.webp`.
3. Enrich from the same week's Runneth pages (`/trending/<category>/`, `self.__next_f` payload): aspectRatio, activeForDays, brand followerCount, and the Meta Ad Library id (the number after `swipe-file-source-link/` in thumbnailUrl/videoUrl). Check brand names match rank by rank.
4. Append rows to `data/runneth_trending_ads.csv`; `video_url` stays the Supabase mp4 (plays on dtcnewsroom.com; the artifact may block it, so the lightbox links to the Meta Ad Library).
5. Publish with every new `rn/<week>/*.webp` in the Artifact `files` map (same published path), and commit `rn/` with the page.

## Runneth creative benchmarks: how many ads to launch (#mo-bench)
- `data/creative_volume_2026.csv`: figures from Sicard, MHI, Billo, Foxwell (Motion headlines) and Curtis Howland. The source cards and the comparison chart are in `renderCv` in template.html. Motion's own talk page redirects to runneth.com; read it in the built-in browser and add its figures when possible.

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
5. Each logged post opens as an article at `#hw-post/li-howland-YYYYMMDD`, showing his image or video and the full post text (republished with Curtis Howland's permission, credited and linked back). For each new post: in the signed-in built-in browser on linkedin.com, fetch `/embed/feed/update/urn:li:activity:<id>`; the image is the `feedshare-shrink_800` (or `videocover`) URL, the text is the `<meta name="description">` content minus the trailing "| N comments on LinkedIn", the video is the `mp4-640p` URL. Re-encode the image to webp (≤1000px, q 0.84, ≤200KB base64) and return it as base64 (bridge limit ~250K chars per call), save to `hw/<date>.webp`. Videos: open a tab on `https://cymkcvdsxoneojfisjgk.supabase.co/...` (linkedin.com's CSP blocks Supabase), fetch the mp4 and POST it with the anon key to `storage/v1/object/creative/howland/<date>.mp4`. Record img/w/h/text/video in `data/howland_media.json`. Publish new `hw/*.webp` in the Artifact `files` map; videos only play on dtcnewsroom.com (the artifact blocks external hosts and links to LinkedIn instead).
6. Done 2 Nov 2026: first capture (124 posts, 1 Jan to 2 Nov 2026) and the `#howland` desk. Posts are read from `/recent-activity/shares/` by scrolling and reading each post's `data-urn` (activity id >> 22 = ms timestamp). `figure` = first stated figure line, verbatim.

## Curtis Howland Meta Ads charts (desk #howland)
- The desk leads with his Meta Ads charts, redrawn in Chart.js and grouped in chapters: `data/howland_meta_charts.json`, built by `python3 tools/howland_meta.py notes/howland_meta_transcriptions.json data/howland_meta_charts.json` (chapter list and per-chart options live in the script).
- `notes/howland_meta_transcriptions.json` holds one transcription per image (kind, data, his message, approx flag, notes). When a new Meta post or issue has a data chart: get the image (LinkedIn: fetch `/feed/update/<urn>/` in the signed-in built-in browser and take the `feedshare-shrink_1280` URL; Substack: `body_html` image src), read it, append a transcription in the same schema, add it to a chapter in the script and rebuild. Printed numbers exact; anything read off bars or lines gets approx=true. Never invent values.

- Headlines, big quotes and hot takes: `data/howland_headlines.json`, one object per newsletter issue (date, url, title, headline max 12 words, take, exact verbatim quote max 25 words, heat 1-3, topic, meta). Add one for each new issue; check the quote is verbatim.

## Every run — Curtis Howland newsletter (Substack, added 2 Nov 2026)
1. https://newsletter.curtishowland.com (curtishowland.substack.com). In the built-in browser on that origin: `fetch('/api/v1/archive?sort=new&limit=50')`; new issues since the newest date in `data/howland_substack.csv`. Body text: `/api/v1/posts/<slug>` → `body_html`.
2. Append each issue to `data/howland_substack.csv` (`date,title,subtitle,url`) and add a library entry (pub="Curtis Howland", src="Newsletter", id `howland-ss-<slug>`, exact short quote).
3. Issues with his own data (ad-library pulls, account analyses) get their figures, as stated, in a CSV on the desk, e.g. `data/howland_bf_ads_2025.csv` from "68,245 Black Friday Ads, Taken Apart" (2 Nov 2026). Third-party figures he cites stay out.

## BFCM Live prediction and Howland ad study (added 4 Nov 2026)
- `data/bfcm2026_predictions.json` holds the newsroom's own calls (verdict, score tiles, 15 items: metric, 2025 value, call, range, confidence, basis, sources). Refresh a call only when a sourced input moves (e.g. a new Adobe forecast or Northbeam CPM read); keep the old call in the basis text ("was +7%"). From 24 Nov, fill each item's `actual` field as results land and say in the summary which calls were right.
- `data/howland_bf_study.json` is Curtis Howland's Field study Nº03 (curtishowland.com/black-friday/breakdown, read from the page's `__NEXT_DATA__`): category profiles (launch curve, discount mix, extras, early access, run days), daily launches, lead offers, example ads (Meta Ad Library links). Static: it describes BFCM 2025.

## Daily 24 Nov – 2 Dec 2026 — BFCM Live
1. Look for new BFCM 2026 figures: Northbeam (X, blog, newsletter), Triple Whale live BFCM page / report, Adobe Digital Insights and Shopify press releases, Haus.
2. Append rows to `data/bfcm2026_live.csv`: `date,day,source,metric,value,note,url`. For Northbeam-style YoY by day use `day` ∈ {Tue-Thu (pre-BF), Black Friday, Saturday, Sunday, Cyber Monday} and `metric` ∈ {spend, revenue, mer, cac} with a numeric YoY %. Other headlines: `day` = Cyber Week, `metric` = short label, `value` = text.
3. Rebuild, check, publish.

## Quarterly — Meta earnings (next: Q4 2026, late Jan 2027)
1. From Meta's release: ad revenue ($bn), ad impressions YoY %, average price per ad YoY %, next-quarter revenue guidance. Regional price per ad (US & Canada, Asia-Pacific) from the earnings slides / coverage.
2. Append a row to `data/meta_earnings.csv`, add a `meta-qN-YY` library entry, and update the `#v-mkt` headline, `mkRead` text and KPI strip in `renderMkt`.

## Quarterly — Google (Alphabet) earnings (next: Q4 2026, early Feb 2027)
1. From Alphabet's earnings release and 10-Q (abc.xyz investor pages or s206.q4cdn.com/479360582/files/doc_financials/<year>/<qN>/; sec.gov is blocked from the cloud): Google Search & other, YouTube ads, Google Network and total advertising revenue ($bn); Search and YouTube YoY % only where stated; paid clicks, cost per click, Network impressions and cost per impression YoY % from the 10-Q "Monetization Metrics". Q4 has no 10-Q: leave the click columns blank and note the 10-K full-year figures in the CSV header.
2. Append a row to `data/google_earnings.csv`, add a `goog-qN-YY` library entry (pub "Google"), and update the `#v-mkt-google` headline, KPI strip and "The read" in `renderMktG`. The Earnings desk has two sub-pages: `#mkt` (Meta) and `#mkt-google`.

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
- Long pages get an automatic sticky "On this page" bar (`buildJump`): section heads when a page has 3+, otherwise card titles when it has 4+. Curtis Howland's desk is split into sub-pages (`#howland`, `#hw-charts`, `#hw-posts`, `#hw-news`, `#hw-bf`, articles at `#hw-post/<id>`) with its own subrow.
- Front page lead is cross-source (Northbeam, Meta, CTC, Foxwell). Refresh its headline/dek when the story changes; the chart, KPI strip and "From the desks" tiles compute from the data automatically (tiles show each publisher's newest library entry, excluding cadence entries).
- New publisher desks go in the Desks dropdown (`#deskMenu`) and in `PUBDESKS`. Run `node tests/nav.js` after nav changes.

## Direct to Consumer desk (daily)
- Each new issue: add to the Wire via the DTCNL collector. Skip sponsored blocks (they end "* sponsored" or sell a product: Insense, Clustie, SARAL, Walmart Marketplace, Dataships, minisocial and similar).
- Brand teardowns (Pilothouse brand breakdowns, ad breakdowns, tech-stack pieces): append to data/dtc_teardowns.csv (date, brand, focus, url). Focus is one of Meta ads, Website & CRO, Email & SMS, Google search, Tech stack, Campaign.
- Headlines and hot takes: add only strong, data-led or contrarian news items to data/dtcnl_headlines.json (headline and take in our words, quote verbatim and under 15 words, source = the original source DTC is citing, heat 1–3). Not every issue earns one.
- New DTC survey: add its landing-page figures to data/dtc_research.csv and a library entry (pub "Direct to Consumer", src "Report"), and a chart on the desk if it doesn't fit an existing one.
- data/dtc_topics.csv: rebuild monthly from the issue text (keyword match per topic, share of issues).

## Wire inventory
- data/wire_articles.csv: `date,pub,title,url,type,topics`, one row per article since 1 Jan 2026, newest first. Built by tools/wire_inventory.py (collectors in tools/collect.md). Library entries dated 2026+ are added automatically. Topics are keyword tags from the TOPICS list in the script: add a topic there, not by hand.
- The Wire page (`renderWire`) shows KPIs, computed takeaways, output by month, topic share by month and the searchable table. Modern Retail is off the volume chart by default (it outnumbers the operator sources).
- Runneth's blog has no publish dates and is not listed; Motion research enters via the library.

## Northbeam Meta desk (weekly)
- Log every Northbeam / Bryan Bumgardner post with Meta or market data in data/nb_x_posts.csv (date, account, headline, figure, feeds, url).
- When Northbeam republishes a weekly Meta chart (CPM/YoY, CPC, CTR/CVR, CAC/ROAS), digitise it week by week rather than by month: load the pbs.twimg.com image (?format=png&name=large) in the built-in browser, read line pixels per column on a canvas, calibrate y from the axis label rows and x from the month labels, then pin the chart's annotated values exactly. Update data/meta_cpm_weekly_approx.csv (CPM + YoY) or data/meta_weekly_h1.csv. Mark interpolated weeks.
- Northbeam's public weekly index (Media Buyer Index) starts w/e 3 Jan 2026; nothing earlier was published. The weekly Meta CPM chart is the longest weekly series (from Jan 2025).
- Share of wallet: Northbeam has not published Q3 2025. The share page computes Q2-Q4 2026 from the weekly index (all-tracked basis from w/c 3 May). Replace with a published quarterly figure if one appears.
