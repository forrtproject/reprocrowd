import urllib.request,json,concurrent.futures,pathlib
root=pathlib.Path('/tmp/scratch_gold/sol')
urls={'hfroot':'https://huggingface.co/api/datasets/chuxuan/REPRO-Bench/tree/main','i4r':'https://www.i4replication.org/reports','score_osf':'https://api.osf.io/v2/nodes/ed8pj/','score_nature':'https://www.nature.com/articles/s41586-026-10203-5','repro_paper':'https://arxiv.org/html/2507.18901v1'}
def f(k,u):
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40); b=r.read();(root/(k+'.txt')).write_bytes(b);return k,r.status,len(b)
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for v in ex.map(lambda x:f(*x),urls.items()):print(v)
