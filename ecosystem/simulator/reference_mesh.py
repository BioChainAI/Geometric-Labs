#!/usr/bin/env python3
"""Real independent checkout APIs over loopback; ephemeral development HMAC only."""
from __future__ import annotations

import argparse
import json
import secrets
import sys
import threading
from pathlib import Path
from urllib.error import HTTPError

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'tools'))
from upstreams import load


def run_mesh():
    origins = load(['SHD-CCP-core','PolyShard-Agent','Polycentric-Orchestrator','Manifold-Projection'])
    from polyshard_agent import PolyShardAgent
    from polyshard_agent.client import http_get,http_post
    from polycentric import PolycentricOrchestrator
    from polycentric.server import create_local_server
    from shdccp_core.envelope import digest_hex,sign_dev_hmac

    # All parties use an explicitly simulated common reference clock/frame.
    now = 1_800_000_000_000_000_000
    core = PolycentricOrchestrator(clock_ns=now)
    agents,keys = [],[]
    sentinel = 'PRIVATE-RAG-SENTINEL-NEVER-EXPORT'
    for i in range(3):
        aid = f'polyshard-{i+1:02d}'
        key = secrets.token_bytes(32)
        agent = PolyShardAgent(aid,key,reference_epoch_ns=now)
        agent.rag.add('local-evidence',sentinel,'agent-private')
        core.register_dev_agent(aid,key)
        agents.append(agent)
        keys.append(key)
    server = create_local_server(core)
    if server.server_address[0] != '127.0.0.1':
        server.server_close()
        raise AssertionError('reference service must bind only to loopback')
    thread = threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    url = f'http://127.0.0.1:{server.server_port}'
    rejected = {}

    def expect_rejected(name,event,reason,path='/v1/observations'):
        before = len(core.memory.events)
        try:
            http_post(url+path,event)
        except HTTPError as error:
            body = json.loads(error.read())
            if error.code != 403 or body.get('error') != reason:
                raise AssertionError(f'{name}: wrong refusal {error.code} {body}')
        else:
            raise AssertionError(name+': unexpectedly admitted')
        if len(core.memory.events) != before:
            raise AssertionError('rejected event mutated accepted memory')
        rejected[name] = reason

    def resign(event):
        event = dict(event)
        event.pop('event_id',None)
        event.pop('dev_mac',None)
        event['event_id'] = digest_hex(event)
        event['dev_mac'] = sign_dev_hmac(event,keys[0])
        return event

    def fresh():
        return agents[0].observe(scene_id='geom-lab-triangle',point=(0,0,0),claim='reference sample')

    try:
        events = []
        for agent,point in zip(agents,((0,0,0),(4,0,0),(0,3,0))):
            handshake = http_post(url+'/v1/handshake',{'agent_id':agent.agent_id})
            if not handshake['accepted'] or handshake['protocol'] != 'SHDCCP-EINSTEIN-1':
                raise AssertionError('upstream protocol handshake mismatch')
            event = agent.observe(scene_id='geom-lab-triangle',point=point,claim='cubic reference sample')
            if sentinel in json.dumps(event):
                raise AssertionError('private RAG exported')
            if not http_post(url+'/v1/observations',event)['admitted']:
                raise AssertionError('reference observation rejected')
            events.append(event)
        expect_rejected('duplicate_replay',events[0],'duplicate_event')
        tampered = dict(events[0],claim='tampered')
        expect_rejected('tamper',tampered,'dev_mac_invalid')
        mutations = [
            ('sequence_replay',{'seq':1},'sequence_replay'),
            ('wrong_protocol',{'protocol_id':'WRONG-PROFILE'},'protocol_incompatible'),
            ('wrong_form',{'tile_hex':'0000000000000000'},'reference_only_accepts_form3'),
            ('denied_purpose',{'purpose':'private_rag_export'},'purpose_denied'),
            ('missing_consent',{'consent_scopes':[]},'consent_missing'),
            ('unknown_frame',{'frame_id':'unregistered-frame'},'unknown_frame_transform')]
        for name,change,reason in mutations:
            event = fresh()
            event.update(change)
            expect_rejected(name,resign(event),reason)
        for name,change,reason in (
            ('clock_uncertainty',{'uncertainty_ns':100_000_000},'clock_uncertainty'),
            ('clock_skew',{'epoch_ns':now+10_000_000_000},'clock_skew')):
            event = fresh()
            event['time'] = dict(event['time'],**change)
            expect_rejected(name,resign(event),reason)
        expect_rejected('unregistered_agent',{'agent_id':'unknown'},'unregistered_agent',path='/v1/handshake')
        scene = http_get(url+'/v1/scenes/geom-lab-triangle')
        if scene['perspectives'] != 3 or scene['tqf_triad']['area16'] != 576 or not core.memory.verify():
            raise AssertionError('scene/TQF/memory integrity mismatch')
        if sentinel in json.dumps(scene) or any(sentinel in json.dumps(event) for event in core.memory.events):
            raise AssertionError('private RAG leaked into shared state')
        if any('time' not in event or 'frame_id' not in event for event in core.memory.events):
            raise AssertionError('source metadata lost')
        return {'schema':'biochain.reference-mesh-report.v1','status':'PASS',
                'perspectives':3,'accepted_events':len(core.memory.events),'tqf_area16':576,
                'negative_fixtures':rejected,'private_rag_exported':False,'memory_root':scene['memory_root'],
                'import_origins':origins,'transport':'loopback-only HTTP; ephemeral development HMAC',
                'clock':'simulated reference epoch; world frame pre-agreed',
                'limitations':['no CubiLoom persistence/replication','no production identity or TLS',
                               'replay state in memory only','upstream handshake has protocol ID but no semantic-profile negotiation',
                               'frame certificates have no expiry contract; deferred to owning-repo wave']}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
        for agent in agents:
            agent.rag.db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    report = run_mesh()
    serialized = json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(serialized)
    print(serialized,end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
