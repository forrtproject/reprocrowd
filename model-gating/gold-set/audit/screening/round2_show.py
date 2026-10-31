import json,pathlib,re,sys
r=pathlib.Path('/tmp/scratch_gold/sol');v=json.loads((r/'report_index.json').read_text())+json.loads((r/'round2_remaining_index.json').read_text())
for x in v:
 if x['node']not in sys.argv[1:] or not x.get('textpath'):continue
 s=pathlib.Path(x['textpath']).read_text();print('\n###',x['node'],x['journal'],x['title'],x['evidence_url']);ms=list(re.finditer(r'(?im)^\s*(?:[23](?:\.\d+)*\.?\s+)?(?:Computational [Rr]eproduc|Reproducibility|Reproduction of)',s));st=ms[0].start()if ms else 0;print(s[st:st+13000])
