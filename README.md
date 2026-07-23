# Ancestry Inference Software Benchmarking – Code Repository

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

This repository provides a standardized test framework for evaluating the performance of four mainstream ancestry inference software tools: **amap**, **flare**, **salai‑net**, and **rfmix**. The benchmarking suite assesses computational efficiency (impacted by SNP count, sample size, and multi‑way admixture levels), accuracy across varying admixture generations, and robustness under different scenarios.

---

## Table of Contents

- [Directory Structure](#directory-structure)
- [Dependencies](#dependencies)
  - [System Requirements](#system-requirements)
  - [Python Dependencies](#python-dependencies)
  - [Third‑Party Software](#thirdparty-software)
- [Quick Start](#quick-start)
- [License](#license)
- [Citation](#citation)
- [Contact](#contact)

---

## Directory Structure

```text
.
├── simulate_data_code/          # Scripts for generating simulated genotype data (.txt) and ground‑truth ancestry labels
├── workflows/                    # Automation scripts for executing all benchmarking tests
└── real_data_code/               # Utilities for extracting and processing real‑world data (including VCF format conversion)
Dependencies
System Requirements
Operating system: Linux

Python version: 3.8 or higher

Python Dependencies
Install the required Python libraries using:
pip install matplotlib numpy pandas

Third‑Party Software
The benchmarking scripts rely on the following external tools. Please install them according to their official documentation before running the tests.
Software	Version / Source
amap	1.6
flare	JAR (latest)
salai‑net	Git repository
rfmix	Git repository
ancestryView213	2.13_1.4.0
Note: ancestryView213 is used for visualizing sample ancestry composition.

Quick Start
Follow these steps to set up and run the benchmarking tests.

1. Generate Simulated Data
Run the following script to generate simulated genotype data and corresponding ground‑truth labels:

bash
python3 get_childrenV2.py
2. Run Benchmarking Tests
Place the test scripts for each software in their respective software folders and adjust the parameter paths accordingly.

For example, the test script for evaluating the relationship between computational speed and the number of SNPs is located at:

text
/aMAP_20140601_binary/test_SNP
When testing robustness with simulated data, you can execute the software directly without using the workflow scripts.

3. Visualize Results
Use ancestryView213 to generate plots of sample ancestry composition from the output files.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Citation
If you use this code in your research, please cite:

Author(s). Title of the paper. Journal, Year. (To be updated)

Contact
For questions or feedback, please contact:

Email: 2112531015@stu.gdpu.edu.cn
