import csv,pathlib,shutil
p=pathlib.Path('model-gating/gold-set/candidates.csv');backup=pathlib.Path('/tmp/scratch_gold/sol/round1_candidates.csv')
if not backup.exists():shutil.copyfile(p,backup)
rs=list(csv.DictReader(p.open()));fields=list(rs[0]);fields+=[]if 'round'in fields else ['round']
for x in rs:
 x.setdefault('round','1');k=x['cand_id'];extra=''
 if k in ['RB-065','RB-038']:
  x['screener_confidence']='medium';extra='reference reproduction used different software/library; does not show the shipped R code itself was run. Integrator: prefer other success cases in the draw.'
 if k=='SC-8R9d':extra='acceptable_alternative_status=technical failure. Integrator settled: version drift with possibly unavailable original package version is the intended abstention target.'
 if k in ['I4R-bz8pf','I4R-mgy45']:extra='code_format=embedded; integrator caps embedded-code papers at 2 in final 30.'
 if k=='RB-019':extra='acceptable_alternative_status=computational issues (P2/P3 on the one figure); retain reproducible primary status, per integrator.'
 if k=='I4R-eb89k':
  x['notes']=x['notes'].replace('Behavioural genetics/neurodevelopmental-disorder scope needs a second opinion.','Behavioural genetics is in scope (integrator settled).')
  extra='Primary Aims 2 and 3 are blocked, so paper-level technical failure applies; Aim 1 needs edits too. Claim mapping should mark blocked primary claims not_checkable with P0.'
 if k=='I4R-mepbv':extra='Primary manuscript/update analyses do not parse as shipped; paper-level technical failure applies (integrator settled clean P0). Gold refers to downloadable commit 32cfd57c635d08a54a2eff8f735382c3c16336ac, with parse audit retained.'
 if extra and extra not in x['notes']:x['notes']+=' '+extra
with p.open('w',newline='')as f:w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rs)
