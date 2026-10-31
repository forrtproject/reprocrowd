import pathlib,json,urllib.request,urllib.parse,difflib,re,concurrent.futures
r=pathlib.Path('/tmp/scratch_gold/sol');v=json.loads((r/'report_index.json').read_text())+json.loads((r/'round2_remaining_index.json').read_text());keys=['82c6v','axj5y','cyb24','nh568','td79f','vkgtf','a8kp5','rvynd','xfc2m','u6gea','63qe2'];items={x['node']:x['title']for x in v if x['node']in keys};items.update({'RB111':'Taste-Based Gender Favouritism in High-Stake Decisions: Evidence from The Price is Right','CC2023004':'Does spatial thinking ability relate to performance when using web-mapping services? A survey with digital natives'})
def norm(s):return ' '.join(re.findall('[a-z0-9]+',s.lower()))
def run(z):
 k,t=z;d=r/'round2_packages'/f'metadata_{k}.json'
 try:
  if not d.exists():d.write_bytes(urllib.request.urlopen('https://api.crossref.org/works?rows=3&query.title='+urllib.parse.quote(t),timeout=30).read())
  v=json.loads(d.read_text());score,x=max((difflib.SequenceMatcher(None,norm(t),norm(x.get('title',[''])[0])).ratio(),x)for x in v['message']['items']);return k,dict(query=t,score=score,doi=x['DOI'],title=x['title'],date=x.get('published'),journal=x.get('container-title'))
 except Exception as e:return k,dict(error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as ex:out=dict(ex.map(run,items.items()))
(r/'round2_metadata_matches.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
