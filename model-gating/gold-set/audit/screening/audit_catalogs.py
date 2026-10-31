import urllib.request,json,pathlib,concurrent.futures,html,re
R=pathlib.Path('/tmp/scratch_gold/sol')
def get(u,path):
 p=R/path
 if p.exists(): return json.loads(p.read_text())
 q=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=50); v=json.load(q);p.write_text(json.dumps(v));return v
for key,u in [('score_files','https://api.osf.io/v2/nodes/ed8pj/files/osfstorage/?page[size]=100'),('score_children','https://api.osf.io/v2/nodes/ed8pj/children/?page[size]=100')]:
 try:
  v=get(u,key+'.json'); print(key, json.dumps(v)[:15000])
 except Exception as e: print(key,e)
def hf(i):
 try:
  v=get(f'https://huggingface.co/api/datasets/chuxuan/REPRO-Bench/tree/main/{i}?recursive=true&limit=1000',f'hf_{i}.json');return i,len(v),sum(x.get('size',0) for x in v),[x['path'] for x in v if x['type']=='file' and re.search(r'\.(r|rmd|py|do|m|jl)$',x['path'],re.I)]
 except Exception as e:return i,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 v=list(ex.map(hf,range(1,113)))
(R/'hf_summary.json').write_text(json.dumps(v))
for x in v:print(x[0:3], str(x[3:])[:180])
s=(R/'i4r.txt').read_text(); print('scripts', re.findall(r'<script[^>]+src="([^"]+)',s));print('serialized',s[-5000:])
