#!/usr/bin/env python3
"""Synthetic vision→Tile sidecar→real independent agents→loopback orchestrator.

Three points are explicitly synthetic fixtures, not inferred scene geometry.
The current upstream receiver is a generic envelope consumer; visual schema
validation is local and its missing remote enforcement is reported explicitly.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import secrets
import sys
import tempfile
import threading
from urllib.error import HTTPError

BASE=Path(__file__).resolve().parents[1]
ECOSYSTEM=BASE.parents[1]
sys.path.insert(0,str(BASE/'src'))
sys.path.insert(0,str(ECOSYSTEM/'tools'))


def run():
    import torch
    from alexneth_geot.model import AlexNetHGEOT
    from alexneth_geot.observations import descriptor,validate
    from upstreams import load
    origins=load(['SHD-CCP-core','PolyShard-Agent','Polycentric-Orchestrator','Manifold-Projection'])
    from polyshard_agent import PolyShardAgent
    from polyshard_agent.client import http_post,http_get
    from polycentric import PolycentricOrchestrator
    from polycentric.server import create_local_server
    from shdccp_core.envelope import digest_hex,sign_dev_hmac
    from shdccp_core.tile import unpack
    torch.manual_seed(20261025);torch.set_num_threads(2)
    model=AlexNetHGEOT().eval()
    checkpoint=io.BytesIO();torch.save(model.state_dict(),checkpoint)
    model_digest=hashlib.sha256(checkpoint.getvalue()).hexdigest()
    core=PolycentricOrchestrator(clock_ns=1_800_000_000_000_000_000)
    server=create_local_server(core)
    if server.server_address[0]!='127.0.0.1':raise AssertionError('nonlocal binding')
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    url=f'http://127.0.0.1:{server.server_port}'
    agents=[];tiles=[];blob_sizes=[];first_event=None
    try:
        with tempfile.TemporaryDirectory(prefix='geot-local-artifacts-') as temporary:
            for index,point in enumerate(((0,0,0),(4,0,0),(0,3,0))):
                key=secrets.token_bytes(32)
                agent=PolyShardAgent(f'geot-{index}',key,reference_epoch_ns=core.clock_ns)
                agents.append(agent);core.register_dev_agent(agent.agent_id,key)
                agent.rag.add('private','DO-NOT-EXPORT-PRIVATE-RAG','test-local')
                h=http_post(url+'/v1/handshake',{'agent_id':agent.agent_id})
                if not h['accepted']:raise AssertionError('handshake failed')
                with torch.no_grad():output=model(torch.randn(1,3,224,224))
                record,blob=descriptor(output['tokens'][0],model_digest,purpose='visual_reference',
                                      consent=['visual_descriptor_share'],source_ref=f'synthetic:image-{index}')
                artifact=Path(temporary)/record['tensor']['sha256'];artifact.write_bytes(blob)
                validate(record,artifact.read_bytes());blob_sizes.append(len(blob))
                # The synthetic point exists solely to exercise existing spatial APIs.
                event=agent.observe(scene_id='geot-synthetic-fixture',point=point,
                     claim='untrained visual descriptor; synthetic fixture point, not inferred pose')
                event.pop('event_id');event.pop('dev_mac')
                event['visual_observation']=record
                event['coordinate_status']='synthetic-test-fixture-not-camera-calibration'
                event['event_id']=digest_hex(event);event['dev_mac']=sign_dev_hmac(event,key)
                tile=bytes.fromhex(event['tile_hex']);fields=unpack(tile)
                if fields['form_id']!=3:raise AssertionError('unexpected Tile form')
                tiles.append(tile.hex())
                if 'DO-NOT-EXPORT-PRIVATE-RAG' in json.dumps(event):raise AssertionError('private RAG leaked')
                receipt=http_post(url+'/v1/observations',event)
                if not receipt['admitted']:raise AssertionError('event rejected')
                stored=core.memory.events[-1]
                if stored['visual_observation']!=record or stored['time']!=event['time'] or stored['frame_id']!=event['frame_id']:
                    raise AssertionError('sidecar/source context lost')
                first_event=first_event or event
            scene=http_get(url+'/v1/scenes/geot-synthetic-fixture')
            if scene['perspectives']!=3 or scene['tqf_triad']['area16']!=576:raise AssertionError('fixture scene mismatch')
            for name,event,reason in (
                ('replay',first_event,'duplicate_event'),
                ('tampered_sidecar',dict(first_event,visual_observation={'schema':'tampered'}),'dev_mac_invalid')):
                try:http_post(url+'/v1/observations',event)
                except HTTPError as error:
                    if error.code!=403 or json.loads(error.read())['error']!=reason:raise AssertionError(name)
                else:raise AssertionError(name+' was admitted')
            if not core.memory.verify() or len(core.memory.events)!=3:raise AssertionError('memory changed on rejection')
            return {'schema':'alexneth-geot.reference-interop-report.v1','status':'PASS_REFERENCE_INTEROP',
                    'torch':torch.__version__,'python':sys.version.split()[0],'device':'cpu','trained':False,
                    'parameters':sum(p.numel() for p in model.parameters()),'classes':10,
                    'tensor_shapes':{'input':[1,3,224,224],'tokens':[1,64,64],'spinors':[1,64,4],'routing':[1,64,7],'semantic':[1,64]},
                    'descriptor_bytes_per_agent':blob_sizes,'accepted_visual_sidecars':3,'tile_form_id':3,
                    'tile_hex':tiles,'tile_byte_order':'big-endian','tensor_byte_order':'little-endian-declared',
                    'fixture_triangle_tqf':576,'fixture_coordinates_are_predicted':False,
                    'negative_http_fixtures':['replay','tampered_sidecar'],'private_rag_exported':False,
                    'independent_import_origins':origins,'remote_visual_schema_enforced':False,
                    'production_ready':False,'gaps':['remote profile/purpose validation for the visual sidecar needs an upstream API',
                    'CubiLoom persistence/replication absent','FractalOS tensor-job implementation absent',
                    'original AlexNet-H weights/baseline source absent','GPU/Loihi/QEMU untested']}
    finally:
        server.shutdown();server.server_close();thread.join(timeout=2)
        for agent in agents:agent.rag.db.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args();report=run();text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    print(text,end='');return 0


if __name__=='__main__':raise SystemExit(main())
