import json,pathlib,re,urllib.request,concurrent.futures,subprocess,time
R=pathlib.Path('/tmp/scratch_gold/sol');root=R/'round2_reports';root.mkdir(exist_ok=True)
v=json.loads((R/'i4r_reports.json').read_text());seen={x['node'] for x in json.loads((R/'report_index.json').read_text())}
sel=[x for x in v if re.fullmatch(r'https://osf.io/[a-z0-9]{5}/?',x.get('reportUrl')or'') and x['reportUrl'].strip('/').split('/')[-1] not in seen]
def get(u,p):
 if p.exists():return p.read_bytes()
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ReproCrowd academic screening'}),timeout=25)as f:b=f.read()
 p.write_bytes(b);return b
def run(x):
 node=x['reportUrl'].strip('/').split('/')[-1];d=root/node;d.mkdir(exist_ok=True);files=[];errors=[]
 def scan(u,dep=0):
  try:
   dat=json.loads(get(u,d/f'tree_{len(files)}_{dep}.json'))
   for f in dat.get('data',[]):
    files.append(f);a=f['attributes']
    if a['kind']=='folder' and dep<2 and re.search('report|reproduc|replicat|^files$',a['name'],re.I):scan(f['relationships']['files']['links']['related']['href']+'?page[size]=100',dep+1)
    elif a['kind']=='file' and a['size']<15000000 and re.search(r'\.pdf$',a['name'],re.I) and not re.search('original|supplement|manuscript',a['name'],re.I):
     p=d/(f['id']+'.pdf');get(f['links']['download'],p);subprocess.run(['pdftotext','-layout',str(p),str(p)+'.txt'],capture_output=True)
   if dat.get('links',{}).get('next'):scan(dat['links']['next'],dep)
  except Exception as e:errors.append(str(e))
 scan(f'https://api.osf.io/v2/nodes/{node}/files/osfstorage/?page[size]=100');(d/'allfiles.json').write_text(json.dumps(files));opts=[]
 for p in d.glob('*.pdf.txt'):
  s=p.read_text();st=re.sub(r'\s+',' ',s[:1000]).lower()
  if re.search(r'response to|reply to|rejoinder|authors.{0,3}response|comment on the reproduction',st):continue
  opts.append((len(s),p,s))
 out=dict(x,node=node,errors=errors)
 if opts:
  _,p,s=max(opts);f=next(z for z in files if z['id']==p.name.split('.')[0]);out.update(textpath=str(p),evidence_url=f['links']['download'],nchars=len(s))
 return out
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:
 for x in ex.map(run,sel):
  out.append(x);(R/'round2_remaining_index.json').write_text(json.dumps(out));print(x['node'],x.get('nchars'),x['errors'][:1],flush=True)
