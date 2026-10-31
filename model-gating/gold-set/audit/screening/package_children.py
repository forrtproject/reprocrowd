import pathlib,json,urllib.request,urllib.error,time,re,hashlib
R=pathlib.Path('/tmp/scratch_gold/sol');pk=json.loads((R/'package_map.json').read_text());out={}
def get(u,key):
 p=R/f'package_children/{key}/{hashlib.sha1(u.encode()).hexdigest()}.json';p.parent.mkdir(exist_ok=True,parents=True)
 if p.exists():return json.loads(p.read_text())
 time.sleep(1.2)
 with urllib.request.urlopen(u,timeout=25)as r:v=json.load(r)
 p.write_text(json.dumps(v));return v
for key,urls in pk.items():
 files=[];errors=[];nodes=[];seen=set()
 def folder(node,u):
  if u in seen:return
  seen.add(u)
  d=get(u,key)
  for f in d.get('data',[]):
   files.append(f)
   if f['attributes']['kind']=='folder':folder(node,f['relationships']['files']['links']['related']['href']+'?page[size]=100')
  if d.get('links',{}).get('next'):folder(node,d['links']['next'])
 for u in urls:
  m=re.search('osf.io/([a-z0-9]{5})',u,re.I)
  if not m:continue
  node=m[1]
  try:
   d=get(f'https://api.osf.io/v2/nodes/{node}/children/?page[size]=100',key)
   for n in d.get('data',[]):
    nodes.append(n)
    if n['attributes'].get('public'):folder(n['id'],f'https://api.osf.io/v2/nodes/{n["id"]}/files/osfstorage/?page[size]=100')
   if d.get('links',{}).get('next'):errors.append('Uninspected child pagination')
  except Exception as e:
   errors.append(str(e))
   if '429'in str(e):print('RATE_LIMIT_STOP',key,flush=True);raise SystemExit()
 out[key]={'files':files,'nodes':nodes,'errors':errors};(R/'package_children_summary.json').write_text(json.dumps(out));print(key,len(nodes),len(files),errors,flush=True)
