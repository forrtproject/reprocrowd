import urllib.request,json,pathlib,concurrent.futures,re,subprocess
R=pathlib.Path('/tmp/scratch_gold/sol')
def fetch(u,p):
 p=R/p;p.parent.mkdir(exist_ok=True,parents=True)
 if p.exists():return p
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as r:p.write_bytes(r.read())
 return p
v=json.loads((R/'i4r_reports.json').read_text()); sel=[x for x in v if x['journal'] in ['Psychological Science','Nature Human Behaviour','AJPS','JOP','APSR']]
def run(x):
 node=x['reportUrl'].strip('/').split('/')[-1]; files=[]; errors=[]
 def tree(u,depth=0):
  try:
   data=json.loads(fetch(u,f'osf/{node}/tree_{len(files)}_{depth}.json').read_text())
   for f in data.get('data',[]):
    files.append(f)
    a=f['attributes'];name=a['name']
    if a['kind']=='folder' and depth<2 and re.search(r'report|reproduc|replicat|^files$',name,re.I):tree(f['relationships']['files']['links']['related']['href']+'?page[size]=100',depth+1)
    elif a['kind']=='file' and a['size']<12000000 and re.search(r'\.pdf$',name,re.I) and not re.search(r'original|manuscript|supplement',name,re.I):
     p=fetch(f['links']['download'],f'osf/{node}/{f["id"]}.pdf');subprocess.run(['pdftotext','-layout',str(p),str(p)+'.txt'],capture_output=True)
   if data.get('links',{}).get('next'):tree(data['links']['next'],depth)
  except Exception as e:errors.append(str(e))
 tree(f'https://api.osf.io/v2/nodes/{node}/files/osfstorage/?page[size]=100')
 (R/f'osf/{node}/allfiles.json').write_text(json.dumps(files))
 return node,x['title'],[(f['attributes']['name'],f['attributes']['size']) for f in files],errors
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 results=list(ex.map(run,sel))
(R/'i4r_files_summary.json').write_text(json.dumps(results))
print('nodes',len(results),'files',sum(len(x[2]) for x in results),'pdfs',len(list((R/'osf').glob('*/*.pdf'))),'errors',[(x[0],x[3]) for x in results if x[3]])
