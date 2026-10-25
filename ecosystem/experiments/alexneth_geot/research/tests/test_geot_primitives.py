import math,sys,unittest
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'reference'))
import torch
from geot_primitives import (fold_three,unfold_three,sparsemax,golden_clifford_torus,hamilton,ordered_block_product,
 hyperbolic_quadrance,lorentz_lift_from_spinor,rational_lorentz,triangle_tqf,quaternion_conjugate)

class Tests(unittest.TestCase):
 def test_fold_inverse(self):
  x=torch.randn(2,8,16,16,requires_grad=True)
  y=fold_three(x)
  self.assertEqual(tuple(y.shape),(2,64,4,8))
  self.assertTrue(torch.equal(unfold_three(y),x))
  y.square().sum().backward();self.assertTrue(torch.isfinite(x.grad).all())
 def test_sparsemax(self):
  z=torch.tensor([[2.0,0.0,-10.0],[0.,0.,0.]],requires_grad=True)
  p=sparsemax(z)
  self.assertTrue(torch.allclose(p.sum(-1),torch.ones(2)))
  self.assertEqual(p[0,2].item(),0)
  p.square().sum().backward();self.assertTrue(torch.isfinite(z.grad).all())
 def test_lorentz_and_rational(self):
  q=torch.tensor([[0.6,0.8,0.,0.]],dtype=torch.float64)
  x=lorentz_lift_from_spinor(q)
  self.assertTrue(torch.allclose(x[:,0]**2-(x[:,1:]**2).sum(-1),torch.ones(1,dtype=torch.float64)))
  self.assertEqual(rational_lorentz((Fraction(3,5),Fraction(4,5),0,0)),(Fraction(5,3),Fraction(4,3),0,0))
  self.assertEqual(hyperbolic_quadrance(x,x).item(),0.0)
 def test_golden_torus_not_group(self):
  a=golden_clifford_torus(torch.tensor(0.),torch.tensor(0.))
  b=golden_clifford_torus(torch.tensor(0.),torch.tensor(math.pi/2))
  r1sqr=float(a[0]**2+a[1]**2)
  product=hamilton(a,b)
  self.assertAlmostEqual(float(product.square().sum()),1,places=6)
  self.assertGreater(abs(float(product[0]**2+product[1]**2)-r1sqr),0.02)
 def test_ordered_noncommutative(self):
  theta=math.pi/6
  a=torch.tensor([math.cos(theta),math.sin(theta),0.,0.],dtype=torch.float64)
  b=torch.tensor([math.cos(theta),0.,math.sin(theta),0.],dtype=torch.float64)
  forward=ordered_block_product(torch.stack([a,b]))
  self.assertTrue(torch.allclose(forward,hamilton(b,a)))
  self.assertFalse(torch.allclose(forward,hamilton(a,b)))
  self.assertTrue(torch.allclose(hamilton(forward,quaternion_conjugate(forward)),torch.tensor([1.,0.,0.,0.],dtype=torch.float64)))
 def test_triangle_tqf_name(self):
  self.assertEqual(triangle_tqf((0,0,0),(4,0,0),(0,3,0)),576)

if __name__=='__main__':unittest.main()
