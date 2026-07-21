import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ==================== 数据准备（请替换为真实数据） ====================
data = {
    'SNP_Count': [1000, 5000, 10000, 25000, 50000, 75000, 100000, 150000, 200000,
                  250000, 300000, 400000, 500000, 600000, 700000, 796678],
    'aMap':        [],   # 请填入实际运行时间（秒）
    'flare':       [],   # 请填入实际运行时间（秒）
    'salai-net':   [],   # 请填入实际运行时间（秒）
    'rfmix':       []    # 请填入实际运行时间（秒）
}
df = pd.DataFrame(data)

# 提取数据
snp_counts = df['SNP_Count'].values
software_names = ['aMap', 'flare', 'salai-net', 'rfmix']   # 明确4个软件

# ==================== 绘图 ====================
plt.figure(figsize=(12, 8))

# 样式设置（4个软件）
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
markers = ['o', 's', '^', 'D']
line_styles = ['-', '--', '-.', ':']
marker_sizes = [6, 6, 6, 5]

# 绘制各软件曲线
for i, software in enumerate(software_names):
    plt.plot(snp_counts, df[software].values,
             marker=markers[i],
             markersize=marker_sizes[i],
             linewidth=2,
             linestyle=line_styles[i],
             label=software,
             color=colors[i],
             alpha=0.8)

# 图表设置
plt.xlabel('Number of SNPs', fontsize=14, fontweight='bold')
plt.ylabel('Running Time (seconds)', fontsize=14, fontweight='bold')
plt.title('Comparison of Running Time Across Different SNP with two Populations Analysis Tools',
          fontsize=16, fontweight='bold', pad=15)

plt.xscale('log')
plt.yscale('log')

# 刻度设置
x_ticks = [1000, 5000, 10000, 50000, 100000, 500000, 796678]
x_tick_labels = ['1k', '5k', '10k', '50k', '100k', '500k', '797k']
plt.xticks(x_ticks, x_tick_labels, fontsize=12)

y_ticks = [0.1, 1, 10, 100, 1000, 10000]
y_tick_labels = ['0.1', '1', '10', '100', '1000', '10000']
plt.yticks(y_ticks, y_tick_labels, fontsize=12)

plt.grid(True, alpha=0.3, linestyle='--', which='both')
plt.legend(fontsize=12, loc='upper left', frameon=True, framealpha=0.9)
plt.tight_layout()

plt.savefig('SNP_Runtime_Comparison.png', dpi=300, bbox_inches='tight')
print("Figure saved as 'SNP_Runtime_Comparison.png'")
plt.show()

# ==================== 生成报告 ====================
report_lines = []
report_lines.append("=" * 80)
report_lines.append("SNP ANALYSIS TOOLS PERFORMANCE REPORT")
report_lines.append("=" * 80)
report_lines.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append(f"Number of SNP data points: {len(snp_counts)}")
report_lines.append(f"SNP range: {snp_counts[0]:,} to {snp_counts[-1]:,}")
report_lines.append("=" * 80)

# 1. 基本统计
report_lines.append("\n1. BASIC STATISTICS (All times in seconds):")
report_lines.append("-" * 80)
report_lines.append(f"{'Tool':<12} {'Min':>10} {'Max':>10} {'At max SNPs':>12} {'Relative Speed':>15}")
report_lines.append("-" * 80)

# 收集数据用于排序
stat_data = []
for sw in software_names:
    times = df[sw].values
    min_t = times.min()
    max_t = times.max()
    last_t = times[-1]
    stat_data.append({'tool': sw, 'min': min_t, 'max': max_t, 'last': last_t})

# 找出最快工具（基于最大SNP处的耗时）
fastest_tool = min(stat_data, key=lambda x: x['last'])
fastest_time = fastest_tool['last']

# 输出统计行，相对速度基于最快工具
for item in stat_data:
    ratio = item['last'] / fastest_time
    report_lines.append(f"{item['tool']:<12} {item['min']:>10.2f} {item['max']:>10.2f} {item['last']:>12.2f} {ratio:>15.1f}x")

# 2. 性能排名（从最快到最慢）
report_lines.append("\n2. PERFORMANCE RANKING (at max SNPs, fastest to slowest):")
report_lines.append("-" * 80)
sorted_by_last = sorted(stat_data, key=lambda x: x['last'])
for i, item in enumerate(sorted_by_last, 1):
    if i == 1:
        rank_str = f"{i}. {item['tool']} (Fastest) - {item['last']:.2f}s"
    else:
        slower = item['last'] / sorted_by_last[0]['last']
        rank_str = f"{i}. {item['tool']} - {item['last']:.2f}s ({slower:.1f}x slower than {sorted_by_last[0]['tool']})"
    report_lines.append(rank_str)

# 3. 时间复杂度分析
report_lines.append("\n3. TIME COMPLEXITY ANALYSIS:")
report_lines.append("-" * 80)
for sw in software_names:
    times = df[sw].values
    growth = times[-1] / times[0]
    snp_growth = snp_counts[-1] / snp_counts[0]
    exp = np.log(growth) / np.log(snp_growth)
    if exp < 1.2:
        comp = "~O(n) (linear)"
    elif exp < 1.5:
        comp = "~O(n log n)"
    elif exp < 2.2:
        comp = "~O(n²) (quadratic)"
    else:
        comp = f"~O(n^{exp:.1f}) (super-quadratic)"
    report_lines.append(f"{sw:<12}: Time grows {growth:.1f}x for {snp_growth:.1f}x SNPs. Estimated complexity: {comp}")

# 4. 关键发现
report_lines.append("\n4. KEY FINDINGS:")
report_lines.append("-" * 80)
fastest = sorted_by_last[0]['tool']
slowest = sorted_by_last[-1]['tool']
diff = sorted_by_last[-1]['last'] / sorted_by_last[0]['last']
report_lines.append(f"• Fastest tool: {fastest} ({sorted_by_last[0]['last']:.1f}s at max SNPs)")
report_lines.append(f"• Slowest tool: {slowest} ({sorted_by_last[-1]['last']:.1f}s at max SNPs)")
report_lines.append(f"• Performance gap: {slowest} is {diff:.1f}x slower than {fastest}")
report_lines.append(f"• Time range: From {min([d['min'] for d in stat_data]):.2f}s to {max([d['max'] for d in stat_data]):.2f}s")
report_lines.append(f"• For small datasets (<10k SNPs): All tools likely complete in under 10 seconds (verify with data)")
report_lines.append(f"• For large datasets (>500k SNPs): Performance differences become significant")

# 5. 建议
report_lines.append("\n5. RECOMMENDATIONS:")
report_lines.append("-" * 80)
report_lines.append(f"• For time-critical applications: Use {fastest} (fastest overall)")
report_lines.append(f"• For small datasets (<50k SNPs): Any tool is acceptable (all < 1 minute if data supports)")
report_lines.append(f"• For medium datasets (50k-200k SNPs): Consider {fastest} or second fastest")
report_lines.append(f"• For large datasets (>200k SNPs): {fastest} is recommended (best scaling)")

# 6. 详细数据表
report_lines.append("\n6. DETAILED DATA TABLE (Running Time in seconds):")
report_lines.append("-" * 80)
header = f"{'SNP Count':>10} " + " ".join([f"{sw:>12}" for sw in software_names])
report_lines.append(header)
report_lines.append("-" * (10 + 13 * len(software_names)))
for idx in range(len(snp_counts)):
    snp_str = f"{snp_counts[idx]:>10,}" if snp_counts[idx] >= 10000 else f"{snp_counts[idx]:>10}"
    time_strs = [f"{df[sw].values[idx]:>12.2f}" for sw in software_names]
    report_lines.append(snp_str + " " + " ".join(time_strs))

report_lines.append("=" * 80)

# 保存报告
report_filename = 'SNP_Tools_Performance_Report.txt'
with open(report_filename, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))
print(f"Report saved as '{report_filename}'")

# 打印摘要
print("\n" + "="*80)
print("QUICK SUMMARY")
print("="*80)
print(f"Fastest tool: {fastest} ({sorted_by_last[0]['last']:.2f}s at max SNPs)")
print(f"Slowest tool: {slowest} ({sorted_by_last[-1]['last']:.2f}s at max SNPs)")
print(f"Speed difference: {diff:.1f}x")
print(f"Graph saved as: SNP_Runtime_Comparison.png")
print(f"Report saved as: {report_filename}")
print("="*80)
