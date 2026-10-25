import numpy as np
import matplotlib.pyplot as plt

# xの範囲を設定（-2π から 2π までを1000等分して滑らかな線にする）
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

# yの値を計算
y_sin = np.sin(x)
y_cos = np.cos(x)

# グラフのサイズを設定
plt.figure(figsize=(8, 5))

# データをプロット（色とラベルも指定）
plt.plot(x, y_sin, label='y = sin(x)', color='blue')
plt.plot(x, y_cos, label='y = cos(x)', color='red')

# グラフの装飾
plt.title('Trigonometric Functions') # タイトル
plt.xlabel('x')                      # x軸ラベル
plt.ylabel('y')                      # y軸ラベル
plt.axhline(0, color='black', linewidth=0.8) # x軸の基準線(y=0)
plt.axvline(0, color='black', linewidth=0.8) # y軸の基準線(x=0)
plt.grid(True, linestyle='--', alpha=0.7)    # 点線のグリッドを表示
plt.legend()                         # 凡例（y=sin(x)などの説明）を表示

# グラフを画面に表示する
plt.show()