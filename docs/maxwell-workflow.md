# Maxwell Workflow – インダクタンスマップ生成手順
本ページでは、磁気結合リアクトルの 電流依存インダクタンスマップ L(I₁,I₂), M(I₁,I₂) を
ANSYS Maxwell 3D を用いて自動生成するためのワークフローをまとめます。

# 1. 目的（Purpose）
磁気結合リアクトルは、漏れ磁束を積極的に利用するため 線形インダクタンスモデルが使えません。
そのため、Maxwell 3D を用いて以下の値を 電流 I₁, I₂ の関数として取得します。

L1(I₁, I₂)

L2(I₁, I₂)

M(I₁, I₂)

漏れ磁束分布（Bx, By, Bz）

これらを Python 側でマップ化し、Ripple 計算や損失計算に使用します。

# 2. モデル構成（Model Structure）
Maxwell モデルは以下の構成で作成します。

2つのコイル（L1, L2）

巻き方向は逆（ドット極性が反転）  
→ 両コイルに下→上の電流が流れると DC 磁束が打ち消し合う

漏れ磁束経路を含む 3D コア形状

I₁, I₂ を独立に設定可能な励磁条件

# 3. 電流パラメータの掃引（Parameter Sweep）
Maxwell のパラメトリック解析で、以下のように電流を掃引します。

パラメータ	範囲	目的
I₁	0 → Imax	L1 の電流依存性
I₂	0 → Imax	L2 の電流依存性
I₁ × I₂	全組み合わせ	M(I₁,I₂) の電流依存性


例：

I₁ = 0, 25, 50, 75, 100 A

I₂ = 0, 25, 50, 75, 100 A

→ 25 ケース × 3 種類のインダクタンス = 75 データ

この掃引を Python DOE で自動化すると、約 12 時間で完了します。(1/4モデル 電流27 x 27水準　1水準あたり3min)

# 4. VBS 自動化スクリプト（Automation Script）
Maxwell の操作はすべて VBS で自動化します。

主な処理内容
モデルパラメータの設定

電流 I₁, I₂ のセット

計算実行

L1, L2, M の抽出

漏れ磁束分布の保存

CSV 出力

重要ポイント
巻き方向（極性）を正しく設定すること

I₁, I₂ の符号が DC フラックスキャンセルに一致すること

漏れ磁束用の座標系（leakix, leakiz など）を定義すること

# 5. 出力データ形式（Output Format）
result_map.csv

<img width="733" height="393" alt="result_map" src="https://github.com/user-attachments/assets/cff25000-5798-4974-aacf-42f4b3d8bd44" />

# 6. 計算結果例（Example Results）
インダクタンスマップ例



