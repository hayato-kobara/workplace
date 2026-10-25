import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import nafusion_utils as na
na.set_style()

# --- 定数の設定（アルゴン） ---
A = 13.6      # [1/(cm*Torr)]
B = 235     # [V/(cm*Torr)]
gamma = 0.1  # 二次電子放出係数 (電極材質により変動)

# パッシェン曲線の計算式
def paschen_voltage(pd, A, B, gamma):
    # 分母が0以下になる領域（対数の中身が負）でのエラーを防ぐ
    denominator = np.log(A * pd) - np.log(np.log(1 + 1/gamma))
    # 物理的に意味のない負の電圧や分母が負になる領域は NaN とする
    V = np.where(denominator > 0, (B * pd) / denominator, np.nan)
    return V

# --- 最小値の計算 ---
# 1. 解析解（数式からの直接計算）
e = np.exp(1)
C = np.log(1 + 1/gamma)
pd_min_ana = (e * C) / A
V_min_ana = (B * e * C) / A

# --- 修正版：数値最適化による計算 ---
# 最小値探索専用の関数（配列や np.inf を絶対に使わない）
def objective(pd_array):
    # NumPy配列から確実に取り出し、純粋なfloat型に変換
    pd = float(pd_array[0])
    
    # 対数の中身が0以下になるのを防ぐ
    if A * pd <= 0:
        return 1e9  # np.infの代わりに、ただの巨大な数値を返す
        
    denominator = np.log(A * pd) - np.log(np.log(1 + 1/gamma))
    
    # 分母が0以下（物理的に放電しない領域）の場合はペナルティ
    if denominator <= 0:
        return 1e9
        
    # 計算可能な場合は、純粋な数値(float)として返す
    return float((B * pd) / denominator)

# 初期値を 1.0 から「2.0」に変更して探索開始
# （アルゴリズムが初期値から本当に動いているかを確認するため）
res = minimize(objective, [2.0], bounds=[(0.1, 10.0)])
pd_min_num = res.x[0]
V_min_num = res.fun



print(f"【解析解】 最小値: pd = {pd_min_ana:.3f} [Torr·cm], V = {V_min_ana:.2f} [V]")
print(f"【数値解】 最小値: pd = {pd_min_num:.3f} [Torr·cm], V = {V_min_num:.2f} [V]")

# --- グラフのプロット ---
# pd の範囲を対数スケールで生成 (0.1 から 100 まで)
pd_values = np.logspace(-1, 2, 1000)
V_values = paschen_voltage(pd_values, A, B, gamma)

plt.figure(figsize=(8, 6))
plt.plot(pd_values, V_values, label=f'Argon ($\gamma$ = {gamma})', color='blue')

# 最小値のポイントを赤点でプロット
plt.scatter(pd_min_ana, V_min_ana, color='red', zorder=5, 
            label=f'Min: {V_min_ana:.1f} V at {pd_min_ana:.2f} Torr·cm')

# グラフの装飾
plt.xlabel('Pressure $\\times$ Distance ($pd$) [Torr$\\cdot$cm]', fontsize=12)
plt.ylabel('Breakdown Voltage ($V$) [V]', fontsize=12)
plt.title('Paschen Curve for Argon', fontsize=14)
plt.xscale('log')
plt.yscale('log')
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()

# 画像の保存と表示
plt.savefig('paschen_argon.png', dpi=300)
plt.show()