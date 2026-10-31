import pathlib,json,urllib.request,time,re,zipfile,hashlib
R=pathlib.Path('/tmp/scratch_gold/sol');pk=json.loads((R/'packages_summary.json').read_text());ch=json.loads((R/'package_children_summary.json').read_text());wanted=['bz8pf','mgy45','j65xf','gjm3c','7cd2s','rkdqv','5c9aj','wg2sv','fpaxs','xg3h9','529en','t68dc','av3mz','kpm3d','kwqj6','kyufb','8dxvk','4wxms','vzpu2','6by24','vcsfj','vg2kt','ucz85','SC-8R9d','SC-rjb'];out={}
for k in wanted:
 fs={f['id']:f for f in pk.get(k,{}).get('files',[])+ch.get(k,{}).get('files',[])if f['attributes']['kind']=='file'};codes=[];data=[];zips=[]
 for f in fs.values():
  a=f['attributes'];name=a['name'].lower();size=a['size']or 0
  if size<500000 and re.search(r'\.(r|rmd|py)$',name):codes.append(f)
  elif size<1000000 and re.search(r'\.(csv|rdata|rds|dta|xlsx)$',name):data.append(f)
  elif size<20000000 and name.endswith('.zip'):zips.append(f)
 targets=codes[:1]+data[:1]
 if not codes or not data:targets+=zips[:3]
 records=[]
 for f in targets:
  a=f['attributes'];p=R/f'package_samples/{k}/{f["id"]}_{a["name"]}';p.parent.mkdir(exist_ok=True,parents=True)
  try:
   if not p.exists():time.sleep(1.25);p.write_bytes(urllib.request.urlopen(f['links']['download'],timeout=35).read())
   b=p.read_bytes();z={'filename':a['name'],'bytes':len(b),'url':f['links']['download'],'sha256':hashlib.sha256(b).hexdigest()}
   if p.suffix=='.zip':
    with zipfile.ZipFile(p)as arc:z['zip_uncompressed_bytes']=sum(i.file_size for i in arc.infolist());z['zip_files']=arc.namelist()
   records.append(z)
  except Exception as e:records.append({'filename':a['name'],'error':str(e)})
 out[k]=records;(R/'sample_download_checks.json').write_text(json.dumps(out));print(k,[(x['filename'],x.get('bytes'),x.get('error'))for x in records],flush=True)
