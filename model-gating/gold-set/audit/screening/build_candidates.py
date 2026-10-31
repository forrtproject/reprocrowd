import pathlib,json,csv,collections,re,hashlib
R=pathlib.Path('/tmp/scratch_gold/sol');O=pathlib.Path(__file__).resolve().parents[2]
def read(n,default=None):
 p=R/n;return json.loads(p.read_text())if p.exists()else(default if default is not None else{})
cur=read('curation.json');sel=read('selection_i4r.json');meta=read('metadata_matches.json');pk=read('packages_summary.json');children=read('package_children_summary.json');gh=read('github_summary.json');maps=read('package_map.json');samples=read('sample_download_checks.json')
# Identify issue-year from authoritative metadata rather than assuming online year = issue year.
allmeta={}
for p in list((R/'metadata').glob('*.json'))+list((R/'metadata_slow').glob('*.json'))+list((R/'metadata_fix').glob('*.json'))+[R/'metadata_hf65.json']:
 try:
  a=json.loads(p.read_text())['message'];items=a.get('items',[a])
  for i in items:
   if i.get('DOI'):allmeta[i['DOI'].lower()]=i
 except (KeyError,TypeError):pass
def year(m):
 a=allmeta.get(m.get('doi','').lower(),{});d=a.get('published-print')or a.get('published')or{};return str(d.get('date-parts',m.get('date',[[None]]))[0][0]or'')
def inventory(k):
 fs={f['id']:f for f in pk.get(k,{}).get('files',[])+children.get(k,{}).get('files',[])if f['attributes']['kind']=='file'}
 size=sum(f['attributes'].get('size')or 0 for f in fs.values())
 g=gh.get(k,{})
 if g.get('bytes'):size+=g['bytes']
 su=set(pathlib.Path(f['attributes']['name']).suffix.lower()for f in fs.values())|set(g.get('suffixes',[]))
 er=pk.get(k,{}).get('errors',[])+children.get(k,{}).get('errors',[])
 # An OSF root itself may be unavailable when a complete public GitHub package is available.
 if g.get('nfiles') and not any('osf.io/'in u for u in maps.get(k,[])):er=[]
 data=bool(su&{'.csv','.dta','.xlsx','.xls','.rdata','.rda','.rds','.sav','.dat','.npz','.gz','.zip'})
 code=bool(su&{'.r','.rmd','.py','.ipynb'})
 if k=='mgy45':data=True;code=True
 if k=='bz8pf':code=True # Original R chunks embedded in shipped HTML; explicitly documented by report.
 if k in ['vcsfj','av3mz'] and '.zip'in su:code=True
 if k=='SC-LbEB':code=bool(g.get('nfiles'))
 return fs,size,su,er,data,code
fields='cand_id,source,source_record_id,doi,title,year,discipline,language,language_ok,package_url,package_size_mb,est_runtime,data_open,provisional_stratum,evidence_summary,evidence_url,claim_level_evidence,eligible,exclusion_reason,screener_confidence,notes'.split(',')
rows=[]; audit={};S='computationally reproducible';I='computational issues';T='technical failure';A='ambiguous'
disc={'z5pjq':'management','kwqj6':'linguistics','2ar74':'sociology','f5p78':'political science','3qs8e':'political science','p8f7d':'metascience','6x8wy':'metascience','mepbv':'metascience','vjkyg':'linguistics','vg2kt':'anthropology','eb89k':'psychology (behavioural genetics)'}
# Source evidence was not recovered for these package addresses; distinguish a verification gap from absent materials.
manual_ex={
 'qe3fx':'', '96nec':'', '3b8z4':'',
 'vjka5':'Full JAGS posterior refit runtime under two hours not established; report uses additional author-provided objects.',
 '9qa3x':'Only cosmetic random jitter varies; full RL training under two hours is not established. No ambiguity label is inferred.',
 'p8f7d':'Complete open inputs and laptop runtime under two hours not established.',
 '6x8wy':'Figure 4 exact fatal error and complete required public inputs unverified; do not promote path/cosmetic issues alone to P0.'}
for x in sel:
 k=x['node'];c=cur[k];m=meta.get(k,{});fs,b,suffix,errors,data,code=inventory(k);why=[]
 lang=c['language'];langok=lang in ['R','Python','R; Python','Python; R']
 if not langok:why.append('Original executable workflow is not verified as R/Python-only')
 reason=manual_ex.get(k,c.get('exclude',''))
 if reason:why.append(reason)
 if not maps.get(k):why.append('Original package URL not recovered')
 if not data:why.append('Open analysis data not verified in inspected package')
 if langok and not code:why.append('Original R/Python analysis code not verified in package')
 if b>5_000_000_000:why.append('Inspected package exceeds 5 GB')
 # Keep genuine incomplete inspections out; an unavailable unrelated registration endpoint is not evidence of missing data.
 blocking=[e for e in errors if '502'in e or '429'in e or 'Uninspected'in e]
 if blocking:why.append('Public package inventory incomplete because an endpoint failed')
 if b==0:why.append('Package size could not be established')
 if k=='3qs8e':data=False
 if k in ['9yve3','f5p78']:data=False
 eligible=not why
 evid=x.get('evidence_url','');txt=x['textpath']
 if k=='z5pjq':
  txt=str(R/'osf/z5pjq/6a8306fe86e9e1fe75bb64bf.pdf.txt');ff=read('osf/z5pjq/allfiles.json');f=next(a for a in ff if a['id']=='6a8306fe86e9e1fe75bb64bf');evid=f['links']['download']
 if k=='8dxvk':
  txt=str(R/'osf/8dxvk/6a7b6264550f4cce0d6a5aa0.pdf.txt');ff=read('osf/8dxvk/allfiles.json');f=next(a for a in ff if a['id']=='6a7b6264550f4cce0d6a5aa0');evid=f['links']['download']
 if k=='xqnhw':
  txt=str(R/'osf/xqnhw/6a564826a754311bf75b92b1.pdf.txt');ff=read('osf/xqnhw/allfiles.json');f=next(a for a in ff if a['id']=='6a564826a754311bf75b92b1');evid=f['links']['download']
 rt='estimated 5-60 min; not timed'
 if k in ['j65xf','qe3fx','fpaxs','kwqj6','fwzbg','3b8z4']:rt='estimated 15-120 min; not timed'
 if k=='7cd2s':rt='source: original code 58.13 seconds'
 if c['stratum']==T:rt='P0 observed by source; full successful runtime unverified'
 if k=='mepbv':rt='parse blocker <1 min verified; full repaired run unestimated'
 if k in ['vjka5','vjkyg','9qa3x','ts2mp','p8f7d']:rt='not established within 2 h'
 claims='yes'
 if c['stratum']==T or k in ['9jzvk','w8gd7','8czs5','pzhgw','vjka5','4wxms','ghkn9']:claims='partial'
 note=c.get('note','')
 if errors:note+=' Inventory endpoint errors: '+'; '.join(errors[:2])+'.'
 if gh.get(k,{}).get('sha'):note+=' Git tree '+gh[k]['sha']+'.'
 if fs:note+=f' Public metadata inspected for {len(fs)} files, including child components; sizes are deposited bytes, not all expanded archives.'
 if eligible:note+=' Screening eligible only; confirm 5-8 claim selections, original package/report version correspondence and runtime before drawing.'
 if c['stratum']==I:note+=' Provisional severity P1/P2 requires independent claim adjudication.'
 row=dict(cand_id=f'I4R-{k}',source='I4R',source_record_id=k,doi=m.get('doi',''),title=m.get('title',x['title']),year=year(m),discipline=disc.get(k,'psychology'),language=lang,language_ok=str(langok).lower(),package_url=' | '.join(maps.get(k,[])),package_size_mb=f'{b/1e6:.3f}'if b else'',est_runtime=rt,data_open=('false' if k in ['9yve3','f5p78'] else ('true'if data and not blocking else'unknown')),provisional_stratum=c['stratum'],evidence_summary=c['summary'],evidence_url=evid,claim_level_evidence=claims,eligible=str(eligible).lower(),exclusion_reason='; '.join(dict.fromkeys(why)),screener_confidence='medium'if eligible else('high'if not langok or b>5e9 else'low'),notes=note.strip())
 rows.append(row);audit[row['cand_id']]={'textpath':txt,'report_sha256':hashlib.sha256(pathlib.Path(txt[:-4]).read_bytes()).hexdigest(),'inventory_nfiles':len(fs),'inventory_errors':errors,'sample_checks':samples.get(k,[])}
# REPRO-Bench mirror is an open package; use a verified report, not its paper-level label, for the stratum.
hfc=read('hf_curated.json');hft=read('hf_titles.json');dp=read('dp_urls.json');dp.update(read('dp_urls_extra.json'));dp.update(read('dp_urls_late.json'));idx={x['node']:x for x in read('report_index.json')};info=read('hf_dataset_info.json');scores=read('ground_truth_remote.json')
for k,c in hfc.items():
 n=int(k);m=meta['hf'+k];tree=read(f'hf_{k}.json');files=[x for x in tree if x['type']=='file'and ('/replication_package/'in x['path']or'/replication-package/'in x['path'])];b=sum(x.get('size',0)for x in files)
 if c.get('dp'):evid=dp[str(c['dp'])];txt=str(R/f'dp/{c["dp"]}.pdf.txt')
 else:x=idx[c['node']];evid=x['evidence_url'];txt=x['textpath']
 if n==49:txt=str(R/'osf/ecymu/65ef0784e5e51c0c62bc556b.pdf.txt') # inspected same report text, other public copy
 rows.append(dict(cand_id=f'RB-{n:03}',source='REPRO-Bench',source_record_id=f'{n}; I4R '+(f'DP {c["dp"]}'if c.get('dp')else c['node']),doi=m['doi'],title=m['title'],year=year(m),discipline='economics'if n==65 else'political science',language='R',language_ok='true',package_url=f'https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/{info["sha"]}/{n}/replication_package',package_size_mb=f'{b/1e6:.3f}',est_runtime='source inclusion criterion <2 h; not timed',data_open='true',provisional_stratum=c['stratum'],evidence_summary=c['summary'],evidence_url=evid,claim_level_evidence='yes',eligible='true',exclusion_reason='',screener_confidence='medium',notes=c['note']+f' HF snapshot {info["sha"]}; {len(files)} package files inventoried. Independent label mapping and mirror/report-version check still required.'))
 audit[f'RB-{n:03}']={'textpath':txt,'source_score':scores[k],'inventory_nfiles':len(files)}
# SCORE outcomes are evidence about assessed claims only; do not promote repaired/recreated analyses or unattempted labels to P1/P0.
sc=read('selection_score.json');stmap={'AvOr':S,'8R9d':A,'9DZl':I,'E4Am':I,'J0Yv':S,'zK2':I,'rjb':I,'0qar':I,'LbEB':S,'GJe4':T};sclang={'AvOr':'unknown','8R9d':'R','9DZl':'SPSS','E4Am':'SPSS','J0Yv':'none','zK2':'SPSS','rjb':'R','0qar':'none','LbEB':'R; Python','GJe4':'R'}
scwhy={'AvOr':'Original analysis code was supplied on request; public original R/Python code not verified. Four assessed result claims only.','9DZl':'Original analysis language is not pilot-compatible; original OSF endpoint now returns 404.','E4Am':'Original code supplied on request; inspected public repository has only SPSS data.','J0Yv':'No original analysis code shipped; SCORE uses author-data reconstruction.','zK2':'Original inferential workflow not verified as R/Python; focal discrepancy is from Author Data Reproduction.','rjb':'Only three assessed result claims; a 5-8-claim numerical mapping was not established.','0qar':'No original analysis code shipped; SCORE reconstruction changes the analysis sample.','LbEB':'Four original numeric references are absent from this joined outcome table; quantitative claim mapping not established.','GJe4':'SCORE only says not attemptable; no precise public fatal-error cause verified.'}
for x in sc:
 k=x['id'];lang=sclang[k];cid=f'SC-{k}';fs,b,su,er,data,code=inventory(cid);c=next((a for a in x['claims']if a['repro_outcome_overall']=='not'),next((a for a in x['claims']if a['repro_outcome_overall']=='approximate'),x['claims'][0]));o=c.get('original',{});evid='https://osf.io/download/cs8up/';txt=str(R/'score/repro_outcomes.csv')
 if k=='8R9d':
  f=next(f for f in read('score_projects/8R9d/allfiles.json')if f['attributes']['name'].startswith('Transparency Trail'));evid=f['links']['download'];txt=str(R/'score_projects/8R9d'/f['attributes']['name'])+'.txt';summary='Transparency trail: old SemNet functions required replacements and 30 original code lines were removed; claim r1zw73 then gives t=2.9574, p=.003246 versus reported t=-3.53, p=.007, which the analyst says may reflect those changes.';why=[] if data and code and b and b<5e9 else['Open original package completeness or size not verified'];note='Twenty assessed claims. Version/repair confounding supports abstention provisionally, not a confirmed P1 discrepancy. Source updated script is Version ID 3; original versions must be pinned.';rt='estimated 30-120 min; not timed'
 else:
  pairs=[]
  for a,bb,label in [('orig_sample_size_value','repro_sample_size_value','N'),('orig_stat_value','repro_stat_value','statistic'),('orig_coef_value','repro_coef_value','coefficient'),('orig_p_value','repro_p_value','p')]:
   if o.get(a)not in [None,'NA','']and c.get(bb)not in [None,'NA','']:
    if label=='p' and c[bb]=='0':continue
    bound='<' if label=='p' and o.get('orig_p_value_type')=='less-than' else ''
    pairs.append(f'{label} {bound}{o[a]} versus {c[bb]}')
  
  if stmap[k]==I and o.get('orig_effect_size_value_repro') not in [None,'NA',''] and c.get('repro_effect_size_value') not in [None,'NA','']:
   pairs.append(f'effect-size field {o["orig_effect_size_value_repro"]} versus {c["repro_effect_size_value"]}')
  summary=f'SCORE {c["claim_id"]}: {c["repro_type"]}, source outcome {c["repro_outcome_overall"]}; '+('; '.join(pairs)if pairs else'no reported/recomputed numerical pair in this joined record')+'.';why=[scwhy[k]];note=f'{x["n"]} version-of-record claims: {x["outcomes"]}. Read analyst data.RData objects orig_outcomes/repro_outcomes; no source rating is imported as a paper-wide verdict.';rt='not established within 2 h'
 if not maps.get(cid):
  urls=re.findall(r'https?://[^\s"<>]+',x['availability'].get('data_location_description',''));maps[cid]=[u.rstrip(').')for u in urls[:1]]
 eligible=not why;rows.append(dict(cand_id=cid,source='SCORE',source_record_id=k,doi=(x.get('doi')or''),title=x['title'],year=x['year'],discipline=(x.get('discipline')or'psychology').lower(),language=lang,language_ok=str(lang in ['R','Python','R; Python']).lower(),package_url=' | '.join(maps.get(cid,[])),package_size_mb=f'{b/1e6:.3f}'if b else'',est_runtime=rt,data_open='true'if data else'unknown',provisional_stratum=stmap[k],evidence_summary=summary,evidence_url=evid,claim_level_evidence='yes'if k not in ['GJe4','LbEB']else('no'if k=='GJe4'else'partial'),eligible=str(eligible).lower(),exclusion_reason='; '.join(why),screener_confidence='medium'if eligible else'low',notes=note));audit[cid]={'textpath':txt,'claim_id':c['claim_id']}
rows.sort(key=lambda x:(x['source'],x['cand_id']))
assert len(rows)==90,len(rows)
seen={}
for x in rows:
 d=x['doi'].lower().strip()
 assert not d or d not in seen,(d,seen.get(d),x['cand_id'])
 seen[d]=x['cand_id']
 assert x['evidence_url'].startswith('https://')
 assert not any('\n'in str(y)or'\r'in str(y)for y in x.values())
with (O/'candidates.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(R/'candidate_audit.json').write_text(json.dumps(audit,indent=2));(R/'candidate_rows.json').write_text(json.dumps(rows,indent=2))
print('ROWS',len(rows));print('ELIGIBLE',collections.Counter(x['provisional_stratum']for x in rows if x['eligible']=='true'));print('EXCLUDED',sum(x['eligible']=='false'for x in rows));print('eligible ids',[(x['cand_id'],x['provisional_stratum'])for x in rows if x['eligible']=='true'])
