# Seeds data/headlines.json with the week of 2 to 8 Nov 2026 and the Northbeam BFCM guide deep dive.
# Written by the editor's desk on 6 Nov 2026. Every figure comes from the library entry named in `lib`.
# Later runs add items to the current week by editing data/headlines.json directly (see UPDATING.md).
import csv, json

rows = [r for r in csv.DictReader(l for l in open('data/mbi_new.csv') if not l.startswith('#'))
        if r['week_end'] == '2026-11-01']
idx = [[r['platform'], r['cpm'], r['ctr'], r['cpc'], r['cac'], r['cvr'], r['roas'], r['share'], r['share_delta']] for r in rows]

NB = 'https://themediabuyer.northbeam.io/p/northbeam-s-black-friday-survival-guide-2026-edition'

items = [
 dict(id='nb-bfguide', date='2026-11-05', pub='Northbeam', impact=3, topics=['BFCM', 'Meta'], lib='mb-bfguide26',
      headline="Northbeam's Black Friday rulebook: four check-ins a day, 20% bumps, reset every night",
      take="Bryan Bumgardner's survival guide turns Northbeam's client playbook into rules you can set up now. Cap every budget raise at 20%, review four times a day from 25 Nov to 1 Dec, and use a 12:01am rule to reopen each campaign at 30% above the previous day's start.",
      figs=['CPMs +20% to 35% over last year\'s big weekend', 'Budget bumps capped at 20%', 'Overnight reset: +30% on prior open'],
      why="It's the most specific BFCM operating plan any source has published this year. Our deep dive breaks down all eight rules and where we'd bend them.",
      url=NB, feature='nb-bf-guide-26'),
 dict(id='nb-index-1nov', date='2026-11-05', pub='Northbeam', impact=3, topics=['Meta', 'Google', 'Benchmarks'], lib='mb-weekly',
      headline="Meta conversion rate falls for a third straight week as CPMs go flat",
      take="In Northbeam's Media Buyer Index for the week ending 1 Nov, Meta CPM barely moved (-0.11%) and CPC fell 4.87%, but CVR dropped 5.05%. That follows falls of 1.63% and 2.88% in the two weeks before. Google's budget share rose to 18.00% (+0.74 pts) as Meta's slipped to 55.25%.",
      figs=['Meta CVR -5.05% WoW', 'Meta CTR +4.86% WoW', 'Google share 18.00%'],
      why="Cheaper clicks aren't turning into orders. Conversion, not cost, is the number to defend going into the sale.",
      url=NB, to='#nb-channels'),
 dict(id='nb-bb-cvr', date='2026-11-05', pub='Northbeam', impact=2, topics=['Meta', 'Measurement'], lib='x-bb-cvr-lows',
      headline="Bumgardner: Meta conversion rates at record lows, ROAS better than ever",
      take="Northbeam's Bryan Bumgardner reads about $6B of spend across 1,000 customers and says Meta now optimises toward clicks. On his read, landing pages and the new-customer signals you send back to Meta matter more than ever.",
      figs=['$6B spend', '1,000 Northbeam customers'],
      why="If ROAS looks fine while conversion falls, the site is where the money leaks. Fix the landing page before you raise bids.",
      url='https://x.com/BryanBumgardner/status/2118318914426081553'),
 dict(id='ctc-ondevice', date='2026-11-02', pub='Common Thread', impact=3, topics=['Meta', 'Measurement', 'BFCM'], lib='ctc-meta-ondevice',
      headline="Meta switches on on-device conversion measurement for every account on 12 Nov",
      take="Common Thread cites early Meta tests with up to 15% more attributed purchases for Advantage+ Sales. The setting runs alongside the Pixel and Conversions API, and Common Thread advises no structural changes for two weeks after it turns on.",
      figs=['Live 12 Nov', 'Up to +15% attributed purchases'],
      why="Meta-reported ROAS will step up mid-month for reasons that have nothing to do with your ads. Take a Shopify baseline this week.",
      url='https://commonthreadco.com/blogs/coachs-corner/meta-is-adding-on-device-pixel-measurement-on-november-12-what-every-ecommerce-brand-must-check-before-bfcm'),
 dict(id='hw-bf-budget', date='2026-11-04', pub='Curtis Howland', impact=3, topics=['BFCM', 'Meta'], lib='li-howland-20261104',
      headline="Howland's BFCM budget curve: 150 to 200% on Black Friday and Cyber Monday",
      take="Answering questions from 8 to 9 figure DTC brands, Curtis Howland lays out a daily budget shape, as a share of BFCM daily budget: 100% Monday to Wednesday, 120% Thanksgiving, 150 to 200% Black Friday, 130% over the weekend, 150 to 200% Cyber Monday, then 80% the Tuesday after. Last year Black Friday day-one CPMs in his accounts ran 45% above the week before.",
      figs=['BF day-1 CPMs +45% vs prior week', 'Black Friday 150-200%', 'Thanksgiving 120%'],
      why="Read it alongside Northbeam's rules. Howland sets each day's budget; Northbeam's check-ins steer spend within the day.",
      url='https://www.linkedin.com/feed/update/urn:li:activity:7523753426166542336/'),
 dict(id='dtc-promo-mode', date='2026-11-05', pub='Direct to Consumer', impact=3, topics=['Google', 'BFCM'], lib='dtcnl-20261105',
      headline="Google's Promotion Mode lets Search and PMax drop tROAS for 3 to 14 day sales",
      take="It's in open beta for eligible Search and Performance Max campaigns. The lower target applies only while the sale runs.",
      figs=['Sales of 3 to 14 days', 'Search and PMax'],
      why="It's the cleanest way to let Google bid harder during a sale without editing your evergreen targets. Set your post-discount floor ROAS before you switch it on.",
      url='https://www.directtoconsumer.co/newsletter/google-promotion-mode-ai-shopping-bfcm-cro'),
 dict(id='hw-68245', date='2026-11-02', pub='Curtis Howland', impact=2, topics=['BFCM', 'Creative'], lib='howland-ss-68245-black-friday-ads-taken-apart',
      headline="68,245 Black Friday ads: the median brand launched 13 days out, at 50% off",
      take="Howland's Meta Ad Library pull covers 6,281 brands. Percent off led 66.2% of ads, 50% was the most common number, and 64% of brands kept the same discount into Black Friday week.",
      figs=['Median first ad 13 days out', '66.2% led with % off', '50% median discount'],
      why="If your Black Friday creative isn't live by mid-November, you're behind the median brand.",
      url='https://newsletter.curtishowland.com/p/68245-black-friday-ads-taken-apart', to='#hw-bf'),
 dict(id='dtc-kiel', date='2026-11-03', pub='Direct to Consumer', impact=2, topics=['Meta', 'BFCM'], lib='dtcnl-20261103',
      headline="Scaling into Q4 is working: biggest accounts +21% spend, CPA down 3%",
      take="Phil Kiel says his biggest accounts raised spend 21% from September to October while CPA fell 3% and purchases rose 23%.",
      figs=['Spend +21%', 'CPA -3%', 'Purchases +23%'],
      why="It counters the 'CPMs are up, so hold back' instinct. Spend scaled into the season and efficiency held.",
      url='https://www.directtoconsumer.co/newsletter/bfcm-audiences-shopify-ai-meta-scaling'),
 dict(id='ctc-ai-creative', date='2026-11-02', pub='Common Thread', impact=2, topics=['Meta', 'Creative', 'AI'], lib='ctc-meta-image-animation',
      headline="Meta's AI video tools are on by default in new campaigns",
      take="Image Animation turns static product photos into short video ads. It's on by default in new campaigns, alongside Video Expansion and Catalog-to-Video.",
      figs=['3 tools on by default'],
      why="Check what's switched on, ad by ad, before the sale. Northbeam flags a related ad-level setting that can drift prospecting toward retargeting.",
      url='https://commonthreadco.com/blogs/coachs-corner/meta-just-launched-ai-video-ads-from-static-images-and-your-legal-liability-deadline-is-november-20'),
 dict(id='ctc-terms', date='2026-11-03', pub='Common Thread', impact=2, topics=['Meta'], lib='ctc-meta-terms-delay',
      headline="Meta delays its new ad terms indefinitely after EU and UK inquiries",
      take="The updated Commercial and Self-Serve Ad Terms, already pushed back to 20 Nov, are now on hold with no new date. The March 2024 terms still apply.",
      figs=['No new date', 'March 2024 terms stand'],
      why="That removes a legal deadline from the middle of BFCM. It doesn't remove the need to review AI-made creative.",
      url='https://commonthreadco.com/blogs/coachs-corner/metas-new-ad-terms-are-now-indefinitely-delayed-what-every-ecommerce-brand-must-know'),
 dict(id='ctc-abs', date='2026-11-03', pub='Common Thread', impact=2, topics=['Google', 'Measurement'], lib='ctc-google-abs',
      headline="Google adds free 'Attributed Branded Searches' for Demand Gen and YouTube",
      take="Google now counts brand searches on Google or YouTube that follow a Demand Gen or YouTube ad, with no pixel setup. Find it under Goals > Summary > Consideration.",
      figs=['Free', 'Default 30-day click, 1-day view'],
      why="It's a cheap read on whether upper-funnel video is creating demand you then harvest in Search.",
      url='https://commonthreadco.com/blogs/coachs-corner/google-just-launched-attributed-branded-searches-what-ecommerce-brands-must-enable-before-bfcm'),
 dict(id='ctc-pmax-income', date='2026-11-02', pub='Common Thread', impact=2, topics=['Google'], lib='ctc-google-pmax-income',
      headline="PMax gets household income exclusions, but don't exclude 'Unknown' before BFCM",
      take="There are seven tiers, applied at campaign level. Common Thread advises adding one tier at a time, seven days apart.",
      figs=['7 income tiers'],
      why="It's a real targeting lever, but changing it mid-season risks resetting learning. Test it in December.",
      url='https://commonthreadco.com/blogs/coachs-corner/google-just-added-household-income-exclusions-to-performance-max-what-ecommerce-brands-must-configure-before-bfcm'),
 dict(id='haus-chatgpt', date='2026-11-04', pub='Haus', impact=2, topics=['AI', 'Measurement'], lib='haus-x-chatgpt-ads',
      headline="A paid ChatGPT visit earned $0.89 against $2.45 for a paid Google search visit",
      take="Olivia Kory flags a working paper covering 1,898 shops and $16B in annual sales, using the ad-free EU as a control. She cautions that the search-versus-ChatGPT comparison rests on last click.",
      figs=['$0.89 vs $2.45 per visit', '1,898 shops'],
      why="It's early evidence to hold off on ChatGPT ads as a BFCM line item.",
      url='https://x.com/oliviaakory/status/2117992986936041673'),
 dict(id='shopify-q3', date='2026-11-03', pub='Shopify', impact=2, topics=['Benchmarks', 'Measurement'], lib='shopify-q3-26',
      headline="Shopify grows revenue 32% and admits it paused US spend to test incrementality",
      take="Q3 GMV was $119B and Q4 revenue is guided to low-thirties growth. On the call, the CFO said slightly slower Q3 growth came from pausing spend in some channels and regions for a couple of weeks. Haus's Olivia Kory called it the definition of optimising for the long term.",
      figs=['Revenue +32%', 'GMV $119B'],
      why="If a company Shopify's size will take a hit to test incrementality, a geo holdout is a defensible ask for January.",
      url='https://www.shopify.com/news/shopify-q3-2026-financial-results'),
 dict(id='hw-ltv', date='2026-11-05', pub='Curtis Howland', impact=2, topics=['Measurement'], lib='li-howland-20261105',
      headline="Before you buy an LTV model, check whether day-3 revenue already predicts day-90",
      take="Rank customers by day-3 and day-90 revenue, then correlate the two rankings. Around 70% means you're probably overbidding on low-LTV customers; 85% or more means day-3 value is fine to bid on.",
      figs=['70% vs 85% thresholds'],
      why="It's a free test worth running on your BFCM cohort in February.",
      url='https://www.linkedin.com/feed/update/urn:li:activity:7524115882311073792/'),
 dict(id='snap-q3', date='2026-11-06', pub='Direct to Consumer', impact=1, topics=['Benchmarks'], lib='dtcnl-20261106',
      headline="Snapchat's North American daily users fall 6% to 92 million",
      take="Snap's Q3 revenue rose 14% to $1.72B, but ad revenue grew only 4%. Worldwide daily users rose 4% to 495M.",
      figs=['NA DAU -6%', 'Ad revenue +4%'],
      why="If Snap is in your mix, check reach and CAC by market before adding holiday budget.",
      url='https://www.directtoconsumer.co/newsletter/google-profit-tracking-snapchat-trends-chappywrap-email-cro'),
 dict(id='graphite-ai', date='2026-11-06', pub='Graphite', impact=1, topics=['AI'], lib='graphite-state-genai-2026',
      headline="AI referral traffic up 92% a year; 64% of Google searches now show AI Overviews",
      take="ChatGPT sends 60% of AI referrals, Gemini 14% and Claude 10%. 86% of AI usage worldwide happens in-app.",
      figs=['AI referrals +92% YoY', 'AI Overviews on 64% of searches'],
      why="It's still small next to search, but it compounds. Make sure your product pages read well to an assistant.",
      url='https://graphite.io/research/the-state-of-genai'),
 dict(id='eu-fee', date='2026-11-02', pub='Direct to Consumer', impact=1, topics=['BFCM'], lib='dtcnl-20261102',
      headline="The EU adds a €2 per-item handling fee on low-value parcels from outside the bloc",
      take="It started on 1 Nov, on top of the €3 customs duty.",
      figs=['€2 per item', 'Plus €3 duty'],
      why="If you ship into the EU from outside it, re-check holiday margins and free-shipping thresholds.",
      url='https://www.directtoconsumer.co/newsletter/eu-shipping-fees-meta-audiences-ai-creative'),
 dict(id='amazon-reviews', date='2026-11-02', pub='Common Thread', impact=1, topics=['Amazon'], lib='ctc-amazon-review-requests',
      headline="Amazon opens paid Review Requests ads to eligible US sellers",
      take="The ads target verified buyers at least 7 days after delivery, bid on CPC. Common Thread says early testing showed 3x more reviews per product.",
      figs=['3x reviews per product'],
      why="It's a cheap way to build review volume on hero products before the sale.",
      url='https://commonthreadco.com/blogs/coachs-corner/amazon-review-requests-ads-are-now-in-open-beta-what-every-ecommerce-brand-must-do-before-bfcm'),
 dict(id='rn-2nov', date='2026-11-02', pub='Runneth', impact=1, topics=['Creative'], lib='rn-trending',
      headline="Runneth's weekly top 120: 57 videos, 53 images and 10 carousels",
      take="These are the most-saved ads this week across apparel, sports and fitness, retail and accessories.",
      figs=['120 ads', '57 videos'],
      why="It's the swipe file for what's working in our categories right now.",
      url='https://motionapp.com/trending/', to='#mo-trend'),
]

# ---- v2 (Ryan, 6 Nov): Graphite-style report sections. Each item gets a short section title (label),
# an annotated chart or a stat card, and drill-down key points + a verbatim quote from the library.
import runpy
_g = runpy.run_path('library.py')
LIB = {}
for _v in _g.values():
    if isinstance(_v, list) and _v and isinstance(_v[0], dict) and 'pub' in _v[0]:
        for _e in _v:
            if isinstance(_e, dict) and 'id' in _e:
                LIB.setdefault(_e['id'], _e)
mbi = [r for r in csv.DictReader(l for l in open('data/mbi_new.csv') if not l.startswith('#'))]
def series(plat, col, n=8):
    rr = sorted((r for r in mbi if r['platform'] == plat and r[col] != ''), key=lambda r: r['week_end'])[-n:]
    return [r['week_end'] for r in rr], [float(r[col]) for r in rr]
wk, cvr = series('Meta', 'cvr'); _, ctr = series('Meta', 'ctr'); _, roas = series('Meta', 'roas')
_, msh = series('Meta', 'share'); _, gsh = series('Google', 'share')
wkl = ['w/e ' + __import__('datetime').date.fromisoformat(w).strftime('%-d %b') for w in wk]
hbf = json.load(open('data/howland_bf_study.json'))
peak = max(range(len(hbf['daily'])), key=lambda k: hbf['daily'][k])
off = hbf['offers']
NBSRC = 'Northbeam, The Media Buyer, 5 Nov 2026'
IDXSRC = "Northbeam Media Buyer Index, week-over-week % change, as printed in each Thursday issue"

V2 = {
 'nb-bfguide': dict(label='The Black Friday rulebook', chart=dict(title="Northbeam's own budget example", views=[dict(label='Reset example', type='bar', unit='$', labels=['Day 1 open', 'Day 1 by evening', 'Day 2 open'], series=[dict(name='Daily budget', data=[10000, 20000, 13000], color='amber')], annos=[dict(i=1, text='Scaled in 20% steps'), dict(i=2, text='12:01am rule: +30% on prior open')])]), src=NBSRC + ", worked example in the guide"),
 'nb-index-1nov': dict(label='Meta conversion', chart=dict(title='Meta, week over week', views=[
     dict(label='CVR vs CTR', type='line', unit='%wow', labels=wkl, series=[dict(name='Meta CVR', data=cvr, color='down'), dict(name='Meta CTR', data=ctr, color='blue')], annos=[dict(s=0, i=len(cvr) - 1, text='CVR %+.2f%%: third straight fall' % cvr[-1])]),
     dict(label='Budget share', type='line', unit='%', labels=wkl, series=[dict(name='Meta share', data=msh, color='meta'), dict(name='Google share', data=gsh, color='google')], annos=[dict(s=1, i=len(gsh) - 1, text='Google %.2f%%' % gsh[-1])])]), src=IDXSRC),
 'nb-bb-cvr': dict(label='ROAS up, conversion down', chart=dict(title='Meta ROAS vs conversion rate, week over week', views=[dict(label='ROAS vs CVR', type='line', unit='%wow', labels=wkl, series=[dict(name='Meta ROAS', data=roas, color='up'), dict(name='Meta CVR', data=cvr, color='down')], annos=[dict(s=0, i=len(roas) - 1, text='ROAS up %d weeks running' % next((k for k in range(len(roas)) if roas[-1-k] <= 0), len(roas)))])]), src=IDXSRC + "; the claim is Bryan Bumgardner's on X, 5 Nov 2026"),
 'ctc-ondevice': dict(label='Measurement shift', stat=dict(value='+15%', label='more attributed purchases, up to', sub='Meta tests for Advantage+ Sales, cited by Common Thread. Switches on for every account on 12 Nov.'), src='Common Thread, 2 Nov 2026, citing Meta'),
 'hw-bf-budget': dict(label='The budget curve', chart=dict(title='Daily budget as a share of your BFCM daily budget', views=[dict(label='Budget curve', type='float', unit='%', labels=['Mon-Wed before', 'Thanksgiving', 'Black Friday', 'Weekend', 'Cyber Monday', 'Tuesday after'], series=[dict(name='Share of daily budget', data=[[100, 100], [120, 120], [150, 200], [130, 130], [150, 200], [80, 80]], color='amber')], annos=[dict(i=2, text='150 to 200%'), dict(i=4, text='150 to 200%')])]), src='Curtis Howland on LinkedIn, 4 Nov 2026'),
 'dtc-promo-mode': dict(label='Google sale bidding', stat=dict(value='3-14', label='day sales can run on a lower tROAS', sub='Promotion Mode, open beta, eligible Search and Performance Max campaigns.'), src='Direct to Consumer newsletter, 5 Nov 2026'),
 'hw-68245': dict(label='When brands launch', chart=dict(title='New Black Friday ads launched per day, 2025', views=[
     dict(label='Launch curve', type='line', unit='', labels=hbf['labels'], series=[dict(name='New ads', data=hbf['daily'], color='amber')], annos=[dict(i=peak, text='%s: %s new ads' % (hbf['labels'][peak], format(hbf['daily'][peak], ',')))]),
     dict(label='Lead offer', type='hbar', unit='%', labels=[o[0] for o in off], series=[dict(name='Share of ads', data=[float(o[1].rstrip('%')) for o in off], color='amber')], annos=[dict(i=0, text='Percent off leads two in three')])]), src="Curtis Howland, Field study Nº03 (Meta Ad Library, 15 Oct to 7 Dec 2025). Lead-offer shares cover 47,013 English ads."),
 'dtc-kiel': dict(label='Scaling into Q4', chart=dict(title='Biggest accounts, September to October', views=[dict(label='Sep to Oct', type='bar', unit='%', labels=['Spend', 'CPA', 'Purchases'], series=[dict(name='Change', data=[21, -3, 23], color='sign')], annos=[dict(i=1, text='CPA fell as spend rose')])]), src='Phil Kiel, via Direct to Consumer newsletter, 3 Nov 2026'),
 'ctc-ai-creative': dict(label='AI creative defaults', stat=dict(value='3', label='AI creative tools on by default', sub='Image Animation, Video Expansion and Catalog-to-Video, in new campaigns from 2 Nov.'), src='Common Thread, 2 Nov 2026'),
 'ctc-terms': dict(label='Meta ad terms', stat=dict(value='On hold', label='no new date', sub='March 2024 terms still apply after EU and UK inquiries.'), src='Common Thread, 3 Nov 2026'),
 'ctc-abs': dict(label='Branded search lift', stat=dict(value='Free', label='brand-search count after Demand Gen and YouTube ads', sub='Goals > Summary > Consideration. Default window 30-day click, 1-day view.'), src='Common Thread, 3 Nov 2026'),
 'ctc-pmax-income': dict(label='PMax income tiers', stat=dict(value='7', label='household income tiers in PMax', sub="Add one at a time, 7 days apart. Don't exclude Unknown before BFCM."), src='Common Thread, 2 Nov 2026'),
 'haus-chatgpt': dict(label='ChatGPT ads', chart=dict(title='Revenue per paid visit, US', views=[dict(label='Per visit', type='bar', unit='$', labels=['Paid ChatGPT visit', 'Paid Google search visit'], series=[dict(name='Revenue per visit', data=[0.89, 2.45], color='amber')], annos=[dict(i=0, text='$0.89, about a third of search')])]), src='Schulze and Kaiser working paper, flagged by Olivia Kory (Haus) on X, 4 Nov 2026. Last-click comparison.'),
 'shopify-q3': dict(label='Shopify Q3', stat=dict(value='+32%', label='Q3 revenue growth', sub='GMV $119B. Q4 guided to low-thirties growth. The CFO says US spend was paused in some channels and regions to test incrementality.'), src='Shopify Q3 2026 release, 3 Nov 2026'),
 'hw-ltv': dict(label='LTV shortcut', stat=dict(value='85%', label='rank correlation where day-3 revenue is good enough', sub='Around 70% suggests you are overbidding on low-LTV customers.'), src='Curtis Howland on LinkedIn, 5 Nov 2026'),
 'snap-q3': dict(label='Snapchat users', chart=dict(title='Snapchat daily users, year over year, Q3 2026', views=[dict(label='DAU change', type='bar', unit='%', labels=['Worldwide (495M)', 'North America (92M)'], series=[dict(name='YoY change', data=[4, -6], color='sign')], annos=[dict(i=1, text='North America -6%')])]), src='Snap Q3 2026, via Direct to Consumer newsletter, 6 Nov 2026'),
 'graphite-ai': dict(label='AI referrals', chart=dict(title='Share of AI referral traffic, worldwide', views=[dict(label='Referral share', type='hbar', unit='%', labels=['ChatGPT', 'Gemini', 'Claude'], series=[dict(name='Share of AI referrals', data=[60, 14, 10], color='amber')], annos=[dict(i=0, text='Referrals +92% YoY')])]), src='Graphite, The State of Gen AI, Nov 2026'),
 'eu-fee': dict(label='EU parcel fee', stat=dict(value='€2', label='per item, on top of €3 customs duty', sub='Low-value parcels from outside the EU, from 1 Nov.'), src='Direct to Consumer newsletter, 2 Nov 2026'),
 'amazon-reviews': dict(label='Amazon reviews', stat=dict(value='3x', label='reviews per product in early testing', sub='Paid Review Requests ads, verified buyers, 7+ days after delivery, CPC.'), src='Common Thread, 2 Nov 2026'),
 'rn-2nov': dict(label='Trending creative', chart=dict(title="This week's 120 most-saved ads, by format", views=[dict(label='Formats', type='bar', unit='', labels=['Video', 'Image', 'Carousel'], series=[dict(name='Ads', data=[57, 53, 10], color='amber')], annos=[dict(i=0, text='Video edges images')])]), src='Runneth Weekly Trending Ads, week of 2 Nov 2026'),
}
POINTS = {'nb-index-1nov': LIB['mb-bfguide26']['stats'][:2]}
for it in items:
    v = V2.get(it['id'], {})
    it.update(v)
    e = LIB.get(it['lib'], {})
    it['points'] = POINTS.get(it['id'], [x for x in e.get('stats', [])][:6])
    q = [] if it['id'] in POINTS else e.get('q', [])
    it['quote'] = q[0] if q else ''
    it['src'] = it.get('src') or it['pub']
missing = [it['id'] for it in items if 'chart' not in it and 'stat' not in it]
assert not missing, missing

feature = dict(
 id='nb-bf-guide-26', date='2026-11-06', pub='Northbeam',
 kicker="Deep dive · Northbeam · BFCM",
 title="Northbeam's Black Friday playbook, taken apart",
 dek="Bryan Bumgardner's survival guide boils Northbeam's client work down to one discipline: check more often, bump in small steps, and reset every night. Here's what it says, what it's really telling you, what to do about it, and where we'd push back.",
 byline="Newsroom analysis of Northbeam's Black Friday Survival Guide: 2026 Edition (The Media Buyer, 5 Nov 2026), read with the same week's index and this week's other BFCM sources.",
 url=NB,
 kpis=[['Big-weekend CPM spike last year', '+20-35%', 'Northbeam, BFCM 2025', 'down'],
       ['Max budget bump', '20%', 'per check-in', 'amber'],
       ['Overnight reset', '+30%', 'on the prior day\'s open', 'amber'],
       ['Check-ins a day', '4', '25 Nov to 1 Dec', 'text']],
 quote=["Last November we saw CPMs spike 20% to 35% during the big weekend.", "Bryan Bumgardner, Northbeam"],
 headlines=[
  ['Check in four times a day, not two or three', "Normally an account under $100k a day gets checked two or three times. For BFCM Northbeam wants a 9am read against the trailing seven days, a 2pm round of calls, a 7pm push and a final pass before bed. A slow morning isn't a verdict: a campaign under target for six to eight hours but on target over seven days gets left until the next check-in."],
  ['Never raise a budget more than 20% at a time', "Northbeam's 'spend S-curve': on Meta, a budget change makes spend spike straight away and then taper off. Several small raises give steadier hourly delivery and spread the risk through the day. Northbeam calls the method 'scale and surf'."],
  ['Reset every budget at 12:01am', "A rule reopens each campaign at 30% above the previous day's opening budget, not wherever it finished the night. In Northbeam's example, a campaign that opened at $10,000 and reached $20,000 by evening reopens the next day at $13,000. It guards against runaway spend, and mornings are quieter anyway while email and SMS land."],
  ['Expect cost caps and bid caps to stall', "CPMs spiked 20% to 35% over last year's big weekend, and Bumgardner thinks this will be the most expensive BFCM yet. When a capped campaign can't spend, copy it into a lowest-cost twin. When one cap campaign's CPMs run away, move it to lowest cost with broader targeting."],
  ["Leave evergreen cost caps alone", "Put the extra sale spend in separate max-conversion campaigns and switch those off when the sale ends. One Northbeam client cut its product-level cost caps after the weekend and had to rebuild performance from scratch."],
  ["Judge today's spend on today's results", "During BFCM, measure spend on an accrual basis. Build one view per platform with blended revenue and blended cost per order by campaign, ad set and ad, showing today against the trailing three to seven days. Keep cash numbers for overall business health. It only works if your conversion-lag multipliers are already set."],
  ["Drop 'up to 50% off'", "Pick one discount number, say it plainly in the caption, and put the call to action in the video. Northbeam says 'up to' is hurting click-through and reads like a credit-card mailer. BFCM creative captures demand you built during the year; it doesn't create it."],
  ["Audit Meta's Product Browsing AI enhancement", "This ad-level setting can turn statics and video into product ads, which tends to pull prospecting toward retargeting. Turn it on or off on purpose, on every prospecting ad."],
 ],
 analysis=[
  "The guide is about tempo more than tactics. The 20% step is the same one Northbeam recommends all year. What changes is how often you take it (up to three times a day) and the nightly reset. Put together, the rules set a ceiling. Three 20% raises compound to about 1.73 times the morning budget by bedtime (our arithmetic). The 12:01 rule then pulls the next morning back to 1.3 times the previous opening budget. Left on autopilot, no campaign's opening budget grows faster than 30% a day.",
  "Read it next to the numbers in the same issue. In the week ending 1 Nov, Meta CPM was flat (-0.11%) but conversion rate fell 5.05%, its third straight weekly decline, and Bumgardner says Meta conversion rates are at record lows. That's why the guide builds its cockpit on blended revenue and new-customer cost per order rather than in-platform ROAS. When clicks get cheaper but convert worse, platform ROAS can hold up while the business pays more for each customer.",
  "The cost-cap warning has independent support. Curtis Howland says Black Friday day-one CPMs ran 45% above the week before in his accounts last year. Northbeam's weekly Meta CPM chart already runs about 24% above last year. A cap set on October costs is likely to stall over the weekend, which is exactly the case the lowest-cost twin is there for.",
  "One thing the guide doesn't mention: Meta switches on on-device conversion measurement for every account on 12 Nov. Common Thread, citing Meta, says it adds up to 15% more attributed purchases. So in-platform numbers this BFCM won't compare cleanly with last year's, and a blended cockpit is the only stable yardstick.",
  "The creative advice matches the data. Howland's study of 68,245 Black Friday ads found 50% was the median discount, 66.2% of ads led with percent off, and 64% of brands kept the same number into Black Friday week. Northbeam's 'pick one number and say it plainly' is what most brands already do. Removing 'up to' is the cheap win.",
 ],
 actions=[
  ['By 11 Nov', "Take a blended baseline before Meta's on-device measurement changes the numbers: Shopify revenue over total spend, and new-customer CAC, for the trailing 7, 14 and 28 days."],
  ['By 18 Nov', "Build the cockpit: blended revenue and cost per order by campaign, ad set and ad, today against the trailing 7 days. Agree the conversion-lag multipliers you'll apply at the 9am read."],
  ['By 18 Nov', "Split your structure. Evergreen cost caps stay untouched until December; the sale budget goes into separate max-conversion campaigns you can switch off on 2 Dec."],
  ['By 20 Nov', "For every cap campaign you rely on, build a lowest-cost twin and leave it paused, ready to launch the moment the cap stalls."],
  ['By 20 Nov', "Write the 12:01am reset rule (+30% on the prior day's opening budget) in Meta's automated rules and trial it on a low-stakes campaign first."],
  ['By 20 Nov', "Audit Product Browsing and Advantage+ Creative enhancements on every prospecting ad, and record what's on and why."],
  ['Creative', "Use one discount number, written in the caption, with no 'up to'. Get it live before the median brand's launch, 13 days out."],
  ['25 Nov to 1 Dec', "Staff the 9am, 2pm, 7pm and late check-ins with a shared handoff doc. Set each day's budget from Howland's curve (Thanksgiving 120%, Black Friday 150 to 200%, weekend 130%, Cyber Monday 150 to 200%), then use Northbeam's 20% steps to steer within the day."],
 ],
 pushback=[
  ["The 30% reset can starve a breakout day", "Howland's accounts run Black Friday and Cyber Monday at 150 to 200% of daily budget. A strict 30% overnight cap won't get you there from Thanksgiving's open. Plan to override the reset on those two mornings rather than let the rule set your ceiling."],
  ["Four check-ins assume a team", "If you're running accounts on your own, automate the steps instead of skipping them: rules for the 20% raises on hitting target and for the 12:01 reset. Keep your own reviews for 9am and 7pm."],
  ["The S-curve is asserted, not shown", "Northbeam bases it on a decade of observation but publishes no chart. Treat it as strong practitioner experience, and check your own hourly spend after a budget change this week."],
  ["'Most expensive BFCM ever' is a forecast", "It's Bumgardner's opinion. Right now the index shows Meta CPM flat week to week, and the gap that matters is year on year (about +24%). Plan for the spike; don't assume it."],
  ["Accrual reads need lag you trust", "Without conversion-lag multipliers, every 9am read will look worse than it really is, and the 'don't panic' rule does all the work. If you don't have multipliers yet, take them from last year's BFCM conversion timing this week."],
 ],
 checklist=["Dashboard: blended revenue, new-customer revenue and CAC per campaign, today against trailing 7 days",
            "12:01am budget reset rules written and tested",
            "Four check-ins a day booked from 25 Nov to 1 Dec, with a handoff doc",
            "Evergreen ads and cost caps left on and untouched",
            "Lowest-cost twins ready for every cap campaign",
            "Auto-DPA and Product Browsing setting checked on every prospecting ad"],
 index=dict(week='w/e 1 Nov 2026', cols=['Platform', 'CPM', 'CTR', 'CPC', 'nCAC', 'CVR', 'ROAS', 'Share', 'Share Δ'], rows=idx,
            note="Week-over-week % change, budget share % and share change (pts), as printed in the same issue. nCAC = new-customer CAC."),
 related=[['#nb-channels', 'Northbeam channel tracker'], ['#hw-bf', "Howland's Black Friday ad study"], ['#bfcm', 'BFCM desk']],
)

week = dict(id='2026-11-02', start='2026-11-02', end='2026-11-08',
            title="Meta's prices pause, its conversions don't",
            dek="Northbeam publishes the most detailed Black Friday rulebook of the season while its own index shows Meta conversion rate falling for a third straight week. Meanwhile, Meta and Google both change what gets measured, three weeks before the sale.",
            items=items)

json.dump(dict(weeks=[week], features=[feature]), open('data/headlines.json', 'w'), ensure_ascii=False)
print('headlines.json:', len(items), 'items,', len(idx), 'index rows')
