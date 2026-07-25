# Python 実装概要
本ページでは、磁気結合 DC/DC コンバータ解析における
Python 実装の構成と役割分担をまとめます。

- Maxwell からのインダクタンスマップ読み込み

- マップ補間関数の構築

- リプル電流・磁束・電圧の逐次計算

- 損失計算（銅損・鉄損）

- 図のプロット

 ## 1. ファイル構成
典型的な構成例：

core/ripple_solver.py  
リプル計算のメインロジック

core/inductance_map.py  
L1, L2, M のマップ読み込み・補間

maxwell/run_maxwell_doe.py  
Maxwell DOE 実行（必要なら）

tools/plot_waveforms.py  
波形プロット用ユーティリティ

# 2. インダクタンスマップの読み込み
Maxwell から出力された CSV を読み込みます。

python
```python
import numpy as np
from scipy.interpolate import RegularGridInterpolator

def load_inductance_map(path):
    data = np.loadtxt(path, delimiter=',', skiprows=1)
    I1 = np.unique(data[:, 0])
    I2 = np.unique(data[:, 1])

    L1 = data[:, 2].reshape(len(I1), len(I2))
    L2 = data[:, 3].reshape(len(I1), len(I2))
    M  = data[:, 4].reshape(len(I1), len(I2))

    L1_map = RegularGridInterpolator((I1, I2), L1)
    L2_map = RegularGridInterpolator((I1, I2), L2)
    M_map  = RegularGridInterpolator((I1, I2), M)

    return L1_map, L2_map, M_map
```
# 3. マップを使った磁束・電圧計算
python
```python
def compute_flux(L1_map, L2_map, M_map, I1, I2):
    L1 = L1_map([I1, I2])
    L2 = L2_map([I1, I2])
    M  = M_map([I1, I2])

    Phi1 = L1 * I1 + M * I2
    Phi2 = L2 * I2 + M * I1
    return Phi1, Phi2
```
電圧は差分で計算します。

python
```python
ef compute_voltage(Phi, Phi_prev, dt):
    return -(Phi - Phi_prev) / dt
```
# 4. 時間ステップループ（リプル計算の骨格）
python
```python
def simulate_ripple(params, L1_map, L2_map, M_map):
    dt = params['dt']
    N  = params['steps']

    I1 = params['I1_init']
    I2 = params['I2_init']

    Phi1_prev = 0.0
    Phi2_prev = 0.0

    I1_list, I2_list = [], []

    for k in range(N):
        # スイッチング状態から VL1, VL2 を決定
        VL1, VL2 = decide_reactor_voltage(k, params)

        # 磁束
        Phi1, Phi2 = compute_flux(L1_map, L2_map, M_map, I1, I2)

        # 電圧
        V1 = compute_voltage(Phi1, Phi1_prev, dt)
        V2 = compute_voltage(Phi2, Phi2_prev, dt)

        # 有効インダクタンス（近似）
        L1_eff = L1_map([I1, I2])
        L2_eff = L2_map([I1, I2])

        # 電流更新
        I1 += (VL1 / L1_eff) * dt
        I2 += (VL2 / L2_eff) * dt

        Phi1_prev, Phi2_prev = Phi1, Phi2

        I1_list.append(I1)
        I2_list.append(I2)

    return np.array(I1_list), np.array(I2_list)
```
# 5. 損失計算
python
```python
def compute_copper_loss(I, R):
    return np.mean(I**2) * R

def compute_iron_loss(Phi, dt, k, alpha, beta):
    # 簡易 Steinmetz 近似などをここに実装
    pass
```
# 6. 波形プロット
python
```python
import matplotlib.pyplot as plt

def plot_ripple(t, I1, I2):
    plt.figure()
    plt.plot(t, I1, label='Coil A')
    plt.plot(t, I2, label='Coil B')
    plt.plot(t, I1 + I2, label='Total Ripple')
    plt.xlabel('Time [s]')
    plt.ylabel('Current [A]')
    plt.legend()
    plt.grid(True)
    plt.show()
```
# 7. まとめ
- Maxwell のインダクタンスマップを Python で読み込み・補間

- 各時刻の (I1, I2) に応じて L1, L2, M を参照

- 磁束 → 電圧 → 電流更新のループでリプル波形を生成

- 損失計算・プロットまで一貫して実装可能
