# CT-486: Network and Information Security (NIS)
## Complex Computing Activity (CCA) – Classical Cipher Challenge [CLO3]
### Al-Kindi Tri-Tiered Composite Cipher (KTCC) & Red Team Cryptanalysis

[![Language](https://img.shields.io/badge/Language-Python%203.14-blue.svg)](https://www.python.org/)
[![Cryptography](https://img.shields.io/badge/Cryptography-Classical%20Product%20Cipher-darkgreen.svg)]()
[![Design](https://img.shields.io/badge/Primitives-Playfair%20%2B%20Vigen%C3%A8re%20%2B%20ADI--PDD-orange.svg)]()
[![University](https://img.shields.io/badge/NED%20University-CS%20%26%20IT%20Department-red.svg)](https://www.neduet.edu.pk/)
[![Batch](https://img.shields.io/badge/Batch-2022--2023-purple.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository contains the complete implementation, cryptanalysis engine, automated test suite, empirical benchmarks, and publication-grade reports for the **Complex Computing Activity (CCA)** in **CT-486: Network and Information Security** at the **Department of Computer Science & Information Technology, NED University of Engineering & Technology, Karachi**.

---

## 👥 Project Team & Contributors

*Department of Computer Science & Information Technology, NED University of Engineering & Technology, Karachi*  
**Course:** CT-486: Network and Information Security | **Batch:** 2022–2023 | **Program:** Final Year - Cyber Security  
**Instructor:** Ms. Sayyda Sahar Fatima (Lecturer, Department of CS & IT)  
**Assessment Type:** Complex Computing Activity (CCA) | **Total Marks:** 10 | **Group Size:** 05 Students  

| S.No | Student Name | Roll Number | GitHub Profile | Assigned Role |
| :---: | :--- | :---: | :---: | :--- |
| 1 | **Mr. Ameem Akhtar** | CR-23013 | [@ameemakhtr](https://github.com/ameemakhtr) | Lead Architect & Cryptanalyst |
| 2 | **Mr. Minhal Rizvi** | CR-23017 | [@Minhal128](https://github.com/Minhal128) | Security Engineer (Blue Team) |
| 3 | **Mr. Muhammad Usman** | CR-23038 | [@Daedalus46](https://github.com/Daedalus46) | Algebraic Analyst (Red Team) |
| 4 | **Mr. Maaz Wasim** | CR-23041 | [@maazw](https://github.com/maazw) | QA & Verification Lead |
| 5 | **Mr. Hamza Saleem** | CR-23009 | [@HamzaSaleem56](https://github.com/HamzaSaleem56) | Implementation & Benchmarking Specialist |

---

## 🔐 Project Overview & Abstract

In accordance with PEC / Washington Accord CLO3 (Design of Security Mechanisms), this Complex Computing Activity required developing and cryptanalyzing a multi-stage classical cipher under a dual-team framework:

* **Blue Team (Deliverables 1–5):** Architected the **Al-Kindi Tri-Tiered Composite Cipher (KTCC)** honoring Abu Yusuf Al-Kindi (Father of Cryptanalysis). KTCC combines:
  1. **Tier 1 (Classical Digraphic Substitution):** 5x5 Keyed Playfair Matrix (`LABYRINTH`) to eliminate unigram frequencies.
  2. **Tier 2 (Classical Polyalphabetic Substitution):** Periodic Keyed Vigenère Substitution (`VALIANT`) to break geometric digraph symmetries.
  3. **Tier 3 (Team-Designed Technique):** Alternating Digraph Inversion & Positional Dynamic Drift (ADI-PDD, $\delta=3, \theta=7$).
* **Challenge Dataset:** 10 Plaintext-Ciphertext pairs (7 mathematically genuine, 3 poisoned with subtle cryptographic anomalies).
* **Red Team (Deliverables 6–10):** Reverse-engineered the cipher using statistical profiling ($\text{IoC} = 0.0388$), isolated the 3 corrupted pairs with formal mathematical proofs, recovered all secret keys (`LABYRINTH`, `VALIANT`, $\delta=3, \theta=7$), and achieved 100% round-trip plaintext decryption on all genuine pairs.

---

## 📊 Summary Comparison: KTCC vs. Classical Primitives

| Metric / Dimension | Caesar Shift | Standard Playfair | Standard Vigenère | KTCC Composite Cipher |
| :--- | :---: | :---: | :---: | :---: |
| **Cipher Class** | Monoalphabetic | Polygraphic (Digram) | Polyalphabetic Stream | **Cascaded Product Cipher** |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathbf{\mathcal{O}(N)}$ |
| **Space Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathbf{\mathcal{O}(N)}$ |
| **Index of Coincidence (IoC)** | $0.0655$ (Vulnerable) | $0.0482$ (Biased) | $0.0430$ (Periodic) | $\mathbf{0.0388}$ (Near-ideal entropy) |
| **Throughput (1,000 chars)** | $\sim 4.0\text{M chars/s}$ | $\sim 1.2\text{M chars/s}$ | $\sim 2.5\text{M chars/s}$ | $\mathbf{552,417\text{ chars/s}}$ |
| **Known-Plaintext Resistance** | Trivial ($1$ char) | Low ($5\text{ pairs}$) | Moderate ($L_V\text{ chars}$) | **High (Cascaded multi-tier)** |

---

## 📁 Repository Directory Structure

```
NIS_CCA/
├── build_report_pdf.py                  # Academic PDF Report Generator (ReportLab)
├── build_report_docx.py                 # Academic Word Report Generator (python-docx)
├── export_cca_pdf.py                    # Wrapper for PDF Generation
├── Complex_Computing_Activity_Report.pdf# Master Publication-Grade PDF Report (Times New Roman, TOC)
├── Complex_Computing_Activity_Report.docx# Master Publication-Grade Word Document
├── CCA_REPORT.pdf                       # Synchronized PDF Report
├── CCA_REPORT.docx                      # Synchronized Word Report
├── CCA_REPORT.md                        # Master Markdown Technical Report
├── REPORT.md                            # Synchronized Technical Report (NIS_CCP style)
├── cca_cipher.py                        # Core Cipher Engine (Playfair + Vigenère + ADI-PDD)
├── cca_challenge.py                     # Challenge Dataset Generator (10 Pairs with 3 Traps)
├── cca_attack.py                        # Red Team Cryptanalysis & Automated Decoupling Suite
├── cca_main.py                          # Unified CLI Console (Blue Team, Red Team, Interactive)
├── test_cca.py                          # Automated Unit & Verification Test Suite (7 Tests)
├── challenge_dataset.json               # Exported 10 Challenge Pairs with Ground Truth
├── ned_logo_1.png                       # NED University Official Emblem
├── NIS_CCA_Review_Package.zip           # Complete Offline Submission Review Archive
└── README.md                            # Repository Documentation & Execution Guide
```

---

## 🚀 Execution & Verification Commands

```bash
# 1. Run Complete Blue Team + Red Team Demonstration
python cca_main.py --all

# 2. Run Red Team Automated Cryptanalysis Solver
python cca_main.py --red

# 3. Inspect Blue Team Deliverables & Challenge Dataset
python cca_main.py --blue

# 4. Launch Interactive Encryption & Decryption Terminal
python cca_main.py --interactive

# 5. Run Automated Unit Test Suite (7/7 passing)
python test_cca.py

# 6. Re-generate Publication-Grade PDF Report
python build_report_pdf.py

# 7. Re-generate Publication-Grade DOCX Report
python build_report_docx.py
```

---

## 📄 Formal Academic Reports

The formal, publication-grade academic reports are precompiled and available directly in the repository:
* **PDF Report:** [`Complex_Computing_Activity_Report.pdf`](Complex_Computing_Activity_Report.pdf) / [`CCA_REPORT.pdf`](CCA_REPORT.pdf)
* **Word Report:** [`Complex_Computing_Activity_Report.docx`](Complex_Computing_Activity_Report.docx) / [`CCA_REPORT.docx`](CCA_REPORT.docx)
* **Typography:** Academic Times New Roman (11 pt), 1-inch margins, Table of Contents, running headers, and dynamic page numbering.
* **Cover Page:** Formal NED University formatting, crest emblem, department metadata, and complete student credentials.

---

## 📜 License
This project is developed for academic evaluation in CT-486 Network and Information Security at NED University of Engineering & Technology. Open-sourced under the [MIT License](LICENSE).
