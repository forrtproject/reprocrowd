import urllib.request,re,json,pathlib,concurrent.futures,subprocess,html
R=pathlib.Path('/tmp/scratch_gold/sol');nums=[10,36,45,58,61,69,73,79,86,152]
def run(n):
 try:
  p=R/f'dp/{n}.html';p.parent.mkdir(exist_ok=True)
  if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://ideas.repec.org/p/zbw/i4rdps/{n}.html',timeout=40).read())
  s=p.read_text();links=re.findall(r'(?:https?[^"<>\s]+)',s);pdfs=[html.unescape(u)for u in links if '.pdf' in u.lower() and 'econstor' in u]
  print(n,list(dict.fromkeys(pdfs)),flush=True)
  if pdfs:
   u=pdfs[0];q=R/f'dp/{n}.pdf'
   if not q.exists():q.write_bytes(urllib.request.urlopen(u,timeout=40).read())
   subprocess.run(['pdftotext','-layout',str(q),str(q)+'.txt'],capture_output=True);return n,u
 except Exception as e:return n,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:out=dict(ex.map(run,nums))
(R/'dp_urls.json').write_text(json.dumps(out));print(out)
