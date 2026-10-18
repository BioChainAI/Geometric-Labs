"""Right-stepping S5 addresses in ORDINARY integer coordinates; Theorem 7.2."""
from typing import Tuple
S5_GENS = {"+i":(1,2,0,0), "-i":(1,-2,0,0), "+j":(1,0,2,0), "-j":(1,0,-2,0), "+k":(1,0,0,2), "-k":(1,0,0,-2)}
OPPOSITE = {g: ('-' if g[0]=='+' else '+')+g[1] for g in S5_GENS}
def step_s5_shift_add(q: Tuple[int, int, int, int], label: str) -> Tuple[int, int, int, int]:
        """Multiplier-free right step q * (1 +/- 2u) = q + 2*(q*u) using only 1-bit shifts and additions."""
        w, x, y, z = q
        if label == "+i":
            return (w - (x << 1), x + (w << 1), y + (z << 1), z - (y << 1))
        if label == "-i":
            return (w + (x << 1), x - (w << 1), y - (z << 1), z + (y << 1))
        if label == "+j":
            return (w - (y << 1), x - (z << 1), y + (w << 1), z + (x << 1))
        if label == "-j":
            return (w + (y << 1), x + (z << 1), y - (w << 1), z - (x << 1))
        if label == "+k":
            return (w - (z << 1), x + (y << 1), y - (x << 1), z + (w << 1))
        if label == "-k":
            return (w + (z << 1), x - (y << 1), y + (x << 1), z - (w << 1))
        raise ValueError(label)

def recover_s5_word(q: tuple[int,int,int,int], depth: int) -> list[str]:
    if type(depth) is not int or depth < 0 or len(q)!=4 or any(type(c) is not int for c in q):
        raise ValueError("invalid address or depth")
    if sum(c*c for c in q)!=5**depth:
        raise ValueError("address norm does not match depth")
    current=q
    recovered=[]
    for remaining in range(depth,0,-1):
        candidates=[]
        for label in S5_GENS:
            prod=step_s5_shift_add(current,OPPOSITE[label])
            if all(c%5==0 for c in prod):
                cand=tuple(c//5 for c in prod)
                if remaining==1 and cand!=(1,0,0,0):
                    continue
                if remaining>1 and all(c%5==0 for c in cand):
                    continue
                candidates.append((label,cand))
        if len(candidates)!=1:
            raise ValueError("address is not a unique reduced S5 word")
        label,current=candidates[0]
        recovered.append(label)
    if current!=(1,0,0,0):
        raise ValueError("invalid root")
    return recovered[::-1]

def abelian_shadow(word: list[str]) -> tuple[int,int,int]:
    coords=[0,0,0]
    for g in word:
        if g not in S5_GENS:
            raise ValueError(g)
        coords['ijk'.index(g[1])] += 1 if g[0]=='+' else -1
    return tuple(coords)
