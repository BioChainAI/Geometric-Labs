"""Experimental sidecars: tensor references, never a new normative Tile form."""
import hashlib
import math
import re
import struct

SCHEMA='biochain.experimental.visual-observation.v1'
PROFILE='alexneth-geot-latent-v0.2'


def descriptor(tensor,model_digest,*,purpose,consent,source_ref):
    if purpose!='visual_reference' or 'visual_descriptor_share' not in consent:
        raise PermissionError('visual descriptor export requires explicit purpose and consent')
    if not re.fullmatch('[0-9a-f]{64}',model_digest) or not isinstance(source_ref,str) or not source_ref:
        raise ValueError('checkpoint/artifact digest and source reference required')
    if tensor.ndim!=2 or tensor.shape[0]!=64 or not 1<=tensor.shape[1]<=256:
        raise ValueError('64-cell bounded-size token matrix required')
    values=tensor.detach().cpu().float().contiguous().flatten().tolist()
    if any(not math.isfinite(v) for v in values):raise ValueError('nonfinite descriptor')
    blob=struct.pack('<'+'f'*len(values),*values)
    record={'schema':SCHEMA,'semantic_profile_id':PROFILE,'wire_format_id':'einstein-tile/1',
            'tile_semantic_profile_id':'shdccp-proposed-v1','supported_tile_form_ids':[3],
            'tensor':{'sha256':hashlib.sha256(blob).hexdigest(),'dtype':'float32','byte_order':'little-endian',
                      'shape':list(tensor.shape),'layout':'voxel-major-contiguous','bytes':len(blob)},
            'representation':'learned-latent-cube-not-physical-xyz','model_digest':model_digest,
            'source_ref':source_ref,'purpose':purpose,'consent_scopes':list(consent),
            'implementation_status':'untrained-reference','numeric_status':'approximate-float32'}
    validate(record,blob)
    return record,blob


def validate(record,blob):
    if record.get('schema')!=SCHEMA or record.get('semantic_profile_id')!=PROFILE:
        raise ValueError('unknown visual sidecar schema/profile')
    if record.get('wire_format_id')!='einstein-tile/1' or record.get('tile_semantic_profile_id')!='shdccp-proposed-v1' or record.get('supported_tile_form_ids')!=[3]:
        raise ValueError('unsupported wire/tile profile')
    if record.get('purpose')!='visual_reference' or 'visual_descriptor_share' not in record.get('consent_scopes',[]):
        raise PermissionError('export policy denied')
    t=record['tensor']
    shape=t['shape']
    if len(shape)!=2 or any(type(n) is not int for n in shape) or shape[0]!=64 or not 1<=shape[1]<=256:
        raise ValueError('invalid bounded tensor shape')
    if (t['dtype'],t['byte_order'],t['layout'])!=('float32','little-endian','voxel-major-contiguous'):
        raise ValueError('tensor encoding mismatch')
    expected=shape[0]*shape[1]*4
    if len(blob)!=expected or t['bytes']!=expected or hashlib.sha256(blob).hexdigest()!=t['sha256']:
        raise ValueError('tensor integrity/size mismatch')
    if any(not math.isfinite(v[0]) for v in struct.iter_unpack('<f',blob)):
        raise ValueError('nonfinite tensor payload')
    if not re.fullmatch('[0-9a-f]{64}',record.get('model_digest','')):
        raise ValueError('missing model digest')
    return True
