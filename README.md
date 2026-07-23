# Ancestry Inference Software Benchmarking – Code Repository

This repository contains test code for evaluating the performance of four mainstream ancestry inference software tools (amap, flare, salai‑net, rfmix). The evaluation covers computational speed (influenced by the number of SNPs, number of samples, and multi‑way admixture), accuracy across different admixture generations, and robustness.

## Directory Structure
- `simulate_data_code/` – Contains scripts for generating simulated genotype data (`.txt` format) and ground‑truth ancestry labels.
- `workflows/` – Automates the execution of all benchmarking tests.
- `real_data_code/` – Automates data processing for real data.

## Dependencies

### System Requirements
- Python 3.8+
- Operating system: Linux

### Python Dependencies
Install the required libraries:
```bash
pip install matplotlib numpy pandas
Third‑Party Software
The benchmarking scripts in this repository use the following software. Please ensure they are installed before running the tests:

-amap:https:https://github.com/Annabel-LS/LAI-benchmark/releases/tag/1.6.

-flare:https://faculty.washington.edu/browning/flare.jar.

-salai‑net:https://github.com/AI-sandbox/SALAI-Net.git.

-rfmix:https://github.com/slowkoni/rfmix.
-ancestryView213:https://github.com/Annabel-LS/LAI-benchmark/releases/tag/2.13_1.4.0

Refer to each software’s official documentation for installation instructions.

Visualisation Software
ancestryView213: Used to plot sample ancestry composition.

Quick Start
Generate simulated data:

bash
python3 get_childrenV2.py
Run all tests:
Place the test scripts for each software in their respective software folders and modify the parameter paths. For example, the test script for evaluating the relationship between computational speed and number of SNPs is located at:
/aMAP_20140601_binary/test_SNP

When testing robustness with simulated data, you can run the software directly without the workflow.

Generate plots: Use ancestryView213 to visualise the results.

Real data:
auto_run.py – Automatically extracts and processes real data, calling VCF format conversion.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Citation
If you use this code in your research, please cite: Author(s), Title of the paper, Journal, Year (to be updated)

Contact
For questions, please contact: 2112531015@stu.gdpu.edu.cn
