import numpy as np
import matplotlib.pyplot as plt
import nafusion_utils as na
na.set_style()

# 日本語フォントの設定（Macおよび主要OSに対応するフォント優先順位）
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'TakaoPGothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def mtanh_pedestal_profile(r, n_core=1.0, n_ped=0.75, n_sep=0.20, r_mid=0.96, delta=0.018, core_peaking=0.3):
    r"""
    Modified Tanh (mtanh) プロファイルによる核融合プラズマHモード密度プロファイル
    
    Parameters:
    -----------
    r : numpy.ndarray
        規格化半径 \rho = r/a
    n_core : float
        中心電子密度 [10^20 m^-3]
    n_ped : float
        ペデスタル肩部 (Pedestal Top) の電子密度 [10^20 m^-3]
    n_sep : float
        最外磁気面 (Separatrix, r/a=1.0) での電子密度 [10^20 m^-3]
    r_mid : float
        ペデスタル傾斜領域の中央位置 (規格化半径)
    delta : float
        ペデスタル半幅パラメータ (\Delta_{ped} \approx 4 * delta)
    core_peaking : float
        コアプラズマの密度向上パラメータ
    """
    # 1. ペデスタル〜端部輸送障壁（ETB）のなめらかなmtanhプロファイル
    # r = r_mid で (n_ped + n_sep)/2 となり、両側にスムーズに接続
    pedestal_term = 0.5 * (1.0 - np.tanh((r - r_mid) / delta))
    n_ped_profile = n_sep + (n_ped - n_sep) * pedestal_term
    
    # 2. コア領域 (r < r_mid) でのゆるやかな密度増加 (エラー警告防止用np.maximum)
    r_ped_top = r_mid - 2.0 * delta  # ペデスタル肩部の位置 (~0.924)
    core_mask = r < r_ped_top
    base_val = np.maximum(0.0, 1.0 - (r / r_ped_top)**2)
    core_shape = np.where(core_mask, base_val**core_peaking, 0.0)
    n_core_profile = (n_core - n_ped) * core_shape
    
    # 3. SOL（最外磁気面外側 r/a > 1.0）での指数関数的減衰
    sol_decay_length = 0.04
    n_sol_profile = n_sep * np.exp(-(r - 1.0) / sol_decay_length)
    
    # 全領域の結合 (r > 1.0 では SOL 減衰を合成)
    profile = np.where(r > 1.0, n_sol_profile, n_ped_profile + n_core_profile)
    return profile

def plot_hmode_density_profile(save_path="/Users/kobarahayato/.gemini/antigravity-ide/scratch/hmode_density_profile/hmode_density_profile.png", show=True):
    # 規格化半径 (r/a) : 0.0 (中心) 〜 1.15 (SOL領域)
    r = np.linspace(0, 1.15, 1000)
    
    # 主要パラメータ (典型的なトカマクHモードプラズマ)
    n_core = 1.00    # 1.0 x 10^20 m^-3
    n_ped = 0.75     # 0.75 x 10^20 m^-3
    n_sep = 0.20     # 0.20 x 10^20 m^-3
    r_mid = 0.96
    delta = 0.018    # ペデスタル幅 \Delta_{ped} \approx 0.072 (4 * delta)
    r_ped_top = r_mid - 2.0 * delta  # r/a = 0.924
    
    # Hモード密度プロファイルの計算
    n_e_hmode = mtanh_pedestal_profile(r, n_core, n_ped, n_sep, r_mid, delta, core_peaking=0.3)
    
    # Lモード密度プロファイルの計算（比較用：ペデスタル/輸送障壁がない低閉じ込めモード）
    lmode_core = np.maximum(0.0, 1.0 - (r / 1.0)**2)**1.2
    n_e_lmode = n_sep + (n_core - n_sep) * lmode_core
    n_e_lmode[r > 1.0] = n_sep * np.exp(-(r[r > 1.0] - 1.0) / 0.04)

    # グラフの作成 (16:9に近いアスペクト比で見やすい高解像度描画)
    fig, ax = plt.subplots(figsize=(10.5, 6.8), dpi=300)
    


    # プロファイル曲線の描画
    ax.plot(r, n_e_hmode, color='#dc2626', linewidth=3.2, label='Hモード密度プロファイル $n_e(r/a)$')
    ax.plot(r, n_e_lmode, color='#475569', linewidth=2.0, linestyle='--', alpha=0.75, label='Lモード密度プロファイル（比較参考）')

    # 重要な境界線（セパラトリクス & ペデスタル肩部）
    ax.axvline(x=1.0, color='#1e293b', linestyle=':', linewidth=1.8)
    ax.axvline(x=r_ped_top, color='#ef4444', linestyle=':', linewidth=1.5)

    # --- ペデスタル領域の注釈・アノテーション ---
    
    

    # 2. 端部輸送障壁 (Edge Transport Barrier: ETB)
    ax.annotate(
        '端部輸送障壁 (ETB)\n急峻な密度勾配 (Steep Gradient)',
        xy=(r_mid, (n_ped + n_sep)/2.0), xytext=(0.4, 0.42),
        arrowprops=dict(facecolor='#ef4444', edgecolor='#ef4444', arrowstyle='->', lw=2.2, shrinkB=4),
        fontsize=16, fontweight='bold', color='#991b1b',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef2f2', edgecolor='#ef4444', alpha=0.95)
    )

    # 軸ラベル・タイトル・目盛りの設定
    ax.set_xlabel('normalized radius $\\rho = r/a$', fontsize=28, fontweight='bold', labelpad=10)
    ax.set_ylabel('electron density $n_e \\ [10^{20}\\ \\mathrm{m^{-3}}]$', fontsize=27, fontweight='bold', labelpad=10)
    
    # 軸の表示範囲・目盛り・グリッド
    ax.set_xlim(0, 1.15)
    ax.set_ylim(0, 1.20)
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=16)
    ax.grid(True, linestyle='--', alpha=0.45)

    # 凡例（文字サイズをさらに拡大）
    ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.95, edgecolor='#cbd5e1', fontsize=20)

    # レイアウト調整と保存
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=600)
        print(f"Graph successfully generated and saved to: {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()

if __name__ == "__main__":
    plot_hmode_density_profile(show=True)
