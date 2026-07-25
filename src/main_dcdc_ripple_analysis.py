#20260720 This code is main module of magnetic coupling DCDC converter ripple current analysis
# This code uses following codes as sub-modules of this main module.
# conditions_loader.py,map_loader.py,magnetic_model.py,ripple_solver.py
# you need to prepare conditons.csv,result_map.csv in advance.
# result_map.csv will be outputted with VCU_inductance_analysis.py and github_REACTOR_TRY_25model_analysis.VBS by using Ansys Maxwell.

from conditions_loader import load_conditions
from map_loader import load_map
from ripple_solver import solver_ripple
from ripple_figure import plt_waveform
import pandas as pd
import os

csv_path =r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\github"

def run_case(map_file,cond_file,prefix="case1"):
    #条件読み込み
    conds=load_conditions(cond_file)

    #マップの読み込み
    Map=load_map(map_file)

    #リプル計算
    df,summary=solver_ripple(Map,conds)

    #時系列データをCSV出力
    file_path=os.path.join(csv_path,f"{prefix}_waveform.csv")
    df.to_csv(file_path,index=False)                 #index=Falseは、出力するCSVに行番号を付与しないことを指示している

    file_path=os.path.join(csv_path,f"{prefix}_summary.csv")
    pd.DataFrame([summary]).to_csv(file_path,index=False) # f"はformatted string　r"はraw stringを意味する

    plt_waveform()

    return df,summary

def main():
    # 単発計算
    run_case(
        map_file=os.path.join(csv_path,"result_map.csv"),
        cond_file=os.path.join(csv_path,"conditions.csv"),
        prefix=os.path.join(csv_path,"testcase")
    )

    #DOEの例（複数条件ファイルを回す)
    #cond_files=["cond1.csv","cond2.csv","cond3.csv"]
    #for i,cond_file in enumerate(cond_files):
    #   run_case("map.csv",cond_file,prefix=f"case_[i]")

if __name__=="__main__":
    main()
