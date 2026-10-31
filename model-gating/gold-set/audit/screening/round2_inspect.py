import urllib.request,json,pathlib,time,sys,re,hashlib
R=pathlib.Path('/tmp/scratch_gold/sol/round2_packages');R.mkdir(exist_ok=True)
def get(u,p):
 if p.exists():return json.loads(p.read_text())
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ReproCrowd research screening'}),timeout=30)as f:v=json.load(f)
 p.write_text(json.dumps(v));time.sleep(.3);return v
def osf(node):
 d=R/node;d.mkdir(exist_ok=True);fs=[];errs=[];seen=set()
 def scan(u,depth=0):
  if u in seen or depth>7:return
  seen.add(u)
  try:
   z=get(u,d/f'{len(seen)}.json')
   for f in z.get('data',[]):
    fs.append(f)
    if f['attributes']['kind']=='folder':scan(f['relationships']['files']['links']['related']['href']+'?page[size]=100',depth+1)
   if z.get('links',{}).get('next'):scan(z['links']['next'],depth)
  except Exception as e:errs.append(str(e)+' '+u)
 scan(f'https://api.osf.io/v2/nodes/{node}/files/osfstorage/?page[size]=100')
 try:
  cs=get(f'https://api.osf.io/v2/nodes/{node}/children/?page[size]=100',d/'children.json')
  for c in cs.get('data',[]):scan(f'https://api.osf.io/v2/nodes/{c["id"]}/files/osfstorage/?page[size]=100')
 except Exception as e:errs.append(str(e))
 out=dict(files=fs,errors=errs,nfiles=sum(f['attributes']['kind']=='file'for f in fs),bytes=sum(f['attributes'].get('size')or 0 for f in fs),urls=[f'https://osf.io/{node}/']);(R/f'{node}_summary.json').write_text(json.dumps(out));print(node,out['nfiles'],round(out['bytes']/1e6,3),errs,flush=True)
 print([(f['id'],f['attributes']['name'],f['attributes'].get('size'),f.get('links',{}).get('download'))for f in fs if f['attributes']['kind']=='file'][:100],flush=True)
def gh(repo):
 d=R/repo.replace('/','_');d.mkdir(exist_ok=True)
 meta=get('https://api.github.com/repos/'+repo,d/'meta.json');branch=meta['default_branch'];z=get('https://api.github.com/repos/'+repo+'/git/trees/'+branch+'?recursive=1',d/'tree.json');print(repo,'SHA',z['sha'],'bytes',sum(f.get('size',0)for f in z['tree']),'truncated',z['truncated']);print([(f['path'],f.get('size'))for f in z['tree'] if f['type']=='blob'][:120])
for a in sys.argv[1:]:
 try:gh(a)if '/'in a else osf(a)
 except Exception as e:print(a,str(e),flush=True)
