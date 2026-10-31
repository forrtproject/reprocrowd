import urllib.request,pathlib,re,html,json,time
R=pathlib.Path('/tmp/scratch_gold/sol');ids={'6x8wy':'s41562-022-01498-1','ucz85':'s41562-023-01715-5','4wxms':'s41562-023-01769-5','9qa3x':'s41562-023-01696-5','p8f7d':'s41562-023-01680-6'}
for k,d in ids.items():
 p=R/f'nature_{k}.html'
 try:
  if not p.exists():time.sleep(1);p.write_bytes(urllib.request.urlopen('https://www.nature.com/articles/'+d,timeout=35).read())
  s=p.read_text();blocks=re.findall(r'<section[^>]+(?:id="data-availability"|aria-labelledby="data-availability")[\s\S]*?</section>',s)
  # the identifiers differ; use all data/code availability text contexts
  for m in re.finditer(r'id="(?:data-availability|code-availability|Sec\d+)"',s):
   st=s[m.start():m.start()+8000]
   if 'Data availability' in st[:1000]or'Code availability'in st[:1000]:blocks.append(st)
  print('\n',k)
  for b in blocks:print(html.unescape(re.sub('<[^>]+>',' ',b))[:4000]);print(re.findall(r'href="(https?[^"\s]+)"',b)[:15])
 except Exception as e:print(k,str(e))
