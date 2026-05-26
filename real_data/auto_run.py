#!/usr/bin/env python3
"""
batch_convert_haplotypes.py
================================
功能：
  1. 遍历 chr1 ~ chr22 子文件夹，从每个文件夹的 ASW.phased 中提取个体 NA19834，
     生成对应 chrN 文件夹下的 NA19834_chrN.phased
  2. 调用 to_vcf.py 将该个体文件与 CHS/CEU/YRI 三个参考文件转换为 VCF，
     输出到同一 chrN 文件夹下
  3. 用 bgzip 压缩生成的 VCF 文件

支持断点续传：若对应染色体的 NA19834_chrN.phased、NA19834_chrN.vcf.gz、ref_chrN.vcf.gz 均已存在，
               则跳过该染色体（除非使用 --force）。

用法：
  python3 batch_convert_haplotypes.py <数据根目录> [--force]

示例：
  python3 batch_convert_haplotypes.py /path/to/data_folder
  python3 batch_convert_haplotypes.py /path/to/data_folder --force

依赖：
  - pandas (用于提取)
  - bgzip 命令 (通常来自 samtools 或 htslib)
  - to_vcf.py 脚本必须与此脚本放在同一目录
"""

import os
import sys
import subprocess
import argparse
import pandas as pd

# ========== 配置 ==========
TO_VCF_SCRIPT = "./to_vcf.py"   # 脚本位置
BGZIP_CMD = "bgzip"             # 系统命令

# ========== 功能1：提取个体 ==========
def extract_individual_phased(asw_file: str, ind_id: str, out_file: str) -> None:
    """
    从 ASW.phased 文件中提取指定个体的两列基因型，输出新文件。
    
    参数：
        asw_file : 输入的 ASW.phased 文件路径
        ind_id   : 个体名（如 NA19834），函数会自动查找 ind_id_A 和 ind_id_B 列
        out_file : 输出的 .phased 文件路径（保留前两列 + 该个体的两列）
    """
    print(f"  提取个体 {ind_id} 从 {asw_file} -> {out_file}")
    try:
        df = pd.read_csv(asw_file, sep='\t', dtype=str)
        if len(df.columns) < 2:
            raise ValueError("文件列数不足2，无法保留前两列")
        
        # 保留前两列（通常为 rsID 和 POS）
        fixed_cols = df.columns[:2].tolist()
        
        # 查找个体对应的两列
        col_a = f"{ind_id}_A"
        col_b = f"{ind_id}_B"
        if col_a not in df.columns or col_b not in df.columns:
            raise ValueError(f"在 {asw_file} 中未找到列 {col_a} 或 {col_b}")
        
        # 提取数据
        df_out = df[fixed_cols + [col_a, col_b]]
        df_out.to_csv(out_file, sep='\t', index=False)
        print(f"    ✓ 已生成 {out_file} (行数: {len(df_out)})")
    except Exception as e:
        print(f"    ✗ 提取失败: {e}")
        raise

# ========== 功能2+3：转换VCF并压缩 ==========
def run_conversion(chrom: int, phased_file: str, ref_files: list, out_vcf_sample: str, out_vcf_ref: str):
    """
    调用 to_vcf.py 将提取的个体文件与参考群体文件转换为 VCF，
    然后压缩生成的 VCF 文件。
    """
    # 2. 转换
    cmd = [
        "python3", TO_VCF_SCRIPT,
        "-i1", phased_file,
        "-i2"] + ref_files + [
        "-o1", out_vcf_sample,
        "-o2", out_vcf_ref,
        "-c", str(chrom)
    ]
    print(f"  转换 VCF (染色体 {chrom}): {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  转换失败:\n{result.stderr}")
        return False
    print(f"    ✓ 已生成 {out_vcf_sample} 和 {out_vcf_ref}")
    
    # 3. 压缩
    for vcf_file in [out_vcf_sample, out_vcf_ref]:
        if os.path.exists(vcf_file):
            gz_file = vcf_file + ".gz"
            # 先检查 bgzip 是否可用
            if subprocess.run(["which", BGZIP_CMD], capture_output=True).returncode == 0:
                subprocess.run([BGZIP_CMD, "-f", vcf_file], check=True)
                print(f"    ✓ 已压缩 {gz_file}")
            else:
                print(f"    ⚠️ {BGZIP_CMD} 未找到，跳过压缩，保留 {vcf_file}")
        else:
            print(f"    ✗ 警告: {vcf_file} 不存在，无法压缩")
    return True

# ========== 主程序 ==========
def main():
    parser = argparse.ArgumentParser(description="批量转换 HapMap 到 VCF，支持断点续传")
    parser.add_argument("root_dir", help="包含 chr1..chr22 子文件夹的根目录")
    parser.add_argument("--force", action="store_true", help="强制重新处理所有染色体（忽略已有文件）")
    args = parser.parse_args()

    root_dir = args.root_dir.rstrip('/')
    if not os.path.isdir(root_dir):
        print(f"错误: 目录 '{root_dir}' 不存在")
        sys.exit(1)
    
    # 检查 to_vcf.py 是否存在
    if not os.path.isfile(TO_VCF_SCRIPT):
        print(f"错误: 找不到 {TO_VCF_SCRIPT}，请确保它与本脚本在同一目录")
        sys.exit(1)
    
    # 检查 bgzip（可选，若没有则警告）
    if subprocess.run(["which", BGZIP_CMD], capture_output=True).returncode != 0:
        print(f"警告: 系统中未找到 {BGZIP_CMD} 命令，将跳过压缩步骤")
        print("      如需压缩，请安装 samtools 或 htslib")
    
    # 遍历染色体 1-22
    for chrom in range(1, 23):
        chr_dir = os.path.join(root_dir, f"chr{chrom}")
        if not os.path.isdir(chr_dir):
            print(f"跳过: {chr_dir} 不存在")
            continue
        
        # 定义输出文件路径（均放在当前染色体的文件夹内）
        extracted_phased = os.path.join(chr_dir, f"NA19834_chr{chrom}.phased")
        out_vcf_sample = os.path.join(chr_dir, f"NA19834_chr{chrom}.vcf")
        out_vcf_ref = os.path.join(chr_dir, f"ref_chr{chrom}.vcf")
        out_vcf_sample_gz = out_vcf_sample + ".gz"
        out_vcf_ref_gz = out_vcf_ref + ".gz"

        # 断点续传：若三个目标文件均已存在且未使用 --force，则跳过该染色体
        if not args.force:
            files_exist = all([
                os.path.exists(extracted_phased),
                os.path.exists(out_vcf_sample_gz),
                os.path.exists(out_vcf_ref_gz)
            ])
            if files_exist:
                print(f"\n===== 染色体 {chrom} 已完成（三个输出文件均已存在），跳过 =====")
                continue

        # 检查必需的输入文件
        asw_file = os.path.join(chr_dir, "ASW.phased")
        ref_files = [
            os.path.join(chr_dir, f"your_chs_chr{chrom}.phased"),
            os.path.join(chr_dir, f"your_ceu_chr{chrom}.phased"),
            os.path.join(chr_dir, f" your_yri_chr{chrom}.phased")
        ]
        missing = []
        if not os.path.isfile(asw_file):
            missing.append(asw_file)
        for rf in ref_files:
            if not os.path.isfile(rf):
                missing.append(rf)
        if missing:
            print(f"染色体 {chrom} 缺失以下文件，跳过: {missing}")
            continue
        
        print(f"\n===== 处理染色体 {chrom} 文件夹: {chr_dir} =====")
        
        # 1. 提取 NA19834（如果已存在，可跳过？但为了保险，重新提取）
        try:
            extract_individual_phased(asw_file, "NA19834", extracted_phased)
        except Exception:
            print(f"染色体 {chrom} 提取失败，跳过转换")
            continue
        
        # 2. 转换 VCF 并压缩
        success = run_conversion(chrom, extracted_phased, ref_files, out_vcf_sample, out_vcf_ref)
        if not success:
            print(f"染色体 {chrom} 转换失败")
        else:
            print(f"染色体 {chrom} 处理完成")
    
    print("\n所有染色体处理完毕！")

if __name__ == "__main__":
    main()
