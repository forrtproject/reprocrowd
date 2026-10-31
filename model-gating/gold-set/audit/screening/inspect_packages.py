import urllib.request,urllib.error,pathlib,json,re,time,sys
R=pathlib.Path('/tmp/scratch_gold/sol');pk=json.loads((R/'package_map.json').read_text());out={};cnt=0
class RateLimit(Exception):pass
def get(u,p):
 global cnt
 p=R/p;p.parent.mkdir(exist_ok=True,parents=True)
 if p.exists():return json.loads(p.read_text())
 time.sleep(1.05);cnt+=1
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ReproCrowd research screener'}),timeout=20)as r:v=json.load(r)
 except urllib.error.HTTPError as e:
  if e.code==429:raise RateLimit()
  raise
 p.write_text(json.dumps(v));return v
for key,urls in pk.items():
 files=[];errors=[];seen=set();nodes=[]
 def scan(node,url,depth=0):
  if url in seen or depth>6 or len(seen)>100:return
  seen.add(url)
  try:
   data=get(url,f'packages/{key}/{len(seen)}.json')
   for f in data.get('data',[]):
    a=f['attributes'];files.append(f)
    if a['kind']=='folder':scan(node,f['relationships']['files']['links']['related']['href']+'?page[size]=100',depth+1)
   if data.get('links',{}).get('next'):scan(node,data['links']['next'],depth)
  except RateLimit:raise
  except Exception as e:errors.append(str(e)+' '+url)
 try:
  for u in urls:
   m=re.search(r'osf.io/([a-z0-9]{5})',u,re.I)
   if not m:continue
   node=m[1].lower();scan(node,f'https://api.osf.io/v2/nodes/{node}/files/osfstorage/?page[size]=100')
   if not files:
    try:
     ch=get(f'https://api.osf.io/v2/nodes/{node}/children/?page[size]=100',f'packages/{key}/children.json')
     for c in ch.get('data',[]):nodes.append(c);scan(c['id'],f'https://api.osf.io/v2/nodes/{c["id"]}/files/osfstorage/?page[size]=100')
    except RateLimit:raise
    except Exception as e:errors.append(str(e))
 except RateLimit:
  print('STOP_RATE_LIMIT',key,'after',cnt,'requests',flush=True);break
 z={'urls':urls,'files':files,'errors':errors,'nodes':nodes,'bytes':sum(f['attributes'].get('size')or 0 for f in files if f['attributes']['kind']=='file'),'nfiles':sum(f['attributes']['kind']=='file'for f in files),'suffixes':sorted(set(pathlib.Path(f['attributes']['name']).suffix.lower()for f in files if f['attributes']['kind']=='file'))};out[key]=z
 (R/'packages_summary.json').write_text(json.dumps(out));print(key,z['nfiles'],round(z['bytes']/1e6,2),z['suffixes'],errors[:2],flush=True)
