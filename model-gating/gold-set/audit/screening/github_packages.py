import pathlib,json,urllib.request,re,time
R=pathlib.Path('/tmp/scratch_gold/sol');pk=json.loads((R/'package_map.json').read_text());pk.update({'mepbv':['https://github.com/grossmania/Forecasting-Tournament/tree/32cfd57c635d08a54a2eff8f735382c3c16336ac'],'4mtga':['https://github.com/nivlab/sciops']});(R/'package_map.json').write_text(json.dumps(pk));out={}
for key,urls in pk.items():
 for u in urls:
  m=re.search(r'github.com/([^/]+/[^/]+)',u)
  if not m:continue
  repo=m[1];p=R/f'github/{key}.json';p.parent.mkdir(exist_ok=True)
  try:
   if p.exists():v=json.loads(p.read_text())
   else:
    sha=u.rstrip('/').split('/')[-1]if'/tree/'in u and len(u.rstrip('/').split('/')[-1])==40 else'HEAD';url=f'https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1';time.sleep(1.2);v=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ReproCrowd'}),timeout=35));p.write_text(json.dumps(v))
   fs=[f for f in v.get('tree',[])if f['type']=='blob'];out[key]={'url':u,'sha':v.get('sha'),'bytes':sum(f.get('size',0)for f in fs),'nfiles':len(fs),'suffixes':sorted(set(pathlib.Path(f['path']).suffix.lower()for f in fs)),'truncated':v.get('truncated'),'files':fs};print(key,len(fs),round(out[key]['bytes']/1e6,2),out[key]['suffixes'],flush=True)
  except Exception as e:out[key]={'error':str(e),'url':u};print(key,str(e),flush=True)
 (R/'github_summary.json').write_text(json.dumps(out))
