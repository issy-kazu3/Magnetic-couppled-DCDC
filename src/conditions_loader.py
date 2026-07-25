import pandas as pd

csv_path=r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\github\conditions.csv"

def load_conditions(csv_path):
    df=pd.read_csv(csv_path)
    # 見出しが正しければそのまま使う
    cols=df.columns.tolist()

    def get_value(name,index):
        if name in cols:
            return df.iloc[0][name]     #pandasのilocの最初の行は見出し。次の行が[0]になっている[name]はみだしがnameの列の値を取得する
        else:
            return df.iloc[0][index]
    conds={
        "V1" : get_value("V1",0),
        "V2" : get_value("V2",1),
        "I_total" : get_value("I_total",2),
        "sw_frq" : get_value("sw_frq",3)*1000,  #kHz→Hz
    }

    return conds
