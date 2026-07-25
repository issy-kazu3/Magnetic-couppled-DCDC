import numpy as np

class MagValues:
    def __init__(self, mag):
        self.La = mag["La"]
        self.Lb = mag["Lb"]
        self.Mab = mag["Mab"]
        self.Mba = mag["Mba"]
        self.Fluxr = mag["Fluxr"]
        self.Fluxl = mag["Fluxl"]
        self.Fluxu = mag["Fluxu"]
        self.Leakr = mag["Leakr"]
        self.Leakl = mag["Leakl"]


def index_from_current(cur):
    return int((cur+260)//20)   #//は整数除算 小数点以下は切り捨て

def CAL_L_comb(cur1,cur2,Map):
    na=index_from_current(cur1)
    nb=index_from_current(cur2)

    da=(cur1+260)-20*na
    db=(cur2+260)-20*nb

    La=bilinear(Map,na,nb,da,db,0)
    Lb=bilinear(Map,na,nb,da,db,1)
    Mab=bilinear(Map,na,nb,da,db,2)
    Fluxr=bilinear(Map,na,nb,da,db,3)
    Fluxl=bilinear(Map,na,nb,da,db,4)
    Fluxu=bilinear(Map,na,nb,da,db,5)
    Leakr=bilinear(Map,na,nb,da,db,6)
    Leakl=bilinear(Map,na,nb,da,db,7)
    Mba=Mab


    return {
        "La": La,
        "Lb": Lb,
        "Mab": Mab,
        "Mba": Mba,
        "Fluxr": Fluxr,
        "Fluxl": Fluxl,
        "Fluxu": Fluxu,
        "Leakr": Leakr,
        "Leakl": Leakl
    }


def bilinear(Map,na,nb,da,db,p):
    # pは0~7の整数で、Mapの3次元目のインデックスに対応する
    # na,nbは0~26の整数で、Mapの1,2次元目のインデックスに対応する
    # da,dbは0~19の整数で、補間するための重みを計算するために使う

    # 4点の値を取得
    Q11 = Map[na, nb, p]
    Q12 = Map[na, nb+1, p]
    Q21 = Map[na+1, nb, p]
    Q22 = Map[na+1, nb+1, p]

    tx=da/20
    ty=db/20    

    # 補間計算
    return (1-tx)*(1-ty)*Q11 + (1-tx)*ty*Q12 + tx*(1-ty)*Q21 + tx*ty*Q22


