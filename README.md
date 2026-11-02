# Classical Cipher Challenge (CCA) — CT-486
## Al-Kindi Tri-Tiered Composite Cipher (KTCC)
**Department of Computer Science & Information Technology**  
**NED University of Engineering & Technology, Karachi, Pakistan**  
**Assessment Type:** Complex Computing Activity (CCA) | **Total Marks:** 10 | **Group Size:** 5 Students

---

## 📌 Project Overview

This repository contains the complete implementation, test suite, cryptanalysis tools, and academic audit report for the **CT-486 Classical Cipher Challenge**:
* **Cipher Design (Blue Team):** **Al-Kindi Tri-Tiered Composite Cipher (KTCC)** combining:
  - **Tier 1 (Classical Digraphic):** 5x5 Keyed Playfair Matrix (`LABYRINTH`)
  - **Tier 2 (Classical Polyalphabetic):** Keyed Vigenère Substitution (`VALIANT`)
  - **Tier 3 (Team-Designed Technique):** Alternating Digraph Inversion & Positional Dynamic Drift (ADI-PDD)
* **Challenge Dataset:** 10 Plaintext-Ciphertext pairs (7 mathematically genuine, 3 intentionally corrupted).
* **Cryptanalysis Suite (Red Team):** Automated Index of Coincidence profiling ($\text{IC} = 0.0388$), mathematical differential consistency auditing isolating the 3 corrupted pairs with formal error proofs, key recovery, and 100% round-trip plaintext decryption.

---

## 📂 File Directory

```
NIS_CCA/
│
├── cca_cipher.py           # Core Cipher Engine (Playfair + Vigenère + ADI-PDD)
├── cca_challenge.py        # Challenge Dataset Generator (10 Pairs with 3 Traps)
├── cca_attack.py           # Red Team Cryptanalysis & Automated Decoupling Suite
├── cca_main.py             # Unified CLI Console (Blue Team, Red Team, Interactive)
├── test_cca.py             # Automated Unit & Verification Test Suite (7 Tests)
├── export_cca_pdf.py       # ReportLab PDF Generator Script
├── challenge_dataset.json  # Exported 10 Challenge Pairs with Validation Ground Truth
├── CCA_REPORT.md           # Master Academic Audit Report (Deliverables 1 to 10)
├── CCA_REPORT.pdf          # Publication-Quality Formatted PDF Report
└── README.md               # Quickstart Guide
```

---

## 🚀 Execution Commands

1. **Run Full Blue Team + Red Team Demonstration:**
   ```powershell
   python cca_main.py --all
   ```

2. **Run Red Team Automated Cryptanalysis Solver:**
   ```powershell
   python cca_main.py --red
   ```

3. **Inspect Blue Team Deliverables & Challenge Pairs:**
   ```powershell
   python cca_main.py --blue
   ```

4. **Launch Interactive Encryption & Decryption Terminal:**
   ```powershell
   python cca_main.py --interactive
   ```

5. **Run Automated Unit Test Suite:**
   ```powershell
   python test_cca.py
   ```

6. **Regenerate Submission PDF Report:**
   ```powershell
   python export_cca_pdf.py
   ```
