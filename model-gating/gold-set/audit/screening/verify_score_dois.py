import pathlib,json,urllib.request,urllib.parse,time,re,difflib
R=pathlib.Path('/tmp/scratch_gold/sol');out={}
for x in json.loads((R/'selection_score.json').read_text()):
 k=x['id'];p=R/f'metadata_score/{k}.json';p.parent.mkdir(exist_ok=True)
 try:
  if not p.exists():time.sleep(1.3);p.write_bytes(urllib.request.urlopen('https://api.crossref.org/works/'+urllib.parse.quote(x['doi'],safe=''),timeout=20).read())
  a=json.loads(p.read_text())['message'];norm=lambda s:' '.join(re.findall('[a-z0-9]+',s.lower()));score=difflib.SequenceMatcher(None,norm(x['title']),norm(a['title'][0])).ratio();out[k]={'doi':a['DOI'],'title':a['title'][0],'match_score':score};print(k,round(score,3),a['DOI'],flush=True)
 except Exception as e:out[k]={'error':str(e)};print(k,str(e),flush=True)
(R/'score_doi_verification.json').write_text(json.dumps(out))
