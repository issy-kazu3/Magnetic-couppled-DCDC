# 20260716 optimusのpython化

import subprocess
import re
import csv
import numpy as np

Cur =260        #Mapの電流レンジ Cur=260ならば、-260～260で20A刻み
div=(Cur//20)*2+1

vbs_path =r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\github\github_REACTOR_TRY_25model_analysis.VBS"
csv_path =r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\github\result_map.csv"

MAXWELL_CMD = r'"D:\Program Files\AnsysEM_2022\v222\Win64\ansysedt.exe" -RunScriptAndExit "{}"'
RESULT_TXT = r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\MAXWELL16_SCRIPT\25MODEL_DETAILED_COIL\Project1_Maxwell3DDesign1.txt"
CORE_FLUXr_TXT = r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\MAXWELL16_SCRIPT\25MODEL_DETAILED_COIL\core_fluxr.txt"
CORE_FLUXl_TXT = r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\MAXWELL16_SCRIPT\25MODEL_DETAILED_COIL\core_fluxl.txt"
CORE_FLUXu_TXT = r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\MAXWELL16_SCRIPT\25MODEL_DETAILED_COIL\core_fluxu.txt"
LEAK_FLUXr_TXT = r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\MAXWELL16_SCRIPT\25MODEL_DETAILED_COIL\leak_flux_ptr.txt"
LEAK_FLUXl_TXT = r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\MAXWELL16_SCRIPT\25MODEL_DETAILED_COIL\leak_flux_ptl.txt"

current_1_list = np.linspace(-1*Cur, 0, (div-1)//2+1)  # 27点 → 20A刻み
current_2_list = np.linspace(-1*Cur, Cur, div)  # 27点 → 20A刻み

# 結果を保持するリスト
result_map = []

for I1 in current_1_list:
    for I2 in current_2_list:

        # --- ① VBS のパラメータ書き換え ---
        with open(vbs_path, "r", encoding="UTF-8") as f:
            text = f.read()
        text = re.sub(r'Cur1\s*=\s*[0-9.eE+-]+', f'Cur1 = {I1}', text)  #reは文字列操作 sub()は文字の置換 r'Cur1\s*=\s*[0-9.eE+-]+' \s*は0個以上の空白 [0-9.eE+-]+は浮動小数点 fはfストリング
        text = re.sub(r'Cur2\s*=\s*[0-9.eE+-]+', f'Cur2 = {I2}', text)

        with open(vbs_path, "w", encoding="UTF-8") as f:
            f.write(text)

        # --- ② Maxwell を実行 ---
        cmd = MAXWELL_CMD.format(vbs_path)
        subprocess.run(cmd)

        # --- ③ Maxwell の結果テキストを読む ---
        with open(RESULT_TXT, "r") as f:
            for line in f:                  #このfor文はテキストファイルを1行づつ読み込むということ
                line=line.strip()           #lineというもともとのテキスト行変数に、行の前後にある空白や改行文字を取り除いたものを再代入している
                #Group1行
                if line.startswith("Group1"):
                    parts=line.split()
                    if parts[1] != "Group2":
                        #parts=["Group1","21666","-4568.7"]
                        L1=float(parts[1])*10**-9
                        M12=float(parts[2])*10**-9
                # Group2行
                if line.startswith("Group2"):
                    parts=line.split()
                    # parts=["Group2","-4568.7",21679"]
                    L2=float(parts[2])*10**-9

#        with open(RESULT_TXT, "r") as f:
#            result_text = f.read()
#        numbers = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', result_text)    #r'  [-+]?\d*\.\d+←少数  |←or　　　　[-+]?\d+←整数      '
#        values = list(map(float, numbers))
#        L1=values[0]
#        L2=values[3]
#        M12=values[1]
        
 #       with open(CORE_FLUXr_TXT, "r") as f:
 #           result_text = f.read()
 #       numbers = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', result_text)    #r'  [-+]?符号?は付いていなくてもよいの意味　　\d*ゼロ桁以上の整数   \.小数点　　\d+←一桁以上の整数  |←or　   [-+]?　　\d+←一桁以上の整数      '
 #       values = list(map(float, numbers))
 #       core_fluxr=values[1]
        
        with open(CORE_FLUXr_TXT, "r") as f:
            values=[]
            for line in f:
                for word in line.split():
                    try:
                        values.append(float(word))
                    except ValueError:
                        pass
        core_fluxr=values[0]

        with open(CORE_FLUXl_TXT, "r") as f:
            values=[]
            for line in f:
                for word in line.split():
                    try:
                        values.append(float(word))
                    except ValueError:
                        pass
        core_fluxl=values[0]
        
        with open(CORE_FLUXu_TXT, "r") as f:
            values=[]
            for line in f:
                for word in line.split():
                    try:
                        values.append(float(word))
                    except ValueError:
                        pass
        core_fluxu=values[0]
        
        with open(LEAK_FLUXr_TXT, "r") as f:
            values=[]
            for line in f:
                for word in line.split():
                    try:
                        values.append(float(word))
                    except ValueError:
                        pass
        leak_flux_ptr=values[0]

        with open(LEAK_FLUXl_TXT, "r") as f:
            values=[]
            for line in f:
                for word in line.split():
                    try:
                        values.append(float(word))
                    except ValueError:
                        pass
        leak_flux_ptl=values[0]
        
        # --- ④ 結果をマップに追加 ---
        result_map.append({
            "I1": I1,
            "I2": I2,
            "La": L1,
            "Lb": L2,
            "Mab": M12,
            "FLUX_in_RCORE": core_fluxr,
            "FLUX_in_LCORE": core_fluxl,
            "FLUX_in_UCORE": core_fluxu,
            "Leak_R": leak_flux_ptr,
            "Leak_L": leak_flux_ptl,
        })

        # --- ⑤ CSV に書き出し ---
        with open(csv_path, "a", newline="") as f:  # newline=""はcsvに空行が入らないようにするための設定  aアペンドモードで開く
            writer = csv.DictWriter(f, fieldnames=["I1", "I2", "La","Lb","Mab","FLUX_in_RCORE","FLUX_in_LCORE","FLUX_in_UCORE", "Leak_R","Leak_L"])   #これらは辞書のキー名である  DictWriterは辞書のキー名を列にしてCSVの設定をやるためのもの
            if f.tell()==0: #ファイルが空か？
                writer.writeheader()    #空ならヘッダーを書く
            writer.writerow({
                "I1": I1,
                "I2": I2,
                "La": L1,
                "Lb": L2,
                "Mab": M12,
                "FLUX_in_RCORE": core_fluxr,
                "FLUX_in_LCORE": core_fluxl,
                "FLUX_in_UCORE": core_fluxu,
                "Leak_R": leak_flux_ptr,
                "Leak_L": leak_flux_ptl,

            })

#計算済みの半分の結果を辞書化
result_dict={}  # (I1,I2) ->row
with open(csv_path,"r") as f:
    reader=csv.DictReader(f)
    for row in reader:
        key=(float(row["I1"]),float(row["I2"]))
        result_dict[key]=row

#CSV追記モードで半分の対象点を追記する
with open(csv_path,"a",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=reader.fieldnames)     #readerは上の処理の変数でまだ生きている これの"fieldnames"をDictWriterで使う別の"fieldnames"に格納している
    for I1 in current_2_list:
        for I2 in current_2_list:
            key=(I1,I2)
            rev_key=(-1*I1,-1*I2)
            #すでに計算済みならスキップ
            if key in result_dict:
                continue
            #対称点が計算済みなら、それを使う
            if rev_key in result_dict:
                row=result_dict[rev_key].copy()
                row["I1"]=I1
                row["I2"]=I2
                row["Leak_R"]=-float(row["Leak_R"])
                row["Leak_L"]=-float(row["Leak_L"])
                writer.writerow(row)











# --- ⑤ CSV に書き出し ---
#with open("result_map.csv", "w", newline="") as f:
#    writer = csv.DictWriter(f, fieldnames=["I1", "I2", "La","Lb","Mab","FLUX_in_RCORE","FLUX_in_LCORE","FLUX_in_UCORE", "Leak_R","Leak_L"])   #これらは辞書のキー名である
#    writer.writeheader()
#    writer.writerows(result_map)   
