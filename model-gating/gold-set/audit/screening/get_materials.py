import urllib.request,json,pathlib,concurrent.futures,re,urllib.parse,zipfile,subprocess
R=pathlib.Path('/tmp/scratch_gold/sol')
def fetch(u,p):
 p=R/p;p.parent.mkdir(exist_ok=True,parents=True)
 if p.exists():return p
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60) as r:p.write_bytes(r.read())
 return p
fetch('https://osf.io/download/cs8up/','score.zip')
with zipfile.ZipFile(R/'score.zip') as z:
 print('SCORE zip',z.namelist()[:100]);z.extractall(R/'score')
s=(R/'i4r.txt').read_text()
# Decode Next's string payload before extracting report records.
reports=[]
for raw in re.findall(r'self\.__next_f\.push\(\[1,("(?:\\.|[^"\\])*")\]\)',s):
 v=json.loads(raw)
 m=re.search(r'"reports":(\[.*\])',v)
 if m:
  arr=json.JSONDecoder().raw_decode(m[1])[0];reports.extend(arr)
(R/'i4r_reports.json').write_text(json.dumps(reports)); print('I4R records',len(reports))
def hf(i):
 try:
  v=json.loads((R/f'hf_{i}.json').read_text());targets=[x for x in v if x['type']=='file' and ('/replication_package/' not in x['path'] or re.search(r'readme',x['path'],re.I)) and x.get('size',0)<5000000]
  for x in targets:
   p=fetch('https://huggingface.co/datasets/chuxuan/REPRO-Bench/resolve/main/'+urllib.parse.quote(x['path']), 'hf_files/'+x['path'])
   if p.suffix.lower()=='.pdf':subprocess.run(['pdftotext','-layout',str(p),str(p)+'.txt'],capture_output=True)
  return i,[(x['path'],x['size']) for x in targets]
 except Exception as e:return i,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for v in ex.map(hf,range(1,113)):print(v)
