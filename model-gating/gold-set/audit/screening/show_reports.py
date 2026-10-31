import pathlib,json,re,sys
R=pathlib.Path('/tmp/scratch_gold/sol');v=json.loads((R/'report_index.json').read_text());args=sys.argv[1:]
for x in v:
 if x['node'] not in args:continue
 s=pathlib.Path(x['textpath']).read_text();print('\n###',x['node'],x['title'],'\n',x['evidence_url'],x['osf_links'],x['code_langs'])
 # strip front matter and introduction then read computational section until robustness
 mats=list(re.finditer(r'(?im)^\s*(?:\d+(?:\.\d+)*\.?\s+)?(?:Computational Reproducibility|Reproducibility|Computational Reproduction|Reproduction results)',s))
 st=mats[0].start() if mats else 0
 print(s[st:st+9500])
