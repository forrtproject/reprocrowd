import json,pathlib,pdfplumber,re,concurrent.futures
R=pathlib.Path('/tmp/scratch_gold/sol');v=json.loads((R/'selection_i4r.json').read_text())
def run(x):
 uris=[]
 with pdfplumber.open(x['textpath'][:-4]) as p:
  for pg in p.pages:
   for a in pg.hyperlinks:
    u=a.get('uri','')
    if u and not re.search(r'mailto:|orcid|doi.org/10.1038/s41562-023-01807',u):uris.append(u)
 return x['node'],list(dict.fromkeys(uris))
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:out=dict(ex.map(run,v))
(R/'report_hyperlinks.json').write_text(json.dumps(out))
for x in v:print(x['node'],out[x['node']][:15])
