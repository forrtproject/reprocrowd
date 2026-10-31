import pathlib,csv,collections,json,re
R=pathlib.Path('/tmp/scratch_gold/sol');r=R/'score'
def read(n):return list(csv.DictReader((r/(n+'.csv')).open()))
meta={x['paper_id']:x for x in read('paper_metadata')};pr={x['paper_id']:x for x in read('pr_outcomes')}; rr={x['rr_id']:x for x in read('rr_internal_tracking')};orig={(x['paper_id'],x['claim_id']):x for x in read('orig_outcomes')}
g=collections.defaultdict(list)
for x in read('repro_outcomes'):
 if x['repro_version_of_record']=='TRUE':g[x['paper_id']].append(x)
out=[]
for k,v in g.items():
 p=pr.get(k,{});m=meta.get(k,{})
 z={'id':k,'title':m.get('title'),'doi':m.get('DOI'),'year':m.get('pub_year'),'discipline':m.get('COS_pub_category'),'n':len(v),'outcomes':dict(collections.Counter(x['repro_outcome_overall'] for x in v)),'types':dict(collections.Counter(x['repro_type'] for x in v)),'availability':p,'projects':[rr.get(i,{}) for i in set(x['rr_id'] for x in v)],'claims':[dict(x,original=orig.get((k,x['claim_id']),{})) for x in v]};out.append(z)
(R/'score_summary.json').write_text(json.dumps(out))
for x in out:
 p=x['availability']
 if p.get('OA_data_shared')=='available_online' or p.get('OA_code_shared')=='available_online':
  print(x['id'],x['n'],x['outcomes'],x['types'], x['title']);print(' ',x['doi'],p.get('restricted_data'),p.get('OA_data_shared'),p.get('OA_code_shared'),[i.get('project_guid') for i in x['projects']]);print(' ',p.get('code_notes','')[:200],p.get('data_location_description','')[:200])
