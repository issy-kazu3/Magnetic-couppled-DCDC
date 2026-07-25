import numpy as np
import pandas as pd
import sys
from magnetic_model import CAL_L_comb
from magnetic_model import MagValues





def solver_ripple(Map,conds):
    Ix=[0.0]*5
    Ia=[0.0]*5
    Ib=[0.0]*5

    # Map : 27×27×8 の3次元配列
    # conds : 計算条件(辞書)

    #条件読み込み
    V1=conds["V1"]
    V2=conds["V2"]
    I_total=conds["I_total"]
    frq=conds["sw_frq"]         # Hzに変換すみ
    max_I = 260

    Idifa = 0 #初期ﾘｾｯﾄ
    Idifb = 0 #初期ﾘｾｯﾄ
    Iave_cala = 0
    Iave_calb = 0
    Istarta = I_total / 2
    Istartb = I_total / 2

    Tall=1.0/frq

    Toff = Tall * V1 / V2
    VL=V2-V1
    Ton = Tall - Toff
    duty = (Tall - Toff) / Tall
    dt=Tall/2000  #2000分割
    steps=int(Tall/dt)  #1周期のステップ数

    #結果格納
    t_list=[0.0]*steps
    Ia_list=[0.0]*steps
    Ib_list=[0.0]*steps
    I_total_list=[0.0]*steps
    Fluxr_list=[0.0]*steps
    Fluxl_list=[0.0]*steps
    Fluxu_list=[0.0]*steps
    Leakr_list=[0.0]*steps
    Leakl_list=[0.0]*steps




    print("steps=",steps)

    cyc=0

    if duty < 0.5:
        mode=0
    elif duty == 0.5:
        mode=1
    else:
        mode=2
    
    if mode==0:
        while True:
            cyc = cyc + 1
            x = Istarta - Idifa
            y = Istartb - Idifb
            Iave_cala = 0
            Iave_calb = 0
            Istarta = x
            Istartb = y
            Brmax = -2
            Brmin = 2
            Blmax = -2
            Blmin = 2
            Bumax = -2
            Bumin = 2
            Leaklmax = -2
            Leakrmax = -2

            #----on off------
            Ea = V1
            Eb = -1 * VL
            for j in range(steps):
                t = j * dt + Ton / 2
                if t > Ton: break 
                if (np.abs(x) > max_I) or (np.abs(y) > max_I) : #　電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
    
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------
            step = j
            Ix[0] = x + y #総電流であることに注意
            Ia[0] = x
            Ib[0] = y
            #------------off off 半周期まで------------
            Ea = -1 * VL
            Eb = -1 * VL
            for j in range(step, steps):
                t = j * dt + Ton / 2
                if t > Tall / 2:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I) : #　電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------

            step = j
            Ix[1] = x + y #総電流であることに注意
            Ia[1] = x
            Ib[1] = y

            #------------off on------------
            Ea = -1 * VL
            Eb = V1
            for j in range(step, steps):
                t = j * dt + Ton / 2
                if t > Tall / 2 + Ton:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I) : #　電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr
                #---------------------------------- 
                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------

            step = j
            Ix[2] = x + y #総電流であることに注意
            Ia[2] = x
            Ib[2] = y
            #----------------------------------

            #------------off off------------
            Ea = -1 * VL
            Eb = -1 * VL
            for j in range(step, steps):
                t = j * dt + Ton / 2
                if t > Tall:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I) : #　電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr
                #----------------------------------
                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------

            step = j
            Ix[3] = x + y #総電流であることに注意
            Ia[3] = x
            Ib[3] = y
            #----------------------------------
            #------------on off------------
            Ea = V1
            Eb = -1 * VL
            for j in range(step, steps):
                t = j * dt + Ton / 2
                if t > Tall + Ton / 2:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I) : #　電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------

            Iave_cala = Iave_cala / steps
            Iave_calb = Iave_calb / steps
            Idifa = Iave_cala - I_total / 2
            Idifb = Iave_calb - I_total / 2
            if np.abs(Idifa) < 2 and np.abs(Idifb) < 2:
                break
        #--------------------ここまでループ-------------------------

    #-----------------------------------------------------------------------------------------------------------
    # MODE=1
    #-----------------------------------------------------------------------------------------------------------
    if mode == 1:
        while True:
            #--------------------------------------ここからループ-------------
            cyc = cyc + 1
            x = Istarta - Idifa
            y = Istartb - Idifb
            Istarta = x
            Istartb = y
            dt = Tall / steps
            Brmax = -2
            Brmin = 2
            Blmax = -2
            Blmin = 2
            Bumax = -2 
            Bumin = 2
            Leaklmax = -2
            Leakrmax = -2
            #-------ﾓｰﾄﾞ1 onとoff ちょうど半周期まで----------------
            Ea = V1
            Eb = -1 * VL
            for j in range(steps):
                t = j * dt + Ton / 2
                if t > Ton:
                    break               
                if (np.abs(x) > max_I) or (np.abs(y) > max_I):  # 電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr    

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------
    
            step = j
            Ix[0] = x + y #総電流であることに注意
            Ia[0] = x
            Ib[0] = y

            #------------off on 全周期まで------------
            Ea = -1 * VL
            Eb = V1
            for j in range(step, steps):
                t = j * dt + Ton / 2
                if t > Tall:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I):  # 電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------
    
            step = j
            Ix[1] = x + y #総電流であることに注意
            Ia[1] = x
            Ib[1] = y

            Ix[2] = x + y #総電流であることに注意
            Ia[2] = x
            Ib[2] = y

            Ix[3] = x + y #総電流であることに注意
            Ia[3] = x
            Ib[3] = y

            #------------on off on区間の半分まで------------
            Ea = V1
            Eb = -1 * VL
            for j in range(step, steps):
                t = j * dt + Ton / 2
                if t > Tall + Ton / 2:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I):  # 電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.FluxlLa * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------

            Iave_cala = Iave_cala / steps
            Iave_calb = Iave_calb / steps
            Idifa = Iave_cala - I_total / 2
            Idifb = Iave_calb - I_total / 2
            if np.abs(Idifa) < 2 and np.abs(Idifb) < 2:
                break
        #--------------------ここまでループ-------------------------

    #-----------------------------------------------------------------------------------------------------------
    # MODE=2
    #-----------------------------------------------------------------------------------------------------------
    if mode == 2:
        print("mode=2")
        while True:
            #--------------------------------------ここからループ-------------
            cyc = cyc + 1
            x = Istarta - Idifa
            y = Istartb - Idifb
            Istarta = x
            Istartb = y
            dt = Tall / steps
            Brmax = -2
            Brmin = 2
            Blmax = -2
            Blmin = 2
            Bumax = -2
            Bumin = 2
            Leaklmax = -2
            Leakrmax = -2
            #-------ﾓｰﾄﾞ1 onとon ----------------
            Ea = V1
            Eb = V1
            for j in range(0, steps):
                t = j * dt + (Ton - Tall / 2) / 2
                if t > (Ton - 1 / 2 * Tall):
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I):  # 電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------

    
            step = j
            Ix[0] = x + y #総電流であることに注意
            Ia[0] = x
            Ib[0] = y
            #------------on off 半周期まで------------
            Ea = V1
            Eb = -1 * VL
            for j in range(step, steps):
                t = j * dt + (Ton - Tall / 2) / 2
                if t > Tall / 2:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I):  # 電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y

                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------
            step = j
            Ix[1] = x + y #総電流であることに注意
            Ia[1] = x
            Ib[1] = y
            #------------on on------------
            Ea = V1
            Eb = V1
            for j in range(step, steps):
                t = j * dt + (Ton - Tall / 2) / 2
                if t > Ton:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I):  # 電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:   
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------
            step = j
            Ix[2] = x + y #総電流であることに注意
            Ia[2] = x
            Ib[2] = y
            #------------off on 全周期まで------------
            Ea = -1 * VL
            Eb = V1
            for j in range(step, steps):
                t = j * dt + (Ton - Tall / 2) / 2
                if t > Tall:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I):  # 電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------
            step = j
            Ix[3] = x + y #総電流であることに注意
            Ia[3] = x
            Ib[3] = y

            #------------on on 最後の半端------------
            Ea = V1
            Eb = V1
            for j in range(step, steps):
                t = j * dt + (Ton - Tall / 2) / 2
                if t > Tall + (Ton - Tall / 2) / 2:
                    break
                if (np.abs(x) > max_I) or (np.abs(y) > max_I):  # 電流が上限超える場合は終了
                    print(f"OVER CURRENT LIMIT")
                    sys.exit()
                mag=MagValues(CAL_L_comb(x, y,Map))
                x = x + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.Lb * Ea - mag.Mab * Eb)
                y = y + dt * 1 / (mag.La * mag.Lb - mag.Mab * mag.Mba) * (mag.La * Eb - mag.Mba * Ea)
                Iave_cala = Iave_cala + x
                Iave_calb = Iave_calb + y
                #----------------------------------
                if mag.Fluxr > Brmax:
                    Brmax = mag.Fluxr
                if mag.Fluxr < Brmin:
                    Brmin = mag.Fluxr
                if mag.Fluxl > Blmax:
                    Blmax = mag.Fluxl
                if mag.Fluxl < Blmin:
                    Blmin = mag.Fluxl
                if mag.Fluxu > Bumax:
                    Bumax = mag.Fluxu
                if mag.Fluxu < Bumin:
                    Bumin = mag.Fluxu
                if np.abs(mag.Leakl) > Leaklmax:
                    Leaklmax = mag.Leakl
                if np.abs(mag.Leakr) > Leakrmax:
                    Leakrmax = mag.Leakr

                t_list[j]=dt*j
                Ia_list[j]=x
                Ib_list[j]=y
                I_total_list[j]=x+y
                Fluxr_list[j]=mag.Fluxr
                Fluxl_list[j]=mag.Fluxl
                Fluxu_list[j]=mag.Fluxu
                Leakr_list[j]=mag.Leakr
                Leakl_list[j]=mag.Leakl
                #----------------------------------
            step = j
            print("step=",step)
#            Ix[4] = x + y #総電流であることに注意
#            Ia[4] = x
#            Ib[4] = y

            Iave_cala = Iave_cala / steps
            Iave_calb = Iave_calb / steps
            Idifa = Iave_cala - I_total / 2
            Idifb = Iave_calb - I_total / 2
            if np.abs(Idifa) < 2 and np.abs(Idifb) < 2:
                break
        #--------------------ここまでループ-------------------------

    #-------------------------------------------------------------------------------------------------------
    #   MODEわけここまで
    #-----------------------------------------------------------------------

    Imax = Ix[0]
    Imin = Ix[0]
    for j in range(1, 3):
        if Ix[j] > Imax:
            Imax = Ix[j]
        if Ix[j] < Imin:
            Imin = Ix[j]
    Ia_max = Ia[0]
    Ia_min = Ia[0]
    for j in range(1, 4):
        if Ia[j] > Ia_max:
            Ia_max = Ia[j]
        if Ia[j] < Ia_min:
            Ia_min = Ia[j]
    Irip=Imax - Imin
    Ia_rip=Ia_max - Ia_min

    dBr = np.abs(Brmax - Brmin) / 2
    dBl = np.abs(Blmax - Blmin) / 2
    dBu = np.abs(Bumax - Bumin) / 2

    #-----------------------------------------
    # ① 時系列データを DataFrame にまとめる
    #-----------------------------------------
    result_df = pd.DataFrame({
        "t": t_list,
        "Ia": Ia_list,
        "Ib": Ib_list,
        "I_total": I_total_list,
        "Fluxr": Fluxr_list,
        "Fluxl": Fluxl_list,
        "Fluxu": Fluxu_list,
        "Leakr": Leakr_list,
        "Leakl": Leakl_list,
    })

    #-----------------------------------------
    # ② 代表値（summary）を辞書で返す
    #-----------------------------------------
    summary = {
        "I_total_max": Imax,
        "I_total_min": Imin,
        "Irip": Irip,

        "Ia_max": Ia_max,
        "Ia_min": Ia_min,
        "Ia_amp": Ia_rip,

        "Brmax": Brmax,
        "Brmin": Brmin,
        "dBr": dBr,

        "Blmax": Blmax,
        "Blmin": Blmin,
        "dBl": dBl,

        "Bumax": Bumax,
        "Bumin": Bumin,
        "dBu": dBu,

        "Leakr_max": Leakrmax,
        "Leakl_max": Leaklmax,
    }

    return result_df, summary
