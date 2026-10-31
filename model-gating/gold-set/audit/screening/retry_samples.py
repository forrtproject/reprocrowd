import pathlib,json,urllib.request,time,hashlib
R=pathlib.Path('/tmp/scratch_gold/sol');checks=json.loads((R/'sample_download_checks.json').read_text());pk=json.loads((R/'packages_summary.json').read_text());ch=json.loads((R/'package_children_summary.json').read_text())
for k,vs in checks.items():
 for i,x in enumerate(vs):
  if not x.get('error'):continue
  fs=pk.get(k,{}).get('files',[])+ch.get(k,{}).get('files',[]);f=next((f for f in fs if f['attributes']['name']==x['filename']),None)
  if not f:continue
  try:
   time.sleep(1.5);b=urllib.request.urlopen(f['links']['download'],timeout=25).read();p=R/f'package_samples/{k}/{f["id"]}_{x["filename"]}';p.write_bytes(b);vs[i]={'filename':x['filename'],'bytes':len(b),'url':f['links']['download'],'sha256':hashlib.sha256(b).hexdigest(),'retried_after_transient_error':x['error']};print(k,x['filename'],'OK',len(b),flush=True)
  except Exception as e:print(k,x['filename'],str(e),flush=True)
(R/'sample_download_checks.json').write_text(json.dumps(checks))
