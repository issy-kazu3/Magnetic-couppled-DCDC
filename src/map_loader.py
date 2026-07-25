import pandas as pd
import numpy as np

csv_path=r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\github\result_map.csv"

def load_map(csv_path):
    df=pd.read_csv(csv_path)
    # df は 27×27×8 の行列が縦に並んだ形になっているはず
    # これを 3次元配列に変換する   
    Map=np.zeros((27,27,8))

    for idx,row in df.iterrows():   #idxはcsvの行番号、rowはその行のデータ これpandasの機能のようだ
        j=int((row['I1']+260)/20)
        k=int((row['I2']+260)/20)
        Map[j,k,:]=row[['La','Lb','Mab','FLUX_in_RCORE','FLUX_in_LCORE','FLUX_in_UCORE','Leak_R','Leak_L']].values
    return Map

