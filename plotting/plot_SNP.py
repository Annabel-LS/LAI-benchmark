import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Create DataFrame
data = {
    'SNP_Count': [1000, 5000, 10000, 25000, 50000, 75000, 100000, 150000, 200000, 
                  250000, 300000, 400000, 500000, 600000, 700000, 796678],
    'aMap': [],
    'flare': [],
    'salai-net': [],
    'loter': [],
    'rfmix': []
}

df = pd.DataFrame(data)

# Extract data properly
snp_counts = df['SNP_Count'].values  # Convert to numpy array
last_snp_count = snp_counts[-1]  # Last SNP count
aMap_last_time = df['aMap'].values[-1]  # Last aMap time

# Create figure
plt.figure(figsize=(12, 8))

# Set colors and styles
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
markers = ['o', 's', '^', 'D', 'v']
line_styles = ['-', '--', '-.', ':', '-']
marker_sizes = [6, 6, 6, 5, 5]

software_names = ['aMap', 'flare', 'salai-net', 'loter', 'rfmix']

# Plot each software
for i, software in enumerate(software_names):
    plt.plot(snp_counts, df[software].values, 
             marker=markers[i],
             markersize=marker_sizes[i],
             linewidth=2,
             linestyle=line_styles[i],
             label=software,
             color=colors[i],
             alpha=0.8)

# Configure plot
plt.xlabel('Number of SNPs', fontsize=14, fontweight='bold')
plt.ylabel('Running Time (seconds)', fontsize=14, fontweight='bold')
plt.title('Comparison of Running Time Across Different SNP with two Populations Analysis Tools', 
          fontsize=16, fontweight='bold', pad=15)

# Set log scale for both axes
plt.xscale('log')
plt.yscale('log')

# Set x-axis ticks
x_ticks = [1000, 5000, 10000, 50000, 100000, 500000, 796678]
x_tick_labels = ['1k', '5k', '10k', '50k', '100k', '500k', '797k']
plt.xticks(x_ticks, x_tick_labels, fontsize=12)

# Set y-axis ticks
y_ticks = [0.1, 1, 10, 100, 1000, 10000]
y_tick_labels = ['0.1', '1', '10', '100', '1000', '10000']
plt.yticks(y_ticks, y_tick_labels, fontsize=12)

# Add grid
plt.grid(True, alpha=0.3, linestyle='--', which='both')

# Add legend
plt.legend(fontsize=12, loc='upper left', frameon=True, framealpha=0.9)


# Adjust layout
plt.tight_layout()

# Save figure
plt.savefig('SNP_Runtime_Comparison.png', dpi=300, bbox_inches='tight')
print("Figure saved as 'SNP_Runtime_Comparison.png'")

# Display figure
plt.show()

# ==================== GENERATE REPORT ====================
# Create a comprehensive report
report_lines = []

report_lines.append("=" * 80)
report_lines.append("SNP ANALYSIS TOOLS PERFORMANCE REPORT")
report_lines.append("=" * 80)
report_lines.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append(f"Number of SNP data points: {len(snp_counts)}")
report_lines.append(f"SNP range: {snp_counts[0]:,} to {snp_counts[-1]:,}")
report_lines.append("=" * 80)

# 1. Basic Statistics
report_lines.append("\n1. BASIC STATISTICS (All times in seconds):")
report_lines.append("-" * 80)
report_lines.append(f"{'Tool':<12} {'Min':>10} {'Max':>10} {'At 797k SNPs':>12} {'Relative Speed':>15}")
report_lines.append("-" * 80)

statistics_data = []
for software in software_names:
    min_time = df[software].min()
    max_time = df[software].max()
    last_time = df[software].values[-1]
    
    # Calculate speed relative to aMap (the fastest)
    if software == 'aMap':
        speed_ratio = 1.0
    else:
        speed_ratio = last_time / aMap_last_time
    
    statistics_data.append({
        'tool': software,
        'min': min_time,
        'max': max_time,
        'last': last_time,
        'ratio': speed_ratio
    })
    
    report_lines.append(f"{software:<12} {min_time:>10.2f} {max_time:>10.2f} {last_time:>12.2f} {speed_ratio:>15.1f}x")

# 2. Performance Ranking
report_lines.append("\n2. PERFORMANCE RANKING (at 797k SNPs, fastest to slowest):")
report_lines.append("-" * 80)

# Sort tools by their last time (fastest first)
sorted_tools = sorted(statistics_data, key=lambda x: x['last'])
for i, tool_data in enumerate(sorted_tools, 1):
    if i == 1:
        rank_str = f"{i}. {tool_data['tool']} (Fastest) - {tool_data['last']:.2f}s"
    else:
        slower_by = tool_data['last'] / sorted_tools[0]['last']
        rank_str = f"{i}. {tool_data['tool']} - {tool_data['last']:.2f}s ({slower_by:.1f}x slower than {sorted_tools[0]['tool']})"
    report_lines.append(rank_str)

# 3. Time Complexity Analysis
report_lines.append("\n3. TIME COMPLEXITY ANALYSIS:")
report_lines.append("-" * 80)

# Calculate approximate time complexity (growth factor)
for software in software_names:
    times = df[software].values
    
    # Calculate growth from smallest to largest SNP count
    growth_factor = times[-1] / times[0]
    snp_growth = snp_counts[-1] / snp_counts[0]
    
    # Estimate time complexity (rough approximation)
    # If time grows linearly with SNP count, growth_factor ≈ snp_growth
    # We'll calculate an approximate exponent
    exponent = np.log(growth_factor) / np.log(snp_growth)
    
    if exponent < 1.2:
        complexity = "~O(n) (linear)"
    elif exponent < 1.5:
        complexity = "~O(n log n)"
    elif exponent < 2.2:
        complexity = "~O(n²) (quadratic)"
    else:
        complexity = f"~O(n^{exponent:.1f}) (super-quadratic)"
    
    report_lines.append(f"{software:<12}: Time grows {growth_factor:.1f}x for {snp_growth:.1f}x SNPs. Estimated complexity: {complexity}")

# 4. Key Findings
report_lines.append("\n4. KEY FINDINGS:")
report_lines.append("-" * 80)
fastest_tool = sorted_tools[0]['tool']
slowest_tool = sorted_tools[-1]['tool']
speed_difference = sorted_tools[-1]['last'] / sorted_tools[0]['last']

report_lines.append(f"• Fastest tool: {fastest_tool} ({sorted_tools[0]['last']:.1f}s at 797k SNPs)")
report_lines.append(f"• Slowest tool: {slowest_tool} ({sorted_tools[-1]['last']:.1f}s at 797k SNPs)")
report_lines.append(f"• Performance gap: {slowest_tool} is {speed_difference:.1f}x slower than {fastest_tool}")
report_lines.append(f"• Time range: From {df['aMap'].min():.2f}s (aMap, 1k SNPs) to {df['rfmix'].max():.2f}s (rfmix, 797k SNPs)")
report_lines.append(f"• For small datasets (<10k SNPs): All tools complete in under 10 seconds")
report_lines.append(f"• For large datasets (>500k SNPs): Performance differences become significant (65s vs 9716s)")

# 5. Recommendations
report_lines.append("\n5. RECOMMENDATIONS:")
report_lines.append("-" * 80)
report_lines.append(f"• For time-critical applications: Use {fastest_tool} (fastest overall)")
report_lines.append(f"• For small datasets (<50k SNPs): Any tool is acceptable (all < 1 minute)")
report_lines.append(f"• For medium datasets (50k-200k SNPs): Consider aMap or flare (under 5 minutes)")
report_lines.append(f"• For large datasets (>200k SNPs): aMap is recommended (best scaling)")

# 6. Data Summary Table
report_lines.append("\n6. DETAILED DATA TABLE (Running Time in seconds):")
report_lines.append("-" * 80)

# Create a formatted table
header = f"{'SNP Count':>10} " + " ".join([f"{tool:>12}" for tool in software_names])
report_lines.append(header)
report_lines.append("-" * (10 + 13*len(software_names)))

for idx in range(len(snp_counts)):
    snp_str = f"{snp_counts[idx]:>10,}" if snp_counts[idx] >= 10000 else f"{snp_counts[idx]:>10}"
    time_strs = [f"{df[tool].values[idx]:>12.2f}" for tool in software_names]
    report_lines.append(snp_str + " " + " ".join(time_strs))

report_lines.append("=" * 80)

# Save report to file
report_filename = 'SNP_Tools_Performance_Report.txt'
with open(report_filename, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f"Report saved as '{report_filename}'")

# Also print to console
print('\n'.join(report_lines[:50]))  # Print first 50 lines to console
print(f"\n... (full report saved to {report_filename})")

# Additional summary for quick view
print("\n" + "="*80)
print("QUICK SUMMARY")
print("="*80)
print(f"Fastest tool: {fastest_tool} ({sorted_tools[0]['last']:.2f}s at 797k SNPs)")
print(f"Slowest tool: {slowest_tool} ({sorted_tools[-1]['last']:.2f}s at 797k SNPs)")
print(f"Speed difference: {speed_difference:.1f}x")
print(f"Graph saved as: SNP_Runtime_Comparison.png")
print(f"Report saved as: {report_filename}")
print("="*80)
