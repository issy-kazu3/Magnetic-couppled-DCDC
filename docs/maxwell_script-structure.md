# Maxwell VBS Script Structure
本ページでは、磁気結合リアクトルのインダクタンスマップ生成に使用する
Maxwell 3D の VBS スクリプト構造をまとめます。

Python DOE から呼び出される VBS は、
Maxwell モデルのパラメータ設定・電流掃引・計算実行・結果出力を
すべて自動化する役割を持ちます。

# 1. VBS の役割（Purpose）
VBS は Maxwell の GUI 操作をすべて自動化し、以下を実行します。

モデルパラメータの設定

電流 I₁, I₂ のセット

計算実行

L1, L2, M の抽出

漏れ磁束分布の出力

CSV 保存

Python からのバッチ呼び出しに対応

Maxwell の解析を 完全自動化する中心的なスクリプトです。

# 2. スクリプト全体構成（Overview）
VBS は以下の 6 つのブロックで構成されます。

パラメータ宣言（dim / dia / din）

モデルの基本設定（コイル・コア寸法）

電流パラメータの設定（I₁, I₂）

解析実行（Solve）

結果抽出（L1, L2, M, Flux）

CSV 出力（保存パス指定）

# 3. パラメータ宣言（Parameter Definition）
VBS の先頭では、モデル寸法・電流値・保存パスなどを宣言します。

例：

コード
dim Curl, Cur2     '右、左コイルの電流
dim Turn           'ターン数
dim Cuh, Cut       '銅線寸法
dim savepath       '保存パス
重要ポイント
Curl と Cur2 が I₁, I₂ に相当する

巻き方向の極性はここで決まる

漏れ磁束用の座標系（leakix など）もここで宣言する

# 4. モデル寸法の設定（Geometry Setup）
コイル・コアの寸法を VBS で設定します。

例：

コード
Cuc1 = 8.4   'コイル間クリアランス
Clw  = 3.05  'コア側クリアランス
Icorew = 32  'コア幅
ポイント
Maxwell モデルの寸法は VBS で完全再現可能

Python DOE から寸法パラメータを渡すことも可能

寸法変更 → 自動再計算ができる

# 5. 電流パラメータの設定（Current Setup）
電流 I₁, I₂ を設定します。

コード
Curl = 100.0
Cur2 = 50.0
極性が最重要
L1 と L2 の巻き方向が逆

下→上の電流で DC フラックスが打ち消し合う

→ Curl と Cur2 の符号が正しく設定されている必要がある

# 6. 解析実行（Solve）
Maxwell の解析を実行します。

コード
oDesign.Solve
Python DOE では、この VBS を電流条件ごとに呼び出し、
数十〜数百ケースを自動計算します。

# 7. 結果抽出（Extract Results）
自己インダクタンス L1, L2
Maxwell の結果から L1, L2 を抽出します。

相互インダクタンス M
M は磁束リンクから計算されます。

漏れ磁束分布
座標系（leakix, leakiz）を使って Bx, By, Bz を抽出します。

# 8. CSV 出力（Save Data）
結果を CSV に保存します。

コード
savedata = "D:\Userarea\...\inductance.csv"
saveflux = "D:\Userarea\...\flux.csv"
Python 側でこの CSV を読み込み、
インダクタンスマップを構築します。

# 9. スクリプトの注意点（Notes）
Curl と Cur2 の符号が正しいこと  
→ 巻き方向と DC フラックスキャンセルに一致させる

漏れ磁束座標系を必ず定義すること

保存パスは絶対パスで指定すること

Maxwell の Solve は時間がかかるため、DOE で並列化すること

# 10. Python からの呼び出し（Integration）
Python DOE では以下のように VBS を呼び出します。

電流 I₁, I₂ を Python で生成

VBS に渡す

Maxwell をバッチ実行

CSV を受け取る

マップを補間する
