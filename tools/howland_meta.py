"""Build data/howland_meta_charts.json: Curtis Howland's Meta-ads charts, transcribed from his
newsletter and LinkedIn images (see notes in each chart), grouped into chapters for the desk."""
import json,sys
A=json.load(open(sys.argv[1]))
CH=[
 ('volume','Volume is the strategy','Launch more ads than feels sensible: winners are rare and spend piles onto a handful of them.',
  [(18,{'ds':[0]}),(22,{'ds':[0,1]}),(28,{'ds':[0]}),(19,{}),(120,{'y2':[2]}),(96,{'ds':[0,1]}),(124,{'ds':[0,1],'stack':True}),(112,{})]),
 ('cutscale','Let the numbers cut and scale','Judge each ad against a line that tightens as spend grows, not on a gut call at $200.',
  [(7,{'logx':True}),(110,{'ds':[1,3,4],'logx':True}),(37,{}),(54,{'ds':[0,1,2,3,4],'logx':True}),(87,{'y2':[1,2]})]),
 ('measure','Meta\'s number is one opinion','Click windows, view-through and last click each tell a different story. He checks them against surveys and new-customer CPA.',
  [(89,{}),(38,{}),(105,{'stack':True}),(55,{}),(34,{}),(73,{}),(5,{})]),
 ('spend','Spend until the next dollar stops paying','Blended ROAS hides the point where the marginal dollar falls below break-even.',
  [(69,{}),(76,{'ds':[0,1,2]}),(59,{})]),
 ('bfcm','Black Friday on Meta','From his pull of 68,245 Black Friday 2025 ads, plus how he ramps CAC into the sale.',
  [(0,{}),(1,{}),(2,{}),(3,{}),(56,{}),(48,{})]),
 ('cpm','What an impression is worth','CPM is an input. Compare it inside a channel, and judge every channel on cost per outcome.',
  [(49,{'float':True,'logx':True}),(15,{'ds':[0],'logx':True})]),
]
out=[]
for cid,h,dek,items in CH:
  charts=[]
  for i,o in items:
    a=A[i];c=dict(a['chart']);ds=c['datasets']
    if 'ds' in o: ds=[ds[k] for k in o['ds']]
    clean=[]
    for d in ds:
      dd=[]
      for v in d.get('data') or []:
        if isinstance(v,(int,float)) or v is None: dd.append(v)
        elif isinstance(v,dict): dd.append({k:v[k] for k in ('x','y','r','label') if k in v})
        else: dd.append(None)
      clean.append({'label':d['label'],'role':d.get('role','bars'),'data':dd})
    charts.append({'id':'hm%d'%i,'title':a['title'],'message':a.get('message',''),'type':c.get('type'),'labels':c.get('labels') or [],
      'datasets':clean,'x':c.get('x_label',''),'y':c.get('y_label',''),'units':c.get('units',''),'approx':bool(c.get('approx')),
      'notes':c.get('notes',''),'annotations':c.get('annotations') or [],'stats':a.get('stats') or [],'url':a['url'],'date':a['date'],
      'src':'Newsletter' if a['source']=='newsletter' else 'LinkedIn','opt':o})
  out.append({'id':cid,'h':h,'dek':dek,'charts':charts})
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,separators=(',',':'))
print(sum(len(c['charts']) for c in out),'charts')
