import json,pathlib,re
R=pathlib.Path('/tmp/scratch_gold/sol');idx=json.loads((R/'report_index.json').read_text());rr=json.loads((R/'i4r_reports.json').read_text()); ps=[x for x in idx if x['journal']=='Psychological Science']; nh=['z5pjq','kwqj6','vdm68','2ar74','9qa3x','4wxms','eb89k','p8f7d','f5p78','3qs8e','8dxvk','kyufb'];out=ps+[x for x in idx if x['node'] in nh]
# 4wxms had an old report URL overwritten in index: recover from current corpus.
if not any(x['node']=='4wxms'for x in out):
 x=next(x for x in rr if (x.get('reportUrl')or'').rstrip('/').endswith('/4wxms')); p=next((R/'osf/4wxms').glob('*.pdf.txt')); fs=json.loads((p.parent/'allfiles.json').read_text());f=next(f for f in fs if f['id']==p.name.split('.')[0]);out.append(dict(x,node='4wxms',textpath=str(p),evidence_url=f['links']['download'],osf_links=[]))
(R/'selection_i4r.json').write_text(json.dumps(out));print('selected I4R',len(out))
