import urllib.request,pathlib,json,concurrent.futures,subprocess
R=pathlib.Path('/tmp/scratch_gold/sol/round2_packages')
items=[('cc_spatial.Rmd','https://osf.io/download/fsmkn/'),('cc_spatial.pdf','https://osf.io/download/3c2rx/'),('cc_power.Rmd','https://raw.githubusercontent.com/codecheckers/ZaunerEtAl_PLoS_ONE_2024/main/codecheck/codecheck.Rmd'),('cc_hrv.Rmd','https://raw.githubusercontent.com/codecheckers/wearable-hrv/master/codecheck/codecheck.Rmd'),('cc_circadian.Rmd','https://raw.githubusercontent.com/codecheckers/HeinrichsEtAl_JVis_2026/main/codecheck/codecheck.Rmd'),('cc_funders.yml','https://raw.githubusercontent.com/codecheckers/funders/main/codecheck.yml')]
def run(z):
 n,u=z;p=R/n
 try:
  if not p.exists():p.write_bytes(urllib.request.urlopen(u,timeout=35).read())
  if n.endswith('.pdf'):subprocess.run(['pdftotext','-layout',str(p),str(p)+'.txt'],capture_output=True);return n
  return n,p.read_text()[:12500]
 except Exception as e:return n,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:
 for z in ex.map(run,items):print(z)
