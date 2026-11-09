"""Turn saved Triple Whale cohort JSON (notes/fetched/TW-API/<date>/<industry>__<band>.json) into rows for
data/tw_benchmarks_weekly.csv. Usage: python3 tools/tw_rows.py <date> [--append]
Skips cohorts with no data (rolled up / "No data") and snapshots already in the CSV. Added 9 Nov 2026."""
import json, os, sys, glob
METRICS = ['roas','cpa','cpm','cpc','ctr','cvr','aov','ncPercent','addToCartRate','discountRate']
CSV = 'data/tw_benchmarks_weekly.csv'
def g(x): return '' if x is None else f'{x:.5g}'
def rows(date):
    out = []
    for f in sorted(glob.glob(f'notes/fetched/TW-API/{date}/*.json')):
        j = json.load(open(f))
        if not j.get('total') or j.get('rolledUp'): continue
        c = j['cohort']; r = j['range']
        base = [date, r['start'], r['end'], c['industry'], c['gmvBand']]
        blocks = [('all', j['total'])] + [(b['channelId'], b) for b in j.get('byChannel') or []]
        for ch, b in blocks:
            for m in METRICS:
                v = (b.get('metrics') or {}).get(m)
                if not v: continue
                out.append(','.join(base + [ch, b.get('cohortSize', ''), m, g(v.get('p25')), g(v.get('median')), g(v.get('p75'))]))
    return out
if __name__ == '__main__':
    date = sys.argv[1]
    have = {l.split(',')[0] for l in open(CSV) if l[:2] == '20'}
    R = rows(date)
    if '--append' in sys.argv:
        if date in have: sys.exit(f'{date} already in {CSV}')
        with open(CSV, 'a') as f:
            txt = open(CSV).read()
            if not txt.endswith('\n'): f.write('\n')
            f.write('\n'.join(R) + '\n')
    print(f'{len(R)} rows for {date}')
