import json,pathlib,urllib.request,urllib.parse,time,re,difflib,unicodedata
R=pathlib.Path('/tmp/scratch_gold/sol');v=json.loads((R/'metadata_matches.json').read_text());ds=json.loads((R/'dois_from_reports.json').read_text());hyper=json.loads((R/'report_hyperlinks.json').read_text())
def norm(s):return ' '.join(re.findall('[a-z0-9]+',unicodedata.normalize('NFKD',s.lower())))
for key,x in v.items():
 if x.get('match_score',0)>.88:continue
 doi=''
 opts=ds.get(key,[])
 for score,d,ctx in opts:
  if score>.85 and re.match(r'10\.(?:1177/095679|1038/s41562)',d) and not d.endswith('09567976231221573') and len(d)>25:doi=d;break
 if not doi:
  opts2=[u.split('doi.org/')[1]for u in hyper.get(key,[]) if 'doi.org/10.1177/095679' in u and not u.endswith('09567976231221573')]
  if len(opts2)==1:doi=opts2[0]
 p=R/f'metadata_slow/{key}.json';p.parent.mkdir(exist_ok=True)
 try:
  if p.exists():data=json.loads(p.read_text())
  else:
   time.sleep(1.4)
   u='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')if doi else 'https://api.crossref.org/works?rows=2&query.title='+urllib.parse.quote(x['query'])
   with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ReproCrowd-candidate-audit/1.0'}),timeout=25)as r:data=json.load(r)
   p.write_text(json.dumps(data))
  items=data['message'].get('items')if not doi else[data['message']]
  opts=[(difflib.SequenceMatcher(None,norm(x['query']),norm(a.get('title',[''])[0])).ratio(),a)for a in items];score,a=max(opts,key=lambda z:z[0])
  v[key]=dict(query=x['query'],match_score=score,title=a.get('title',[''])[0],doi=a['DOI'],date=a.get('published',{}).get('date-parts'),journal=a.get('container-title'),url=a.get('URL'))
  print(key,round(score,2),a['DOI'],flush=True)
 except Exception as e:
  print(key,str(e),flush=True)
  if '429' in str(e):break
 (R/'metadata_matches.json').write_text(json.dumps(v))
