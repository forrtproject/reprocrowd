import json,pathlib,urllib.request,urllib.parse,time,re,difflib,unicodedata
R=pathlib.Path('/tmp/scratch_gold/sol');v=json.loads((R/'metadata_matches.json').read_text());sel=json.loads((R/'selection_i4r.json').read_text());extra={x['node']:x['title']for x in sel if x['node']not in v}; fix={k:v[k]['query']for k in ['u2rx8','8czs5','g82fy','p8f7d']};fix['p8f7d']='Accelerating science with human-aware artificial intelligence';tasks={**extra,**fix,'rn8t7':'Caricaturing Shapes in Visual Memory','hf25':'Entertaining Beliefs in Economic Mobility','us2g4':'Can Invalid Information Be Ignored When It Is Detected?'};known={'rn8t7':'10.1177/09567976231225091','hf25':'10.1111/ajps.12702','us2g4':'10.1177/09567976241231571'}
def norm(s):return ' '.join(re.findall('[a-z0-9]+',unicodedata.normalize('NFKD',s.lower())))
for k,t in tasks.items():
 p=R/f'metadata_fix/{k}.json';p.parent.mkdir(exist_ok=True)
 try:
  if p.exists():d=json.loads(p.read_text())
  else:
   time.sleep(1.5);url='https://api.crossref.org/works/'+urllib.parse.quote(known[k],safe='')if k in known else'https://api.crossref.org/works?rows=5&filter=type:journal-article&query.title='+urllib.parse.quote(t);d=json.load(urllib.request.urlopen(url,timeout=25));p.write_text(json.dumps(d))
  items=[d['message']]if k in known else d['message']['items'];score,a=max([(difflib.SequenceMatcher(None,norm(t),norm(a.get('title',[''])[0])).ratio(),a)for a in items],key=lambda z:z[0]);v[k]=dict(query=t,match_score=score,title=a['title'][0],doi=a['DOI'],date=a.get('published',{}).get('date-parts'),journal=a.get('container-title'),url=a.get('URL'));print(k,round(score,2),a['DOI'],a.get('container-title'),flush=True)
 except Exception as e:print(k,str(e),flush=True)
 (R/'metadata_matches.json').write_text(json.dumps(v))
