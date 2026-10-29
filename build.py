import csv, json, io
from library import LIB
def load(fn):
    note=[];rows=[]
    with open('data/'+fn) as f:
        lines=f.read().splitlines()
    body=[l for l in lines if not l.startswith('#')]
    note=' '.join(l.lstrip('# ').strip() for l in lines if l.startswith('#'))
    r=list(csv.reader(body))
    return note,r[0],r[1:]
REG=[
 ("mbi","Media Buyer Index — weekly channel deltas","mbi_new.csv","Newsletter + X, weekly, Dec 2025–Oct 2026","Week-over-week % change by platform. Budget share is absolute %. Before the week of 05/03/2026 shares exclude 'All other platforms' and share Δ is a relative % change; from 05/03 share Δ is percentage points."),
 ("meta_cpm","Meta weekly CPM, Jan 2025–Oct 2026 (read from chart)","meta_cpm_weekly_approx.csv","Newsletter 2026-10-22",None),
 ("meta_roas_cac","Meta blended ROAS & first-time CAC (read from charts)","meta_roas_cac_weekly_approx.csv","X 2026-10-23 / 2026-10-28",None),
 ("meta_monthly","Meta CPM, CPC, CTR, CVR, 1-day ROAS, CAC (read from H1 charts)","meta_monthly_approx.csv","Newsletter 2026-08-06",None),
 ("lag","Facebook ROAS by Q4 phase (conversion lag)","q4_lag_phases.csv","Newsletter 2026-09-10",None),
 ("bfcm_daily","Cyber Week 2025 by day, YoY","bfcm2025_daily.csv","Newsletter 2026-01-09",None),
 ("bfcm_spend","Spend increase by BFCM period, 2025 vs 2024","bfcm2025_spend_by_period.csv","Blog 2025-12-22",None),
 ("cw2025","Cyber Week 2025 at a glance","cyberweek2025_summary.csv","Blog 2025-12-22",None),
 ("bfcm_industry","BFCM 2025 YoY by industry","bfcm2025_industry.csv","X 2025-12-04",None),
 ("bfcm_pacing","Cyber Five 2024 daily spend pacing","bfcm2024_pacing.csv","Blog 2025-11-07",None),
 ("bfcm_start","When big spenders started BFCM 2024 sales","bfcm2024_sale_start.csv","Blog 2025-11-07",None),
 ("q3_heatmap","Q3 2026 YoY by monthly ad spend & percentile","q3_heatmap.csv","Newsletter 2026-10-22",None),
 ("h1_dist","H1 2026 YoY distribution (all advertisers)","h1_distribution.csv","Newsletter 2026-08-06",None),
 ("h1_spend","H1 2026 YoY by monthly ad spend & percentile","h1_spend_level.csv","Newsletter 2026-08-06",None),
 ("h1_rev","H1 2026 YoY by company revenue & percentile","h1_revenue_band.csv","Newsletter 2026-08-06",None),
 ("h1_aov","H1 2026 YoY by AOV & percentile","h1_aov.csv","Newsletter 2026-08-06",None),
 ("monthly_yoy","Monthly median YoY, all businesses (assembled)","monthly_median_yoy.csv","Blog + Newsletter, multiple",None),
 ("may_retro","May 2026 aggregate YoY","may_retro.csv","Newsletter 2026-06-22",None),
 ("may_meta","May 2026 Meta spend change by spend band","may_meta_spend_by_band.csv","Newsletter 2026-06-22",None),
 ("may_meta_bars","May 2026 Meta average metric changes","may_meta_bars.csv","Newsletter 2026-06-22",None),
 ("may_aov","May 2026 YoY by AOV band","may_aov.csv","Newsletter 2026-06-22",None),
 ("q1_share","Share of tracked ad spend, Q1 2025 vs Q1 2026","q1_share_of_wallet.csv","Newsletter 2026-06-22",None),
 ("april_retro","April 2026 aggregate YoY","april_retro.csv","Newsletter 2026-05-13",None),
 ("april_spend","April 2026 median revenue change by spend band","april_rev_by_spend_band.csv","Newsletter 2026-05-13",None),
 ("april_rev_band","April 2026 YoY by revenue band","april_rev_band.csv","Newsletter 2026-05-13",None),
 ("april_aov","April 2026 YoY by AOV band","april_aov.csv","Newsletter 2026-05-13",None),
 ("jan2026","January 2026 benchmarks: median vs P75","jan2026_benchmarks.csv","Blog 2026-02-18",None),
 ("feb_size","February 2026 by company size","feb2026_size.csv","Blog 2026-03-13",None),
 ("amazon","Amazon Ads by spend tier, Feb 2026","amazon_feb2026.csv","Blog 2026-03-27",None),
 ("size_2025","2025 spend & revenue by company size","size_2025.csv","Blog 2026-02-04",None),
 ("verticals_2025","2025 median performance by vertical","verticals_2025.csv","Blog 2026-02-11",None),
 ("vertical_mix","Q1 2026 wallet share & creative volume by vertical","vertical_mix_q1_2026.csv","X 2026-06-05",None),
 ("ads_launched","Meta ads launched per month by spend level, 2025","fb_ads_launched_2025.csv","Blog 2026-02-18",None),
 ("emerging","Fastest-growing emerging platforms, H1 2026","emerging_platforms_h1.csv","X 2026-07-14",None),
 ("ai_search","AI share of organic search visits & revenue (read from chart)","ai_search_share_approx.csv","Newsletter 2026-08-13",None),
 ("creative","Creative volume & testing benchmarks","creative_benchmarks.csv","Newsletter + Blog, 2025-2026",None),
 ("events","Calendar events used on weekly charts","events.csv","Retail calendar",None),
 ("tiktok_cvr","TikTok 1-day click CVR (read from chart)","tiktok_cvr_approx.csv","Newsletter 2026-05-21",None),
 ("meta_earn","Meta quarterly ad impressions & price per ad","meta_earnings.csv","Meta earnings releases, Q1 2024 – Q3 2026",None),
 ("mo_tiers","Motion: creative volume & hit rate by spend tier","motion_tiers.csv","Motion / Runneth Creative Benchmarks 2026",None),
 ("mo_formats","Motion: visual formats by winners & hit rate","motion_visual_formats.csv","Motion / Runneth Creative Benchmarks 2026",None),
 ("mo_hooks","Motion: hooks & headlines by hit rate","motion_hooks.csv","Motion / Runneth Creative Benchmarks 2026",None),
 ("mo_assets","Motion: asset types by hit rate","motion_assets.csv","Motion / Runneth Creative Benchmarks 2026",None),
 ("mo_bfcm_hw","Motion: Health & Wellness BFCM 2025 over-index","motion_bfcm_hw.csv","Runneth BFCM 2026 planner",None),
 ("mo_ai","Motion: AI use by creative-strategy stage","motion_ai.csv","Thumbstop Pulse, Nov 2025",None),
 ("mo_trending","Motion: top 30 ads this week (weekly snapshots)","motion_trending.csv","motionapp.com/trending, weekly",None),
 ("tw_bfcm","Triple Whale BFCM 2025 weekend totals","tw_bfcm2025.csv","Triple Whale, Dec 2025",None),
 ("bfcm_live","BFCM 2026 live log","bfcm2026_live.csv","Scheduled update, 24 Nov – 2 Dec 2026",None),
 ("bfcm_sched","BFCM 2026: what lands when","bfcm2026_schedule.csv","Newsroom",None),
 ("q3_rev","Q3 2026 YoY by company revenue & percentile","q3_revenue_band.csv","X 2026-10-24",None),
 ("tw_weekly","Triple Whale benchmarks, weekly snapshots","tw_benchmarks_weekly.csv","benchmark.triplewhalelabs.com, weekly from 28 Oct 2026",None),
 ("haus_ch","Haus incrementality benchmarks by channel","haus_channels.csv","Haus research reports, 2025-2026",None),
 ("haus_ia","Meta Incremental Attribution vs standard (Haus)","haus_ia.csv","Haus / Olivia Kory, X, Jul & Oct 2026",None),
 ("haus_rep","Which Meta number tracks holdout lift (Haus)","haus_meta_reporting.csv","Haus, X, 9 Oct 2026",None),
 ("haus_7dc","7-day click purchases per 100 IA, monthly (Haus)","haus_7dc_per_ia.csv","Haus, X, 9 Oct 2026",None),
 ("haus_search","Google non-brand text vs shopping incrementality (Haus)","haus_search.csv","Haus, X, 28 Aug 2026",None),
 ("haus_cat","Meta catalog ads incrementality (Haus)","haus_catalog.csv","Haus, X, 25 & 28 Oct 2026",None),
 ("haus_textnow","TextNow YouTube geo test, cumulative lift (Haus)","haus_textnow.csv","Haus, X, 20 Aug 2026",None),
 ("haus_cw","Cyber Week 2025 delayed lift (Haus)","haus_cyberweek2025.csv","Haus report, 11 Dec 2025",None),
 ("haus_app","AppLovin beat rate by quarter (Haus)","haus_applovin.csv","Haus report, 18 Jun 2026",None),
 ("haus_sow","Spend share for brands live on AppLovin, Q4 2025 (Haus)","haus_sow_q4_2025.csv","Haus, X, 14 Jan 2026",None),
]
DATA={}
for k,t,fn,src,extra in REG:
    note,cols,rows=load(fn)
    if extra: note=(extra+' '+note).strip()
    DATA[k]=dict(title=t,file=fn,source=src,note=note,cols=cols,rows=rows)
tpl=open('template.html').read()
out=tpl.replace('/*__DATA__*/null',json.dumps(DATA,separators=(',',':'))).replace('/*__LIB__*/null',json.dumps(LIB,separators=(',',':')))
open('dtc-newsroom.html','w').write(out)
print(len(out))
# GitHub Pages: full document at index.html (site root)
open('index.html','w').write('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'+out+'\n</body></html>' if False else '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n</head>\n<body>\n'+out+'\n</body>\n</html>\n')
