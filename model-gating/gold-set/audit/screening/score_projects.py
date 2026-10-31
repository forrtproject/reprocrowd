import json,pathlib,urllib.request,re,concurrent.futures,subprocess
R=pathlib.Path('/tmp/scratch_gold/sol');v=json.loads((R/'score_summary.json').read_text())
def get(u,p):
 p=R/p;p.parent.mkdir(exist_ok=True,parents=True)
 if not p.exists():
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30)as r:p.write_bytes(r.read())
 return p
sel=[x for x in v if x['availability'].get('OA_code_shared')=='available_online' or any(k in x['outcomes'] for k in ['none','not attemptable'])]
def run(x):
 allf=[];children=[];errs=[];ns=[a['project_guid'] for a in x['projects'] if a.get('project_guid') not in ['NA',None]]
 def folder(node,url,dep=0):
  try:
   pg=0
   while url:
    data=json.loads(get(url,f'score_projects/{x["id"]}/{node}_{dep}_{len(allf)}_{pg}.json').read_text())
    for f in data.get('data',[]):
     allf.append(f);a=f['attributes']
     if a['kind']=='folder' and dep<2 and not re.search(r'data|archive|figure',a['name'],re.I):folder(node,f['relationships']['files']['links']['related']['href']+'?page[size]=100',dep+1)
     elif a['kind']=='file' and a.get('size',0)<8000000 and re.search(r'\.pdf$',a['name'],re.I):
      p=get(f['links']['download'],f'score_projects/{x["id"]}/{f["id"]}.pdf');subprocess.run(['pdftotext','-layout',str(p),str(p)+'.txt'],capture_output=True)
    url=data.get('links',{}).get('next');pg+=1
  except Exception as e:errs.append(str(e))
 for node in ns:
  folder(node,f'https://api.osf.io/v2/nodes/{node}/files/osfstorage/?page[size]=100')
  try:
   ds=json.loads(get(f'https://api.osf.io/v2/nodes/{node}/children/?page[size]=100',f'score_projects/{x["id"]}/{node}_children.json').read_text())
   for c in ds.get('data',[]):
    children.append(c);folder(c['id'],f'https://api.osf.io/v2/nodes/{c["id"]}/files/osfstorage/?page[size]=100')
  except Exception as e:errs.append(str(e))
 (R/f'score_projects/{x["id"]}/allfiles.json').write_text(json.dumps(allf))
 return x['id'],len(allf),len(children),errs
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as ex:
 for z in ex.map(run,sel):print(z,flush=True)
