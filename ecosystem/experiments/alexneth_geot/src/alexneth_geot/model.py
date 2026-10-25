"""Multiscale AlexNet → fold3 → cubic local routing; latent, not physical 3D.

Temporary experimental ownership in Geometric-Labs. Stable projection operators
can move upstream after review. Float paths do not claim rational exactness.
"""
import torch
from torch import nn
from torch.nn import functional as F
from .primitives import fold_three,lorentz_lift_from_spinor,hyperbolic_quadrance,sparsemax


def semantic_exp0(tangent):
    """Fixed-c=1 Poincare map with analytic zero derivative and interior margin."""
    if not tangent.is_floating_point() or not torch.isfinite(tangent).all():
        raise ValueError('finite floating tangent required')
    norm=tangent.norm(dim=-1,keepdim=True)
    if not torch.isfinite(norm).all():
        raise ValueError('tangent norm overflow')
    scale=torch.where(norm>1e-8,torch.tanh(norm)/norm.clamp_min(1e-8),torch.ones_like(norm))
    return (1-1e-5)*tangent*scale


class MultiScaleStem(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1=nn.Conv2d(3,64,11,stride=4,padding=2)
        self.conv2=nn.Conv2d(64,192,5,padding=2)
        self.conv3=nn.Conv2d(192,384,3,padding=1)
        self.conv4=nn.Conv2d(384,256,3,padding=1)
        self.conv5=nn.Conv2d(256,256,3,padding=1)

    def forward(self,x):
        x=F.max_pool2d(F.relu(self.conv1(x)),3,2)
        c2=F.relu(self.conv2(x))
        c3=F.relu(self.conv3(F.max_pool2d(c2,3,2)))
        c5=F.relu(self.conv5(F.relu(self.conv4(c3))))
        return c2,c3,c5


class FoldedTriQuad(nn.Module):
    """Declared local proposal: three learned symmetric four-fiber energies.

    Windows (0123),(2345),(4567). Not TriangleTQF or an authenticated metric.
    Coefficients are proposed, not attributed to an unavailable source formula.
    """
    def __init__(self):
        super().__init__()
        self.coefficients=nn.Parameter(torch.eye(4).repeat(3,1,1)/4)
        self.register_buffer('windows',torch.tensor([[0,1,2,3],[2,3,4,5],[4,5,6,7]]))

    def forward(self,x):
        b,c,h,w=x.shape
        if c%8:raise ValueError('eight fibers per original channel required')
        fibers=x.reshape(b,c//8,8,h,w)
        local=fibers[:,:,self.windows,:,:]  # B,C,3,4,H,W
        matrices=(self.coefficients+self.coefficients.transpose(-1,-2))/2
        return torch.einsum('bctihw,tij,bctjhw->bcthw',local,matrices,local).flatten(1,2)


def neighbors64():
    """Periodic V=(Z/4Z)^3: self + six face neighbors, x fastest."""
    rows=[]
    for z in range(4):
        for y in range(4):
            for x in range(4):
                coords=[(x,y,z),((x+1)%4,y,z),((x-1)%4,y,z),(x,(y+1)%4,z),(x,(y-1)%4,z),(x,y,(z+1)%4),(x,y,(z-1)%4)]
                rows.append([a+4*b+16*c for a,b,c in coords])
    return torch.tensor(rows)


class LocalRouter(nn.Module):
    def __init__(self,dimension=64,mode='lorentz',w_min=.25,w_max=.9):
        super().__init__()
        if mode not in ('lorentz','euclidean') or not 0<w_min<w_max<1:
            raise ValueError('unsupported router or scalar bounds')
        self.mode,self.w_min,self.w_max=mode,w_min,w_max
        self.state=nn.Linear(dimension,4)
        self.value=nn.Linear(dimension,dimension)
        self.register_buffer('neighbors',neighbors64())

    def spinors(self,x):
        raw=self.state(x)
        w=self.w_min+(self.w_max-self.w_min)*raw[...,:1].sigmoid()
        norm=raw[...,1:].norm(dim=-1,keepdim=True)
        fallback=torch.zeros_like(raw[...,1:]);fallback[...,0]=1
        direction=torch.where(norm>1e-8,raw[...,1:]/norm.clamp_min(1e-8),fallback)
        return torch.cat((w,(1-w.square()).sqrt()*direction),-1)

    def forward(self,tokens):
        if tokens.ndim!=3 or tokens.shape[1]!=64:raise ValueError('B,64,D tokens required')
        q=self.spinors(tokens)
        if self.mode=='lorentz':
            state=lorentz_lift_from_spinor(q)
            costs=hyperbolic_quadrance(state.unsqueeze(2),state[:,self.neighbors,:])
        else:
            # Capacity-matched counterfactual: same bounded spinors and value map.
            costs=(q.unsqueeze(2)-q[:,self.neighbors,:]).square().sum(-1)
        beta=(1-q[...,0])/q[...,0]
        weights=sparsemax(-beta.unsqueeze(-1)*costs)
        output=tokens+(weights.unsqueeze(-1)*self.value(tokens)[:,self.neighbors,:]).sum(2)
        diagnostics={'support_mean':(weights>0).sum(-1).float().mean().detach(),
                     'self_mass':weights[...,0].mean().detach(),
                     'self_only_fraction':(weights[...,0]>=1-1e-6).float().mean().detach()}
        return output,q,weights,diagnostics


class AlexNetHGEOT(nn.Module):
    def __init__(self,classes=10,dimension=64,semantic_dimension=64,channels=16,routing='lorentz'):
        super().__init__()
        if any(type(v) is not int or v<1 for v in (classes,dimension,semantic_dimension,channels)):
            raise ValueError('positive integer dimensions required')
        self.stem=MultiScaleStem()
        self.projections=nn.ModuleList(nn.Conv2d(c,channels,1) for c in (192,384,256))
        self.align=nn.Conv2d(3*channels,channels,1)
        self.quad=FoldedTriQuad()
        self.mix=nn.Conv2d(11*channels,dimension,1)
        self.to_voxels=nn.Linear(32,64)
        self.router=LocalRouter(dimension,routing)
        self.classifier=nn.Linear(dimension,classes)
        self.semantic=nn.Linear(dimension,semantic_dimension)

    def forward(self,images):
        if images.ndim!=4 or images.shape[1:]!=(3,224,224) or not images.is_floating_point() or not torch.isfinite(images).all():
            raise ValueError('finite floating B,3,224,224 input required')
        maps=self.stem(images)
        aligned=[F.interpolate(project(m),size=(16,16),mode='bilinear',align_corners=False) for project,m in zip(self.projections,maps)]
        selected=self.align(torch.cat(aligned,1))
        folded=fold_three(selected)
        features=self.mix(torch.cat((folded,self.quad(folded)),1))
        tokens=self.to_voxels(features.flatten(2)).transpose(1,2)
        routed,q,weights,diagnostics=self.router(tokens)
        pooled=routed.mean(1)
        tangent=self.semantic(pooled)
        semantic=semantic_exp0(tangent)
        return {'logits':self.classifier(pooled),'semantic':semantic,'spinors':q,
                'tokens':routed,'weights':weights,'diagnostics':diagnostics,
                'tap_shapes':[tuple(m.shape) for m in maps],
                'selected_shape':tuple(selected.shape),'folded_shape':tuple(folded.shape)}
