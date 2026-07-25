import csv
import numpy as np

Cur =40        #Mapの電流レンジ Cur=260ならば、-260～260で20A刻み
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

#current_1_list = np.linspace(-1*Cur, 0, (div-1)//2+1)  # 27点 → 20A刻み
current_1_list = np.linspace(-20, -20, 1)  # 27点 → 20A刻み
current_2_list = np.linspace(-1*Cur, Cur, div)  # 27点 → 20A刻み

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