import pandas as pd
import matplotlib.pyplot as plt

csv_path =r"D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\github\testcase_waveform.csv"

def plt_waveform():
    df=pd.read_csv(csv_path)
    plt.plot(df["t"],df["Ia"],label="Ripple Coil A")
    plt.plot(df["t"],df["Ib"],label="Ripple Coil B")
    plt.plot(df["t"],df["I_total"],label="Ripple total")
    plt.xlabel("Time [s]")
    plt.ylabel("[A]")
    plt.title("Magnetic Coupled Cnverter Ripple Waveform")
    plt.ylim(0,250)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
