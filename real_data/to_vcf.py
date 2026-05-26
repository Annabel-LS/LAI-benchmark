#!/usr/bin/env python3
"""
to_vcf.py - hapmap格式转为vcf格式工具

该脚本用于hapmap格式转为vcf格式文件，支持以下参数：
  -i1 <hapmap格式样本文件>
  -i2 <ref文件><ref文件><ref文件> \
  -o1 <vcf格式样本文件路径> \
  -o2 <vcf格式ref文件路径> \
  -c <染色体号>

使用方法：
python3 to_vcf.py \
  -i1 sample.phased \
  -i2 ref1.phased ref2.phased ref3.phased \
  -o1 sample.vcf \
  -o2 ref.vcf \
  -c 1
"""

import argparse
from typing import List, Dict, Tuple


def parse_header(header_line: str) -> Dict[str, Tuple[int, int]]:
    cols = header_line.strip().split('\t')
    samples = {}
    for i in range(2, len(cols), 2):
        sample_name = cols[i].replace('_A', '')
        a_idx = i
        b_idx = i + 1 if (i + 1) < len(cols) else -1
        samples[sample_name] = (a_idx, b_idx)
    return samples


def build_genotypes(cols: List[str],
                    indices: Dict[str, Tuple[int, int]],
                    allele_map: Dict[str, str]) -> List[str]:
    gts = []
    for a_idx, b_idx in indices.values():
        a = cols[a_idx] if 0 <= a_idx < len(cols) else '.'
        b = cols[b_idx] if 0 <= b_idx < len(cols) else '.'
        a_gt = allele_map.get(a, '.')
        b_gt = allele_map.get(b, '.')
        gt = './.' if a_gt == '.' and b_gt == '.' else f"{a_gt}|{b_gt}"
        gts.append(gt)
    return gts


def write_vcf_header(outfile, sample_names: List[str]):
    outfile.write("##fileformat=VCFv4.2\n"
                  "##source=myConverter\n"
                  "##INFO=<ID=AF,Number=A,Type=Float,Description=\"Allele Frequency\">\n"
                  "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n"
                  "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT")
    if sample_names:
        outfile.write('\t' + '\t'.join(sample_names))
    outfile.write('\n')


def convert_hap_plus_merged_to_vcfs(hap_file: str,
                                    merged_files: List[str],
                                    out_vcf_sample: str,
                                    out_vcf_ref: str,
                                    chrID: str):
    fps_merged = [open(f, 'r') for f in merged_files]

    try:
        with open(hap_file, 'r') as f_hap, \
             open(out_vcf_sample, 'w') as fout_s, \
             open(out_vcf_ref,   'w') as fout_r:

            header_hap     = f_hap.readline().strip()
            headers_merged = [fp.readline().strip() for fp in fps_merged]

            samples_hap    = parse_header(header_hap)
            samples_merged = [parse_header(h) for h in headers_merged]

            if not samples_hap or any(not sm for sm in samples_merged):
                raise RuntimeError("Empty sample list")

            write_vcf_header(fout_s, list(samples_hap.keys()))
            ref_sample_names = [name for sm in samples_merged for name in sm.keys()]
            write_vcf_header(fout_r, ref_sample_names)

            line_num = 0
            while True:
                line_hap     = f_hap.readline()
                lines_merged = [fp.readline() for fp in fps_merged]

                if not line_hap and all(not lm for lm in lines_merged):
                    break
                line_num += 1

                cols_hap   = line_hap.strip().split('\t') if line_hap else []
                cols_merged_lst = [lm.strip().split('\t') if lm else [] for lm in lines_merged]

                pos = cols_hap[1] if len(cols_hap) > 1 else str(line_num)

                all_alleles = set()
                for a_idx, b_idx in samples_hap.values():
                    if a_idx < len(cols_hap) and cols_hap[a_idx] not in ['', '.']:
                        all_alleles.add(cols_hap[a_idx])
                    if b_idx < len(cols_hap) and cols_hap[b_idx] not in ['', '.']:
                        all_alleles.add(cols_hap[b_idx])
                for cols_m, sm in zip(cols_merged_lst, samples_merged):
                    for a_idx, b_idx in sm.values():
                        if a_idx < len(cols_m) and cols_m[a_idx] not in ['', '.']:
                            all_alleles.add(cols_m[a_idx])
                        if b_idx < len(cols_m) and cols_m[b_idx] not in ['', '.']:
                            all_alleles.add(cols_m[b_idx])

                alleles = sorted(all_alleles) if all_alleles else ['.', '.']
                if '.' in alleles:
                    alleles.remove('.')
                    alleles.insert(0, '.')
                allele_map = {a: str(i) for i, a in enumerate(alleles) if a != '.'}
                allele_map['.'] = '.'
                ref = alleles[0] if alleles else '.'
                alt = ','.join(alleles[1:]) if len(alleles) > 1 else '.'

                base_fields = [str(chrID), pos, '.', ref, alt, '.', '.', '.', 'GT']

                gts_s = build_genotypes(cols_hap, samples_hap, allele_map) if cols_hap else []
                if gts_s:
                    fout_s.write('\t'.join(base_fields + gts_s) + '\n')

                gts_r = []
                for cols_m, sm in zip(cols_merged_lst, samples_merged):
                    gts_r.extend(build_genotypes(cols_m, sm, allele_map))
                if gts_r:
                    fout_r.write('\t'.join(base_fields + gts_r) + '\n')

    finally:
        for fp in fps_merged:
            fp.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1', '--hap', required=True)
    parser.add_argument('-i2', '--merged', nargs='+', required=True)
    parser.add_argument('-o1', '--out1', required=True)
    parser.add_argument('-o2', '--out2', required=True)
    parser.add_argument('-c', '--chr', dest='chrID', required=True)
    args = parser.parse_args()

    convert_hap_plus_merged_to_vcfs(
        hap_file=args.hap,
        merged_files=args.merged,
        out_vcf_sample=args.out1,
        out_vcf_ref=args.out2,
        chrID=args.chrID
    )
    print('All VCF files generated successfully')


if __name__ == '__main__':
    main()
