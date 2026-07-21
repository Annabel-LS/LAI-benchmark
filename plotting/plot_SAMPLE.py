import pandas as pd
import matplotlib.pyplot as plt
import re

# ==================== 字体设置 ====================
# 尝试使用 Arial，若不存在则使用 Times New Roman
try:
    from matplotlib.font_manager import FontProperties
    arial_font = FontProperties(family='Arial')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Times New Roman', 'DejaVu Sans']
except:
    # 如果 Arial 不可用，使用 Times New Roman
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# ==================== 数据准备（根据最新 Excel 文件更新） ====================
data = {
    'Software': ['amap', 'flare', 'salai', 'rfmix', 'loter'],
    '20': [],
    '60': [],
    '80': [],
    '99': []
}

df = pd.DataFrame(data)
df.set_index('Software', inplace=True)

print("Data loaded successfully!")
print(f"Sample sizes: {list(df.columns)}")
print(f"Software names: {list(df.index)}")

# 样本数（直接从列名获取，均为数字）
sample_sizes = [20, 60, 80, 99]
print(f"Extracted sample sizes: {sample_sizes}")

# ==================== 绘制折线图 ====================
plt.figure(figsize=(14, 9))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
markers = ['o', 's', '^', 'D', 'v']
line_styles = ['-', '--', '-.', ':', '-']
marker_sizes = [8, 8, 8, 6, 8]  # loter 使用稍小的标记

for i, (software, row) in enumerate(df.iterrows()):
    plt.plot(sample_sizes, row.values,
             marker=markers[i % len(markers)],
             markersize=marker_sizes[i],
             linewidth=2.5,
             linestyle=line_styles[i % len(line_styles)],
             label=software,
             color=colors[i % len(colors)],
             alpha=0.8)

plt.xlabel('Number of Samples', fontsize=14, fontweight='bold')
plt.ylabel('Running Time (seconds) - Log Scale', fontsize=14, fontweight='bold')
plt.title('Running Time vs Sample Size for Different Software', 
          fontsize=16, fontweight='bold', pad=20)

plt.xticks(sample_sizes, [f'{s}' for s in sample_sizes], fontsize=12)

# 对数刻度
plt.yscale('log')
y_ticks = [1, 10, 100, 1000, 10000, 100000]
y_tick_labels = ['1', '10', '100', '1k', '10k', '100k']
plt.yticks(y_ticks, y_tick_labels, fontsize=12)

plt.grid(True, alpha=0.3, linestyle='--', which='both')
plt.legend(fontsize=12, loc='lower right', frameon=True, framealpha=0.9, 
           bbox_to_anchor=(0.98, 0.02), ncol=1)

plt.tight_layout()

# 保存为 TIFF 格式，DPI 改为 600
plt.savefig('runtime_vs_samples.tiff', dpi=600, bbox_inches='tight')
print("\nFigure saved as 'runtime_vs_samples.tiff' (600 DPI)")

plt.show()

# ==================== 输出数据摘要 ====================
print("\n" + "=" * 80)
print("DATA SUMMARY")
print("=" * 80)
print(f"{'Software':<8} {'20 samples':>12} {'60 samples':>12} {'80 samples':>12} {'99 samples':>12}")
print("-" * 80)

for software in df.index:
    times = df.loc[software]
    print(f"{software:<8} {times[0]:>12.2f} {times[1]:>12.2f} {times[2]:>12.2f} {times[3]:>12.2f}")

print("=" * 80)
