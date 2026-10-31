import urllib.request,urllib.parse,pathlib,json,concurrent.futures,re,unicodedata,difflib
R=pathlib.Path('/tmp/scratch_gold/sol');sel=json.loads((R/'selection_i4r.json').read_text())
extra={1:'Antinormative Messaging, Group Cues, and the Nuclear Ban Treaty',4:'Black Workers in White Places: Daytime Racial Diversity and White Public Opinion',10:'Can’t We All Just Get Along? How Women MPs Can Ameliorate Affective Polarization in Western Publics',11:'Changing Hearts and Minds? Why Media Messages Designed to Foster Empathy Often Fail',12:'Changing Tides: Public Attitudes on Climate Migration',19:'Do Transitional Justice Museums Persuade Visitors? Evidence from a Field Experiment',23:'Effective for Whom? Ethnic Identity and Nonviolent Resistance',25:'Entertaining Beliefs in Economic Mobility',29:'Flight to Safety: COVID-Induced Changes in the Intensity of Status Quo Preference and Voting Behavior',32:'Hate Crimes and Gender Imbalances: Fears over Mate Competition and Violence against Refugees',36:'Ideological Asymmetries and the Determinants of Politically Motivated Reasoning',38:'Indecent Disclosures: Anticorruption Reforms and Political Selection',49:'Multiracial Identity and Political Preferences',53:'Playing Politics with Environmental Protection: The Political Economy of Designating Protected Areas',58:'Re-Assessing Elite-Public Gaps in Political Behavior',69:'Talking Shops: The Effects of Caucus Discussion on Policy Coalitions',81:'The Morning After: Cabinet Instability and the Purging of Ministers after Failed Coup Attempts in Autocracies',91:'What Makes Anticorruption Punishment Popular? Individual-Level Evidence from China',94:'Yellow Vests, Pessimistic Beliefs, and Carbon Tax Aversion',112:'The PhD Pipeline Initiative Works: Evidence from a Randomized Intervention to Help Underrepresented Students Prepare for PhDs in Political Science'}
(R/'hf_titles.json').write_text(json.dumps(extra))
items=[(x['node'],x['title'])for x in sel]+[(f'hf{k}',t)for k,t in extra.items()]
def norm(s):return ' '.join(re.findall('[a-z0-9]+',unicodedata.normalize('NFKD',s.lower())))
def get(item):
 k,t=item;p=R/f'metadata/{k}.json';p.parent.mkdir(exist_ok=True)
 try:
  if p.exists():v=json.loads(p.read_text())
  else:
   u='https://api.crossref.org/works?rows=3&query.title='+urllib.parse.quote(t)
   r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ReproCrowd-candidate-screening/1.0'}),timeout=40);v=json.load(r);p.write_text(json.dumps(v))
  scored=[(difflib.SequenceMatcher(None,norm(t),norm(x.get('title',[''])[0])).ratio(),x)for x in v['message']['items']];score,x=max(scored,key=lambda z:z[0]);return k,dict(query=t,match_score=score,title=x.get('title',[''])[0],doi=x['DOI'],date=x.get('published',{}).get('date-parts'),url=x.get('URL'),journal=x.get('container-title'),crossref_url='https://api.crossref.org/works/'+urllib.parse.quote(x['DOI'],safe=''))
 except Exception as e:return k,{'query':t,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as ex:out=dict(ex.map(get,items))
(R/'metadata_matches.json').write_text(json.dumps(out));print('metadata',len(out),'low matches',[(k,x)for k,x in out.items()if x.get('match_score',0)<.88])
