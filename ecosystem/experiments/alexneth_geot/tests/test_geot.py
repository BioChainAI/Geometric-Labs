import copy
from fractions import Fraction as F
import importlib.util
from pathlib import Path
import sys
import unittest

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
import torch
from torch.autograd import gradcheck
from alexneth_geot.primitives import fold_three,unfold_three,lorentz_lift_from_spinor,hyperbolic_quadrance,sparsemax,triangle_tqf
from alexneth_geot import oracle
from alexneth_geot.model import AlexNetHGEOT,FoldedTriQuad,LocalRouter,neighbors64,semantic_exp0
from alexneth_geot.observations import descriptor,validate

torch.set_num_threads(2)


class Geometry(unittest.TestCase):
    def test_fold_supported_types_noncontiguous_and_gradients(self):
        for dtype in (torch.float32,torch.float64,torch.int64,torch.uint8,torch.bool):
            x=torch.arange(2*3*16*16).reshape(2,3,16,16).to(dtype).transpose(2,3)
            self.assertTrue(torch.equal(unfold_three(fold_three(x)),x))
        x=torch.randn(1,1,4,2,dtype=torch.float64,requires_grad=True)
        self.assertTrue(gradcheck(fold_three,(x,)))

    def test_fold_invalid(self):
        with self.assertRaises(ValueError):fold_three(torch.zeros(1,2,6,3))

    def test_three_distinct_quadrances(self):
        self.assertEqual(triangle_tqf((0,0,0),(4,0,0),(0,3,0)),576)
        mixer=FoldedTriQuad().double()
        self.assertEqual(mixer(torch.ones(1,8,1,1,dtype=torch.float64)).flatten().tolist(),[1,1,1])
        x=oracle.lorentz((F(3,5),F(4,5),0,0))
        self.assertEqual(oracle.hyperbolic_quadrance(x,x),0)

    def test_exact_rational_simplex(self):
        for values in ((F(2),0,-10),(F(1,10),F(2,10),F(3,10)),(0,0,0)):
            p=oracle.sparsemax(values)
            self.assertEqual(sum(p),1)
            self.assertTrue(all(x>=0 for x in p))
            q=sparsemax(torch.tensor([float(v) for v in values],dtype=torch.float64))
            self.assertTrue(torch.allclose(q,torch.tensor([float(v) for v in p],dtype=torch.float64),atol=1e-12))

    def test_oracle_rejects_floats_and_overflow(self):
        with self.assertRaises(ValueError):oracle.lorentz((.6,.8,0,0))
        with self.assertRaises(ValueError):oracle.lorentz((0,1,0,0))
        with self.assertRaises(OverflowError):oracle.sparsemax((2**300,0))

    def test_lorentz_float_matches_oracle(self):
        a=(F(3,5),F(4,5),0,0);b=(F(3,5),0,F(4,5),0)
        qa,qb=(torch.tensor([float(v) for v in q],dtype=torch.float64) for q in (a,b))
        x,y=lorentz_lift_from_spinor(qa),lorentz_lift_from_spinor(qb)
        expected=oracle.hyperbolic_quadrance(oracle.lorentz(a),oracle.lorentz(b))
        self.assertAlmostEqual(hyperbolic_quadrance(x,y).item(),float(expected),places=12)
        for q in (torch.tensor([0.,1,0,0]),torch.tensor([float('nan'),0,0,0]),torch.ones(4)):
            with self.assertRaises(ValueError):lorentz_lift_from_spinor(q)

    def test_sparsemax_stability_gradcheck_and_invalid(self):
        z=torch.tensor([[.2,.1,-2]],dtype=torch.float64,requires_grad=True)
        self.assertTrue(gradcheck(sparsemax,(z,)))
        self.assertTrue(torch.allclose(sparsemax(z+1e6),sparsemax(z),atol=1e-9))
        with self.assertRaises(ValueError):sparsemax(torch.tensor([float('inf'),1]))
        with self.assertRaises(ValueError):hyperbolic_quadrance(torch.zeros(4),torch.zeros(4))


class NeuralReference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.manual_seed(42)
        cls.model=AlexNetHGEOT().eval()
        cls.image=torch.randn(1,3,224,224)
        with torch.no_grad():cls.output=cls.model(cls.image)

    def test_tensor_contracts(self):
        out=self.output
        self.assertEqual(out['tap_shapes'],[(1,192,27,27),(1,384,13,13),(1,256,13,13)])
        self.assertEqual(out['folded_shape'],(1,128,4,8))
        self.assertEqual(out['tokens'].shape,(1,64,64))
        self.assertEqual(out['weights'].shape,(1,64,7))
        self.assertTrue(torch.all(out['semantic'].norm(dim=-1)<1))
        self.assertTrue(torch.allclose(out['weights'].sum(-1),torch.ones(1,64)))
        self.assertTrue(torch.allclose(out['spinors'].square().sum(-1),torch.ones(1,64),atol=1e-6))
        self.assertTrue(2_500_000<=sum(p.numel() for p in self.model.parameters())<=5_000_000)

    def test_local_periodic_graph(self):
        graph=neighbors64()
        self.assertEqual(graph.shape,(64,7))
        for i,row in enumerate(graph):
            self.assertEqual(row[0].item(),i)
            self.assertEqual(len(set(row.tolist())),7)
            for j in row:self.assertIn(i,graph[j].tolist())

    def test_forward_backward_optimizer_and_equivalent_control(self):
        torch.manual_seed(7)
        m=AlexNetHGEOT()
        optimizer=torch.optim.SGD(m.parameters(),lr=1e-3)
        before=m.classifier.weight.detach().clone()
        output=m(self.image)
        loss=torch.nn.functional.cross_entropy(output['logits'],torch.tensor([2]))+output['semantic'].square().mean()
        loss.backward()
        self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all() for p in m.parameters()))
        optimizer.step()
        self.assertFalse(torch.equal(before,m.classifier.weight))
        control=AlexNetHGEOT(routing='euclidean')
        control.load_state_dict(m.state_dict())
        self.assertEqual(sum(p.numel() for p in m.parameters()),sum(p.numel() for p in control.parameters()))
        self.assertTrue(torch.isfinite(control(self.image)['logits']).all())

    def test_quad_gradients_and_invalid_model_input(self):
        q=FoldedTriQuad().double()
        x=torch.randn(1,8,1,1,dtype=torch.float64,requires_grad=True)
        self.assertTrue(gradcheck(q,(x,)))
        with self.assertRaises(ValueError):self.model(torch.randn(1,3,32,32))

    def test_semantic_zero_gradient_and_interior(self):
        x=torch.zeros(1,64,dtype=torch.float64,requires_grad=True)
        self.assertTrue(gradcheck(semantic_exp0,(x,)))
        semantic_exp0(x).sum().backward()
        self.assertTrue(torch.allclose(x.grad,torch.full_like(x,1-1e-5)))
        self.assertLess(semantic_exp0(torch.full((1,64),100.)).norm().item(),1.)
        with self.assertRaises(ValueError):semantic_exp0(torch.tensor([[float('nan')]]))

    def test_checkpoint_roundtrip(self):
        import io
        buffer=io.BytesIO();torch.save(self.model.state_dict(),buffer);buffer.seek(0)
        restored=AlexNetHGEOT().eval()
        restored.load_state_dict(torch.load(buffer,weights_only=True))
        with torch.no_grad():self.assertTrue(torch.equal(restored(self.image)['logits'],self.output['logits']))

    def test_collapse_monitor(self):
        router=LocalRouter()
        with torch.no_grad():router.state.weight.zero_();router.state.bias.zero_()
        _,q,weights,diagnostics=router(torch.zeros(1,64,64))
        self.assertTrue(torch.isfinite(q).all())
        self.assertAlmostEqual(diagnostics['support_mean'].item(),7)
        self.assertAlmostEqual(diagnostics['self_only_fraction'].item(),0)

    def test_sidecar_integrity_profiles_and_privacy(self):
        kwargs={'purpose':'visual_reference','consent':['visual_descriptor_share'],'source_ref':'synthetic:fixture'}
        record,blob=descriptor(self.output['tokens'][0],'a'*64,**kwargs)
        self.assertTrue(validate(record,blob))
        self.assertNotIn('image',record)
        with self.assertRaises(PermissionError):descriptor(self.output['tokens'][0],'a'*64,**(kwargs|{'consent':[]}))
        with self.assertRaises(ValueError):validate(record,blob[:-1]+bytes([blob[-1]^1]))
        changed=copy.deepcopy(record);changed['semantic_profile_id']='unknown'
        with self.assertRaises(ValueError):validate(changed,blob)


if __name__=='__main__':unittest.main()
