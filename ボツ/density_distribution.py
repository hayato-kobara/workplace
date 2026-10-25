import numpy as np
import matplotlib.pyplot as plt
import nafusion_utils as na
na.set_style()

# 1. 平均(mu)と標準偏差(sigma)の設定
mu1 = 0
sigma1 = 0.8
mu2 = 0
sigma2 =0.3
# 2. xの範囲を設定（平均から左右に4シグマの範囲）
x = np.linspace(mu1 - 3 * sigma1, mu1 + 3 * sigma1, 1000)

# 3. 正規分布の確率密度関数 (PDF) の計算
y1 = (1 / (sigma1 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu1) / sigma1) ** 2)
y2 =0.6*( (1 / (sigma2 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu2) / sigma2) ** 2))
y3 = y1 + y2
# 4. グラフの描画
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y1, label="RF only")
ax.plot(x, y2, label="arc only")
ax.plot(x, y3, label="RF+arc")
# 5. 軸ラベルやタイトルの設定
ax.set_xlabel('Radial position', fontsize=20)
ax.set_ylabel('density', fontsize=20)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(fontsize=20)
# 横軸の下側（bottom）と、縦軸の左側（left）のラベルを非表示にする
ax.tick_params(labelbottom=False, labelleft=False)




# レイアウトの自動調整
fig.tight_layout()

# 6. 画像の保存
#plt.savefig('normal_distribution.png')

plt.show()
