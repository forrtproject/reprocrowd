import json,pathlib,urllib.request,time,re,zipfile,xml.etree.ElementTree as ET
R=pathlib.Path('/tmp/scratch_gold/sol')
for k in ['8R9d','LyWB','9DZl','q8xv','Pxp7','JRpA','0P4r']:
 p=R/f'score_projects/{k}/allfiles.json'
 if not p.exists():continue
 for f in json.loads(p.read_text()):
  a=f['attributes'];name=a['name']
  if a['kind']!='file'or a['size']>1000000 or not re.search(r'\.(md|docx|xlsx|r|do|csv)$',name,re.I):continue
  dest=p.parent/name
  try:
   if not dest.exists():
    time.sleep(1.1);dest.write_bytes(urllib.request.urlopen(f['links']['download'],timeout=25).read())
   if name.endswith('.docx'):
    with zipfile.ZipFile(dest)as z:txt=ET.fromstring(z.read('word/document.xml'));t='\n'.join(''.join(n.itertext())for n in txt.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'));pathlib.Path(str(dest)+'.txt').write_text(t)
  except Exception as e:print(k,name,str(e),flush=True)
 print('done',k,flush=True)
