# CT-486: Network and Information Security (NIS)
## Complex Computing Activity (CCA) – Classical Cipher Challenge [CLO3]
### Al-Kindi Tri-Tiered Composite Cipher (KTCC) – Blue Team Submission

[![Language](https://img.shields.io/badge/Language-Python%203.14-blue.svg)](https://www.python.org/)
[![Cryptography](https://img.shields.io/badge/Cryptography-Classical%20Product%20Cipher-darkgreen.svg)]()
[![Design](https://img.shields.io/badge/Primitives-Playfair%20%2B%20Vigen%C3%A8re%20%2B%20ADI--PDD-orange.svg)]()
[![University](https://img.shields.io/badge/NED%20University-CS%20%26%20IT%20Department-red.svg)](https://www.neduet.edu.pk/)
[![Batch](https://img.shields.io/badge/Batch-2023-purple.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository contains the complete implementation, automated test suite, empirical benchmarks, and publication-grade reports for the **Complex Computing Activity (CCA)** in **CT-486: Network and Information Security** at the **Department of Computer Science & Information Technology, NED University of Engineering & Technology, Karachi**.

---

## 👥 Project Team & Contributors

*Department of Computer Science & Information Technology, NED University of Engineering & Technology, Karachi*  
**Course:** CT-486: Network and Information Security | **Batch:** 2023 | **Program:** Final Year - Cyber Security  
**Instructor:** Ms. Sayyda Sahar Fatima (Lecturer, Department of CS & IT)  

| S.No | Student Name | Roll Number | GitHub Profile |
| :---: | :--- | :---: | :---: |
| 1 | **Mr. Hamza Saleem** | CR-23009 | [@HamzaSaleem56](https://github.com/HamzaSaleem56) |
| 2 | **Mr. Ameem Akhtar** | CR-23013 | [@ameemakhtr](https://github.com/ameemakhtr) |
| 3 | **Mr. Minhal Rizvi** | CR-23017 | [@Minhal128](https://github.com/Minhal128) |
| 4 | **Mr. Muhammad Usman** | CR-23038 | [@Daedalus46](https://github.com/Daedalus46) |
| 5 | **Mr. Maaz Wasim** | CR-23041 | [@maazw](https://github.com/maazw) |

---

## 🔐 Project Overview & Abstract

In accordance with PEC / Washington Accord CLO3 (Design of Security Mechanisms), this Complex Computing Activity splits groups into Blue and Red Teams. Our group was assigned the **Blue Team** role: design the cipher and the challenge dataset. Breaking it (Deliverables 6–10) is the Red Team group's task.

* **Blue Team (Deliverables 1–5):** Architected the **Al-Kindi Tri-Tiered Composite Cipher (KTCC)** honoring Abu Yusuf Al-Kindi (Father of Cryptanalysis). KTCC combines:
  1. **Tier 1 (Classical Digraphic Substitution):** 5x5 Keyed Playfair Matrix (`LABYRINTH`) to flatten unigram frequencies.
  2. **Tier 2 (Classical Polyalphabetic Substitution):** Periodic Keyed Vigenère Substitution (`VALIANT`) to break geometric digraph symmetries.
  3. **Tier 3 (Team-Designed Technique):** Alternating Digraph Inversion & Positional Dynamic Drift (ADI-PDD, $\delta=3, \theta=7$).
* **Challenge Dataset:** 10 Plaintext-Ciphertext pairs (7 mathematically genuine, 3 poisoned with subtle cryptographic anomalies).

---

> **Disclosure note:** This repository publishes the keys, algorithm and corrupted pairs as Blue Team Deliverable 5 (final explanation after the challenge). The Red Team challenge has concluded. For any new challenge, share only `challenge_dataset_public.json`.

---

## 📊 Summary Comparison: KTCC vs. Classical Primitives

| Metric / Dimension | Caesar Shift | Standard Playfair | Standard Vigenère | KTCC Composite Cipher |
| :--- | :---: | :---: | :---: | :---: |
| **Cipher Class** | Monoalphabetic | Polygraphic (Digram) | Polyalphabetic Stream | **Cascaded Product Cipher** |
| **Time Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathbf{\mathcal{O}(N)}$ |
| **Space Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathbf{\mathcal{O}(N)}$ |
| **Index of Coincidence (IoC)** | $0.0688$ (same as plaintext) | $0.0551$ (Biased) | $0.0441$ (Periodic) | $\mathbf{0.0388}$ (Near random) |
| **Encrypt time (1,000 chars)** | $0.190\text{ ms}$ | $0.323\text{ ms}$ | $0.251\text{ ms}$ | $\mathbf{1.208\text{ ms}}$ |
| **Known-Plaintext Resistance** | Trivial ($1$ char) | Low | Trivial ($L_V$ chars) | **Low** (Tiers 2+3 collapse into one positional keystream; see Suggestions in the report) |

*IoC and timings come from `python cca_benchmark.py` (timings are best of 50 runs on one machine and vary by hardware).*

---

## 📁 Repository Directory Structure

```
NIS_CCA/
├── build_report_pdf.py                  # Academic PDF Report Generator (ReportLab)
├── build_report_docx.py                 # Academic Word Report Generator (python-docx)
├── Complex_Computing_Activity_Report.pdf# Master Publication-Grade PDF Report (Times New Roman)
├── Complex_Computing_Activity_Report.docx# Master Publication-Grade Word Document
├── REPORT.md                            # Comprehensive Markdown Technical Report
├── cca_cipher.py                        # Core Cipher Engine (Playfair + Vigenère + ADI-PDD)
├── cca_challenge.py                     # Challenge Dataset Generator (10 Pairs with 3 Traps)
├── cca_main.py                          # Unified CLI Console (Blue Team, Interactive)
├── cca_benchmark.py                     # Reproduces every IoC and timing number in the reports
├── test_cca.py                          # Automated Unit & Verification Test Suite (6 Tests)
├── challenge_dataset.json               # Exported 10 Challenge Pairs with Ground Truth (Blue Team only)
├── challenge_dataset_public.json        # Handed to the Red Team: pairs only, no keys or ground truth
├── ned_logo_1.png                       # NED University Official Emblem
└── README.md                            # Repository Documentation & Execution Guide
```

---

## 🚀 Execution & Verification Commands

```bash
# 1. Inspect Blue Team Deliverables & Challenge Dataset
python cca_main.py --blue

# 2. Launch Interactive Encryption & Decryption Terminal
python cca_main.py --interactive

# 3. Run Automated Unit Test Suite (6/6 passing)
python test_cca.py

# 4. Reproduce every IoC and timing number in the reports
python cca_benchmark.py

# 5. Re-generate Publication-Grade PDF Report
python build_report_pdf.py

# 6. Re-generate Publication-Grade DOCX Report
python build_report_docx.py
```

---

## 📄 Formal Academic Reports

The formal, publication-grade academic reports are precompiled and available directly in the repository:
* **PDF Report:** [`Complex_Computing_Activity_Report.pdf`](Complex_Computing_Activity_Report.pdf)
* **Word Report:** [`Complex_Computing_Activity_Report.docx`](Complex_Computing_Activity_Report.docx)
* **Typography:** Academic Times New Roman (11 pt), 1-inch margins, Table of Contents, running headers, and dynamic page numbering.
* **Cover Page:** Formal NED University formatting, crest emblem, department metadata, and complete student credentials.

---

## 📜 License
This project is developed for academic evaluation in CT-486 Network and Information Security at NED University of Engineering & Technology. Open-sourced under the [MIT License](LICENSE).
