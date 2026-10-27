#!/usr/bin/env python3
"""Capture command exit codes and exact test totals; never overwrite test fixtures."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=BASE/'evidence/wave01')
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    commands = [
        ('baseline',['make','verify-all']),
        ('pillars',['make','test-pillars']),
        ('vectors',['make','check-vectors']),
        ('ecosystem-unit',['make','-C','ecosystem','test']),
        ('geometry',['make','-C','ecosystem','geometry']),
        ('doctor',[sys.executable,'ecosystem/tools/glab.py','doctor']),
        ('sync-repeat',[sys.executable,'ecosystem/tools/glab.py','sync','--require-lock']),
        ('check-lock',[sys.executable,'ecosystem/tools/glab.py','check-lock']),
        ('integration',['make','-C','ecosystem','integration']),
        ('protocol',[sys.executable,'ecosystem/tools/protocol_compatibility.py','--output',str(args.output_dir/'protocol-compatibility.json')]),
        ('demo',[sys.executable,'ecosystem/simulator/reference_mesh.py','--output',str(args.output_dir/'reference-mesh.json')]),
        ('diff-check',['git','diff','--check'])]
    outcomes = []
    for name,command in commands:
        result = subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True)
        log = result.stdout+result.stderr
        (args.output_dir/(name+'.log')).write_text(log)
        counts = [int(n) for n in re.findall(r'Ran (\d+) tests?',log)]
        outcome = {'name':name,'command':command,'returncode':result.returncode,
                   'status':'PASS' if result.returncode==0 else 'FAIL','test_counts':counts,
                   'log':name+'.log'}
        outcomes.append(outcome)
        print(name,outcome['status'],counts,flush=True)
    sources = [p for parent in ('tools','simulator','tests','integration_tests','manifest','locks','contracts')
               for p in (BASE/parent).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    report = {'schema':'biochain.ecosystem-acceptance-report.v1',
              'validation_base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
              'python':platform.python_version(),'platform':platform.platform(),
              'status':'PASS' if all(r['returncode']==0 for r in outcomes) else 'FAIL',
              'commands':outcomes,'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources)},
              'not_executed':['Python runtimes other than the recorded version','actual 32-bit host','Docker','GPU/H100','Loihi2','QEMU','production identity','CubiLoom persistence/replication']}
    (args.output_dir/'acceptance.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    return 0 if report['status']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
