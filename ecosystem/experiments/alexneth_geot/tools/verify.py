#!/usr/bin/env python3
"""Capture actually executed local CPU/model/ecosystem checks without fixture writes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[2]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=BASE/'evidence')
    args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    cases=[('root-baseline',['make','verify-all']),
           ('ecosystem-offline',['make','-C','ecosystem','test']),
           ('ecosystem-integration',['make','-C','ecosystem','integration']),
           ('research-primitives',[sys.executable,'-m','unittest','discover','-s',str(BASE/'research/tests'),'-v']),
           ('geot-tests',[sys.executable,'-m','unittest','discover','-s',str(BASE/'tests'),'-v']),
           ('protocol-gate',[sys.executable,'ecosystem/tools/protocol_compatibility.py','--output',str(args.output_dir/'protocol.json')]),
           ('vision-interop',[sys.executable,str(BASE/'tools/interop.py'),'--output',str(args.output_dir/'interop.json')]),
           ('release-lock',[sys.executable,'ecosystem/tools/glab.py','check-lock'])]
    expected_counts={'root-baseline':40,'ecosystem-offline':23,'ecosystem-integration':4,'research-primitives':6,'geot-tests':16}
    results=[]
    for name,command in cases:
        result=subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True)
        log=result.stdout+result.stderr
        (args.output_dir/(name+'.log')).write_text(log)
        counts=[int(n) for n in re.findall(r'Ran (\d+) tests?',log)]
        mismatch=name in expected_counts and counts!=[expected_counts[name]]
        results.append({'name':name,'command':command,'command_returncode':result.returncode,
                        'returncode':result.returncode or int(mismatch),'test_counts':counts,
                        'count_mismatch':mismatch,'log':name+'.log'})
        print(name,'PASS' if results[-1]['returncode']==0 else 'FAIL',counts,flush=True)
    source_files=[p for section in ('src','tests','tools') for p in (BASE/section).rglob('*.py') if '__pycache__' not in p.parts]
    report={'schema':'alexneth-geot.validation.v1','status':'PASS' if all(r['returncode']==0 for r in results) else 'FAIL',
            'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
            'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'dependency_snapshot_sha256':hashlib.sha256((BASE/'requirements-cpu-py312.txt').read_bytes()).hexdigest(),
            'checks':results,'unique_unittest_methods':sum(sum(r['test_counts']) for r in results),
            'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source_files)},
            'limits':['untrained synthetic CPU reference only','original claimed v0.1 baseline unavailable',
                      'GPU/Loihi/QEMU not executed','remote visual-sidecar semantic validation not implemented',
                      'no CubiLoom storage or FractalOS tensor backend']}
    (args.output_dir/'validation.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    return 0 if report['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
