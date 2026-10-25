#!/usr/bin/env python3
"""Validate/describe the proposal; deliberately provides no fake training entrypoint."""
import argparse
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((BASE/name).read_text())


def validate(experiments, scaffold, flow):
    if experiments['schema'] != 'get-alexnet.experiment-plan.v1' or experiments['status'] != 'proposed-not-trained':
        raise ValueError('wrong experiment version/status')
    variants = experiments['variants']
    ids = [v['id'] for v in variants]
    if len(ids) != len(set(ids)) or set(ids) != {'E0','E1','H1','H2','Q1','QH1','T1','X1'}:
        raise ValueError('missing or duplicate experiment IDs')
    if experiments['input']['shape'] != ['N',3,224,224]:
        raise ValueError('reference input convention changed')
    dimension = experiments['embedding_dimension']
    seeds = experiments['seeds']
    if type(dimension) is not int or dimension <= 0 or len(seeds)<3 or len(set(seeds)) != len(seeds) or any(type(s) is not int for s in seeds):
        raise ValueError('positive dimension and three unique integer seeds required')
    numerics = experiments['numerics']
    lo,hi = numerics['curvature_bounds']
    c = numerics['curvature_fixed']
    if any(type(v) not in (int,float) or not math.isfinite(v) for v in (lo,c,hi)) or not 0 < lo < c < hi:
        raise ValueError('finite positive curvature bounds required')
    if experiments['comparison']['test_split_for_selection'] or experiments['comparison']['results'] is not None:
        raise ValueError('plan must not claim results or select on the test split')
    parents = {v['id']:v['compare_to'] for v in variants}
    for node in parents:
        seen = set()
        current = node
        while current is not None:
            if current in seen or current not in parents:
                raise ValueError('unknown or cyclic experiment comparator')
            seen.add(current)
            current = parents[current]
    paths = set()
    if scaffold['schema'] != 'get-alexnet.scaffold-plan.v1' or scaffold['status'] != 'proposed':
        raise ValueError('wrong scaffold version/status')
    for area in scaffold['areas']:
        if area['implementation_status'] != 'not-implemented' or not area['acceptance']:
            raise ValueError('proposed component must have honest status and acceptance')
        for name in area['proposed_files']:
            path = Path(name)
            if path.is_absolute() or '..' in path.parts or name in paths:
                raise ValueError('unsafe or duplicate proposed path')
            paths.add(name)
    if flow['schema'] != 'get-alexnet.flow-plan.v1' or flow['status'] != 'proposed':
        raise ValueError('wrong flow version/status')
    nodes = [n['id'] for n in flow['nodes']]
    if len(nodes) != len(set(nodes)):
        raise ValueError('duplicate flow node')
    for edge in flow['edges']:
        if edge['source'] not in nodes or edge['target'] not in nodes or not edge['contract']:
            raise ValueError('dangling or untyped flow edge')
    return {'status':'VALID_PROPOSAL','model_implemented':False,'training_executed':False,
            'experiment_variants':len(variants),'proposed_source_files':len(paths),
            'flow_nodes':len(nodes),'flow_edges':len(flow['edges'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['validate','list','flow'])
    args = parser.parse_args()
    experiments = read('configs/experiments.v1.json')
    scaffold = read('contracts/scaffold.v1.json')
    flow = read('contracts/flow.v1.json')
    result = validate(experiments,scaffold,flow)
    if args.command == 'list':
        result = {'status':'PROPOSED', 'variants':experiments['variants'],'areas':scaffold['areas']}
    elif args.command == 'flow':
        result = flow
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
