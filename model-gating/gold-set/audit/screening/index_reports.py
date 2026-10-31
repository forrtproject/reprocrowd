import pathlib,json,re,collections
R=pathlib.Path('/tmp/scratch_gold/sol');v=json.loads((R/'i4r_reports.json').read_text());out=[]
for x in v:
 node=(x.get('reportUrl')or'').strip('/').split('/')[-1]
 if not re.fullmatch('[a-z0-9]{5}',node):continue
 ps=list((R/'osf'/node).glob('*.pdf.txt'))
 opts=[]
 for p in ps:
  s=p.read_text();start=re.sub(r'\s+',' ',s[:900]).lower()
  if re.search(r'(response to|reply to|rejoinder|authors.{0,3}response|comment on the reproduction)',start):continue
  opts.append((len(s),p,s))
 if not opts:continue
 _,p,s=max(opts);files=json.loads((R/'osf'/node/'allfiles.json').read_text())if (R/'osf'/node/'allfiles.json').exists()else[]
 f=next((f for f in files if f['id']==p.name.split('.')[0]),{})
 out.append(dict(x,node=node,textpath=str(p),evidence_url=f.get('links',{}).get('download',''),nchars=len(s),osf_links=list(dict.fromkeys(re.findall(r'https?://osf.io/[a-zA-Z0-9]{5}',s))),code_langs=list(set(re.findall(r'(?i)\b(?:R scripts?|R code|R version|Python|Stata|SPSS|Matlab|JASP|jamovi)\b',s)))))
(R/'report_index.json').write_text(json.dumps(out))
for x in out:
 if x['journal']=='Nature Human Behaviour':
  s=pathlib.Path(x['textpath']).read_text(); matches=list(re.finditer(r'(?i)(?:random.{0,15}seed|seed.{0,30}not|not.{0,20}seed|missing.{0,25}(?:files?|code|data)|could not.{0,30}run|unable to.{0,25}run|fatal)',s))
  if matches:
   print('\n',x['node'],x['title'],'LANG',x['code_langs'])
   for m in matches[:3]: print(re.sub(r'\s+',' ',s[max(0,m.start()-120):m.end()+400]))
