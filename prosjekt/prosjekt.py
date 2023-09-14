import math
import itertools as it
from typing import *
# from matplotlib import pyplot as plt

def d(l : list[float],v : float) -> int:
    return sum(1 for x in l if x >= v)

def e(l : list[int]) -> list[int]:
    return [y-x for x,y in zip(l[:-1],l[1:])]

def f(l : list[int]) -> int:
    zc = 0
    mc = 0
    for i in l:
        if i:
            zc = 0
        else:
            zc += 1
            mc = max(mc,zc)
    return mc

def g(x : list[float], y : list[float]) -> tuple[int,int]:
    avgx = sum(x)/len(x)
    avgy = sum(y)/len(y)
    a = sum((xi - avgx)*(yi-avgy) for xi,yi in zip(x,y)) \
       / sum((xi - avgx)**2 for xi in x)
    b = avgy - a * avgx
    return (a,b)

def h(l : list[int]) -> int:
    return sum(map(lambda x: max(x-5,0),l))


def hb(l : list[int]) -> tuple[int,int,int]:
    l = [x if x < 0 else 0 if x < 5 else x for x in l]
    minVal = 0
    minValidx = 0
    maxdiff = 0
    maxIdx = 0
    ps = 0
    for i in range(len(l)):
        ps += l[i]
        if l[i] - minVal > maxdiff:
            maxdiff = l[i] - minVal
            maxIdx = i
        if ps < minVal: 
            minVal = ps
            minValidx = i
        
    return (minValidx,maxIdx,maxdiff)

def setup():
    global temperaturer,dogn_nedbor,temperaturer_tidspunkter
    temperaturer = [-5, 2, 6, 13, 9, 22, 28, 19, 24, 12, 5, 1, -3, -8, 2, 8, 15, 18,
    21, 26, 21, 31, 15, 4, 1, -2]
    dogn_nedbor = [2, 5, 0, 0, 0, 3, 6, 4, 0, 0, 5, 0, 12, 12, 12, 12, 7, 19]
    temperaturer_tidspunkter = list(range(len(temperaturer)))

def i() -> tuple[int,int,int]:
    return tuple(d(temperaturer,i) for i in (20,25,30))

def j() -> None:
    print(*[str(i) + " " + ["synkende","uforandret","stigende"][(x>0) + (x>=0)] for i,x in enumerate(temperaturer)],sep="\n")

def k():
    x,_ = g(temperaturer_tidspunkter,temperaturer)
    print(["synkende","uforandret","stigende"][x>0 + x>=0])

def l():
    print(h(temperaturer))

def m():
    print(f(dogn_nedbor))

def main():
    setup()
    i()
    j()
    k()
    l()
    m()

main()