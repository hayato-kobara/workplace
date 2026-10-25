import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# パラメータ設定
# ==========================================
N = 64          # グリッド数 (PoCのため小さめに設定)
L = 20.0        # 空間領域のサイズ
c = 1.0         # 電子の断熱性パラメータ (ドリフト波と不安定性の結合度合い)
kappa = 1.0     # 背景密度勾配の強さ (不安定性を駆動するエネルギー源)
nu = 0.01       # 運動量拡散係数 (数値的安定化のための人工粘性)
D = 0.01        # 粒子拡散係数
dt = 0.005      # 時間刻み幅
steps = 1500    # シミュレーションのステップ数

# ==========================================
# 空間グリッドと波数ベクトルの初期化
# ==========================================
dx = L / N
x = np.linspace(0, L, N, endpoint=False)
y = np.linspace(0, L, N, endpoint=False)
X, Y = np.meshgrid(x, y)

# フーリエ空間の波数ベクトル (kx, ky)
kx = np.fft.fftfreq(N, d=dx) * 2 * np.pi
ky = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY = np.meshgrid(kx, ky)

# 波数ベクトルの二乗 K^2 = kx^2 + ky^2
K2 = KX**2 + KY**2
K2[0, 0] = 1e-10  # ゼロ割り防止用

# ==========================================
# 初期条件の設定 (微小なランダムノイズ)
# ==========================================
np.random.seed(42)
n = np.random.randn(N, N) * 0.1
zeta = np.random.randn(N, N) * 0.1

# ==========================================
# ヘルパー関数: スペクトル法による微分
# ==========================================
def get_phi(zeta_k):
    """ ポアソン方程式 ∇^2 phi = zeta をフーリエ空間で解く """
    phi_k = -zeta_k / K2
    phi_k[0, 0] = 0.0
    return phi_k

def calc_derivatives(f_k):
    """ フーリエ空間のデータから x, y 方向の空間微分を計算する """
    df_dx = np.fft.ifft2(1j * KX * f_k).real
    df_dy = np.fft.ifft2(1j * KY * f_k).real
    return df_dx, df_dy

# ==========================================
# メインループ (時間発展)
# ==========================================
for i in range(steps):
    # 現在の n, zeta をフーリエ空間へ変換
    zeta_k = np.fft.fft2(zeta)
    n_k = np.fft.fft2(n)
    
    # 1. 渦度からポテンシャル phi を算出
    phi_k = get_phi(zeta_k)
    phi = np.fft.ifft2(phi_k).real
    
    # 2. 空間微分の計算
    dphi_dx, dphi_dy = calc_derivatives(phi_k)
    dzeta_dx, dzeta_dy = calc_derivatives(zeta_k)
    dn_dx, dn_dy = calc_derivatives(n_k)
    
    # 3. ポアソン括弧 [phi, f] の計算 (E×Bドリフトによる移流項)
    pb_zeta = dphi_dx * dzeta_dy - dphi_dy * dzeta_dx
    pb_n = dphi_dx * dn_dy - dphi_dy * dn_dx
    
    # 4. 散逸項 (拡散と粘性) の計算
    diff_zeta = np.fft.ifft2(-K2 * zeta_k).real * nu
    diff_n = np.fft.ifft2(-K2 * n_k).real * D
    
    # 5. 時間微分の計算 (長谷川・若谷方程式の右辺)
    dzeta_dt = -pb_zeta + c * (phi - n) + diff_zeta
    dn_dt = -pb_n + c * (phi - n) - kappa * dphi_dy + diff_n
    
    # 6. 時間積分 (前進オイラー法)
    zeta += dzeta_dt * dt
    n += dn_dt * dt

# ==========================================
# 結果の可視化
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

im1 = ax1.pcolormesh(X, Y, n, shading='auto', cmap='plasma')
ax1.set_title("Density fluctuation (n)")
fig.colorbar(im1, ax=ax1)

im2 = ax2.pcolormesh(X, Y, phi, shading='auto', cmap='viridis')
ax2.set_title("Electrostatic potential (phi)")
fig.colorbar(im2, ax=ax2)

plt.tight_layout()
plt.show()