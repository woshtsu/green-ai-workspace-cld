import json,subprocess
from pathlib import Path
root=Path.cwd(); results=[]
def git(p,*args):
 r=subprocess.run(['git','-C',p,*args],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=100)
 return r.returncode,(r.stdout+r.stderr).strip()
for p in json.loads((root/'output/traspaso-claude/repos.json').read_text()):
 entry={'path':p}
 for key,args in [('branch',['branch','--show-current']),('before',['rev-parse','HEAD']),('status',['status','--short']),('upstream',['rev-parse','--abbrev-ref','@{upstream}'])]: entry[key]=git(p,*args)[1]
 code,msg=git(p,'fetch','--all','--prune');entry['fetch']={'code':code,'output':msg}
 if code==0:
  code,msg=git(p,'pull','--ff-only');entry['pull']={'code':code,'output':msg}
 entry['after']=git(p,'rev-parse','HEAD')[1];results.append(entry)
 (root/'output/traspaso-claude/actualizacion-repos.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
 print(Path(p).name,entry['branch'],entry.get('pull',entry['fetch']),flush=True)
