import pathlib,json,urllib.request,subprocess,hashlib
R=pathlib.Path('/tmp/scratch_gold/sol')
u='https://huggingface.co/api/datasets/chuxuan/REPRO-Bench';v=json.load(urllib.request.urlopen(u,timeout=25));(R/'hf_dataset_info.json').write_text(json.dumps(v));print('HF',v.get('sha'))
u='https://raw.githubusercontent.com/uiuc-kang-lab/REPRO-Bench/main/ground_truth.json';b=urllib.request.urlopen(u,timeout=25).read();(R/'ground_truth_remote.json').write_bytes(b);print('same groundtruth',json.loads(b)==json.loads(pathlib.Path('/tmp/scratch_gold/src/REPRO-Bench/ground_truth.json').read_text()))
print('code git',subprocess.check_output(['git','-C','/tmp/scratch_gold/src/REPRO-Bench','rev-parse','HEAD'],text=True).strip())
