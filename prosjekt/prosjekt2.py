
import prosjekt
from matplotlib import pyplot as plt
from typing import Iterator,Generator
from collections.abc import Iterable
import itertools as it

def tof(val: str) -> float|None:
    if val == "-": return None
    return float(val)

class Maaling:
    def __init__(self,line:str):
        self.navn,self.stasjonsid,dato,sno,nedbor,temp,sky,vind = line.replace(",",".").split(";")
        self.dato = f"{dato[6:]}-{dato[3:5]}-{dato[0:2]}" # ISO-8601 maker (kan sammenligne med bare string comparisons)
        self.sno = tof(sno)
        self.nedbor = tof(nedbor)
        self.temp = tof(temp)
        self.sky = tof(sky)
        self.vind = tof(vind)

def hvor_mange(data:Iterable[Maaling],verdi:str) -> int:   
    return sum(1 for x in data if x.__dict__[verdi] is not None)


def hvert_aar(data:list[Maaling]) -> Generator[Generator[Maaling,None,int],None,None]:
    start_aar = int(min(x.dato for x in data)[:4])
    slutt_aar = int(max(x.dato for x in data)[:4])
    idx = 0
    for i in range(start_aar,slutt_aar+1):
        while data[idx].dato < str(i): idx += 1
        def inner():
            where = idx
            while True:
                if int(data[where].dato[:4]) != i: return i
                where += 1
                yield data[where-1]
        yield inner
    
def fra_til(data: list[Maaling],start:str,slutt:str) -> Generator[Maaling,None,None]:
    for i in data:
        if start <= i.dato < slutt: yield i


def countif_per_aar(data:Iterable[Maaling],func,has:str|None=None,count=0,reduce=sum) \
        -> list[tuple[int,any]]:
    return [(int(next(aar()).dato[:4]),reduce(func(x) for x in aar())) for aar in hvert_aar(data)  \
            if has is None or hvor_mange(aar(),has)>=count]    

# a
def les_inn(filnavn: str) -> list[Maaling]:
    data = []
    with open(filnavn,"r") as f:
        for l in f.readlines()[1:-1]:
            if ";" in l:
                data.append(Maaling(l[:-1]))
    return data

# b
def skifore(data: list[Maaling],aar: int) -> int:
    start = f"{aar}-10-01"
    end = f"{aar+1}-06-01"
    return sum(1 for x in fra_til(data,start,end) if x.sno and x.sno >= 20)
    # gidder ikke bruke løsningen fra tidligere, blir mye unpacking og repacking av data

# c
def trend_skifore(data: list[Maaling],start_aar: int, slutt_aar: int) -> list[int]:
    val = [skifore(data,i) for i in range(start_aar,slutt_aar)]
#    plt.plot(skifore,range(start_aar,slutt_aar))
#    plt.show()
    return val

# d
def plot_sno(data: list[Maaling]) -> None:
    start_aar = int(min(x.dato for x in data)[:4])
    slutt_aar = int(max(x.dato for x in data)[:4])
    data2 = zip(trend_skifore(data,start_aar,slutt_aar),range(start_aar,slutt_aar))
    data2 = tuple(filter(lambda x: hvor_mange(fra_til(data,f"{x[1]}-10-01",f"{x[1]+1}-06-01"),"sno")>=200,data2))
    plt.plot(tuple(y for x,y in data2),tuple(x for x,y in data2),"ro")
    plt.plot((data2[0][-1],data2[-1][-1]),(data2[0][0],data2[-1][0]))
    plt.show()
    
#plot_sno(data)

# e
def vekst(data: list[Maaling]):
    vekst = countif_per_aar(data,lambda x: max(x.temp-5,0) if x.temp else 0,"temp",300)
    vekst = [(round(i,8),j) for i,j in vekst] # fordi floats
    return vekst

# f
def torke(data: list[Maaling]):
    torke = [prosjekt.f(x.nedbor for x in aar()) \
             if hvor_mange(aar(),"nedbor")>=300 else None for aar in hvert_aar(data)]
    plt.plot(list(set(int(x.dato[:4]) for x in data)),torke)
    plt.show()

# g
def penvar(data: list[Maaling]):
    return countif_per_aar(data,lambda x: x.sky and x.sky <= 3,"sky",300)

# h
def vind(data: list[Maaling]) -> None: 
    gjvind = [(x[0],x[1]/y[1])for x,y in zip(
        countif_per_aar(data,lambda x: x.vind if x.vind is not None else 0,"vind",300),
        countif_per_aar(data,lambda x: x.vind is not None,"vind",300)
    )]
    maksvind = countif_per_aar(data,lambda x: x.vind if x.vind else 0,"vind",300,max)
    print(gjvind)
    plt.plot([x for x,y in gjvind],[y for x,y in gjvind])
    plt.plot([x for x,y in maksvind],[y for x,y in maksvind])
    plt.show()


# i
def trend_temp(data: list[Maaling]):    
    out = {}
    md = ""
    v = 0
    n = 0
    for x in data:
        if x.dato[:7] != md:
            if n > 0:
                out[md] = v / n
            md = x.dato[:7]
            v = 0
            n = 0
        if x.temp is not None:
            v += x.temp
            n += 1
    if n > 0:
        out[md] = v / n
    nm = [k for k,v in out.items()]
    v = [v for k,v in out.items()]
    diff = prosjekt.e(v)
    plt.plot(nm,v)
    plt.figure(2)
    plt.plot(nm[:-1],diff)
    plt.show()

def main():
    data = les_inn("snoedybder_vaer_en_stasjon_dogn.csv")
    plot_sno(data)
    torke(data)
    vind(data)
    trend_temp(data)


if __name__=="__main__":
    main()
            
