"""Independent consumers of the committed cross-language reference fixtures."""
from pathlib import Path
import hashlib
import importlib.util
import contextlib
import io
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'spec_sync/golden_vectors'


def load(name):
    return json.loads((DIRECTORY / name).read_text())['data']


def multiply(a, b):
    w,x,y,z = a
    v,i,j,k = b
    return [(w*v-x*i-y*j-z*k)//2, (w*i+x*v+y*k-z*j)//2,
            (w*j-x*k+y*v+z*i)//2, (w*k+x*j-y*i+z*v)//2]


class GoldenConformance(unittest.TestCase):
    def test_tiles(self):
        data = load('v1_tiles_forms_0_15.json')
        for record in data['forms']:
            word = int(record['hex'],16)
            self.assertEqual(word >> 56, 0x4d)
            self.assertEqual((word >> 40)&15, record['form'])
            self.assertEqual(word & 0xffffffff,record['decoded']['payload'])
        self.assertEqual(data['forms'][1]['hex'], '4d2461c001ff0101')
        self.assertEqual(data['forms'][3]['hex'], '4d2463c03fc00000')

    def test_unit_table_and_s5(self):
        data = load('v1_hurwitz_and_s5_tree.json')
        units = data['units']
        self.assertEqual(len(units),24)
        for i,a in enumerate(units):
            for j,b in enumerate(units):
                self.assertEqual(multiply(a,b),data['multiplication_table'][i][j])
        s5 = data['s5']
        self.assertEqual(sum(c*c for c in s5['address']),5**len(s5['word']))
        self.assertEqual(s5['address'],s5['path'][-1])
        u,v=data['gram']['u'],data['gram']['v']
        # Lagrange identity: independent 2x2 minors, rather than the Gram code.
        quadrea=4*sum((u[i]*v[j]-u[j]*v[i])**2 for i in range(4) for j in range(i+1,4))
        self.assertEqual(quadrea,data['gram']['quadrea'])

    def test_crt(self):
        data = load('v1_garner_crt_881_883_887.json')
        primes = data['primes']
        self.assertEqual(primes,[881,883,887])
        for row in data['cases']:
            self.assertEqual([row['value']%p for p in primes],row['residues'])
            # Direct CRT using modular exponentiation, independent of Garner.
            modulus=data['modulus']
            value=sum(r*(modulus//p)*pow(modulus//p,-1,p) for r,p in zip(row['residues'],primes))%modulus
            self.assertEqual(value,row['value'])

    def test_chain_and_hash_root(self):
        data = load('v1_quaternion_blockchain_merkle.json')
        self.assertEqual(len(data['states']),720)
        q=data['states'][0]
        for delta,expected in zip(data['deltas'],data['states']):
            q=multiply(delta,q)
            self.assertEqual(q,expected)
        layers=[bytes.fromhex(x) for x in data['layers_hex']]
        tau=hashlib.sha256(layers[-1]).digest()
        for layer in layers[-2::-1]:
            tau=hashlib.sha256(layer+tau).digest()
        self.assertEqual(tau.hex(),data['merkle_root_hex'])
        self.assertEqual(data['gears']['holonomy'],[0,-2,0,0])

    def test_stream_routes(self):
        data = load('v1_64stream_balancer_threading.json')
        self.assertEqual(len(data['streams']),64)
        self.assertTrue(all(data['invariants'].values()))
        for s,name in enumerate(('I','A','A_bar','E')):
            for j,q in enumerate(data['structures'][name]):
                self.assertEqual(data['streams'][str(16*s+j)],q)
        structures=data['structures']
        for j in range(12):
            q=[2,0,0,0]
            for name in ('A','I','A_bar','E'):
                q=multiply(q,structures[name][j])
            self.assertEqual(q,[2,0,0,0])

    def test_generator_detects_missing_and_drift(self):
        spec=importlib.util.spec_from_file_location('vector_generator',ROOT/'spec_sync/generate_golden_vectors.py')
        generator=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(generator,'DIRECTORY',Path(temp)):
                with patch.object(sys,'argv',['generate']), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(generator.main(),0)
                with patch.object(sys,'argv',['generate','--check']), contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(generator.main(),0)
                    path=next(Path(temp).glob('*.json'))
                    original=path.read_bytes()
                    path.write_bytes(original+b' ')
                    self.assertEqual(generator.main(),1)
                    self.assertEqual(path.read_bytes(),original+b' ')
                    path.unlink()
                    self.assertEqual(generator.main(),1)


if __name__ == '__main__':
    unittest.main()
