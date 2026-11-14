# Network and Information Security (CT-486)
## Complex Computing Activity [CLO3]
### Classical Cipher Challenge: Cipher Design and Cryptanalysis
#### Al-Kindi Tri-Tiered Composite Cipher (KTCC)

**Course Code:** CT-486  
**Course Title:** Network and Information Security  
**Department:** Department of Computer Science & Information Technology  
**Institution:** NED University of Engineering & Technology, Karachi, Pakistan  
**Class & Batch:** Final Year - Cyber Security | Batch: 2023  
**Instructor:** Ms. Sayyda Sahar Fatima (Lecturer, Department of CS & IT)  
**Total Marks:** 10  
**Group Size:** 05 Members  
**Submission Deadline:** 8th November 2026  

---

## Student Team Details

| Seat Number | Student Name | GitHub Profile |
| :---: | :--- | :---: |
| **CR-23009** | **Mr. Hamza Saleem** | [@HamzaSaleem56](https://github.com/HamzaSaleem56) |
| **CR-23013** | **Mr. Ameem Akhtar** | [@ameemakhtr](https://github.com/ameemakhtr) |
| **CR-23017** | **Mr. Minhal Rizvi** | [@Minhal128](https://github.com/Minhal128) |
| **CR-23038** | **Mr. Muhammad Usman** | [@Daedalus46](https://github.com/Daedalus46) |
| **CR-23041** | **Mr. Maaz Wasim** | [@maazw](https://github.com/maazw) |

---

## Executive Summary & Architecture Overview

This technical report documents the end-to-end design, implementation, cryptanalysis, and empirical verification for the **CT-486 Classical Cipher Challenge**. The submission provides a complete, dual-perspective engineering record:
* **Blue Team (Deliverables 1–5):** Design of the **Al-Kindi Tri-Tiered Composite Cipher (KTCC)**, combining 5x5 Playfair digraphic substitution, polyalphabetic Vigenère substitution, and team-designed Alternating Digraph Inversion & Positional Dynamic Drift (ADI-PDD), alongside 10 challenge pairs (7 genuine, 3 corrupted).
* **Red Team (Deliverables 6–10):** Systematic cryptanalytic reverse-engineering isolating the 3 corrupted pairs with formal mathematical proofs, recovering secret keys (`LABYRINTH`, `VALIANT`, $\delta=3, \theta=7$), and proving 100% round-trip plaintext decryption.

```mermaid
flowchart LR
    subgraph BlueTeam["Blue Team: Al-Kindi Tri-Tiered Architecture"]
        P["Plaintext (P)"] --> DP["Digraph Prep (J->I, X-split, Z-pad)"]
        DP --> S1["Tier 1: Playfair 5x5 (Key: LABYRINTH)"]
        S1 --> S2["Tier 2: Vigenère (Key: VALIANT)"]
        S2 --> S3["Tier 3: Team ADI-PDD (Delta=3, Theta=7)"]
        S3 --> CT["Challenge Dataset: 10 Pairs (7 Genuine, 3 Poisoned)"]
    end

    subgraph RedTeam["Red Team: Reverse-Engineering & Cryptanalysis"]
        CT --> SP["Statistical Profiling (IC ~0.0388, Even L)"]
        SP --> AD["Simulated Annealing: Cross-Pair Keystream Consistency"]
        AD --> BAD["Identify & Prove 3 Poisoned Pairs (Pairs 3, 6, 9)"]
        AD --> GEN["Isolate 7 Genuine Pairs"]
        GEN --> DEC["Multi-Tier Decoupling & Key Recovery"]
        DEC --> REC["Recovered Keys: LABYRINTH, VALIANT, (3, 7)"]
        REC --> VER["100% Round-Trip Plaintext Verification"]
    end

    style BlueTeam fill:#eef2ff,stroke:#4338ca,stroke-width:2px;
    style RedTeam fill:#fef2f2,stroke:#b91c1c,stroke-width:2px;
```

---

# PART I: BLUE TEAM DELIVERABLES (DELIVERABLES 1 – 5)

## Deliverable 1: Unique Cipher Name and Comprehensive Description

* **Official Cipher Name:** **Al-Kindi Tri-Tiered Composite Cipher (KTCC)**
* **Technical Classification:** Three-Tiered Composite Product Cipher with Positional Dynamic Affine Diffusion.

### Detailed Architectural Description
* **Historical Foundation:** Named in honor of **Abu Yusuf Ya'qub ibn Ishaq al-Kindi (801–873 CE)**, universally recognized as the Father of Cryptanalysis. Al-Kindi authored *Risalah fi Istikhraj al-Mu'amma* (*Manuscript on Deciphering Cryptographic Messages*) at Baghdad's House of Wisdom, inventing frequency analysis.
* **Shannon's Product Cipher Criterion:** Cascades three distinct operators following Claude Shannon's product-cipher idea of combining confusion and diffusion.
* **Three Cascaded Layers:**
  1. *Tier 1 (Classical Digraphic Substitution):* 5x5 Keyed Playfair Matrix to flatten single-character frequencies (IoC 0.0688 → 0.0551 on the challenge plaintexts).
  2. *Tier 2 (Classical Polyalphabetic Substitution):* Periodic Keyed Vigenère Substitution to mask geometric digram symmetries.
  3. *Tier 3 (Team-Designed Dynamic Technique):* Alternating Digraph Inversion & Positional Dynamic Drift (ADI-PDD) providing a fixed in-block transposition and a position-dependent affine shift.

---

## Deliverable 2: Complete Encryption Technique and Sequence

The encryption pipeline executes sequentially through three ordered tiers:

```
Plaintext (P)
     │
     ▼
[Step 0: Preprocessing & Digraph Conditioning]
  - Filter non-alphabetical characters; capitalize A-Z
  - Map 'J' -> 'I'
  - Insert 'X' between identical letters in a digraph (e.g., "EE" -> "EX", "EX")
  - Append 'Z' if total length is odd
     │
     ▼
[Tier 1: Playfair 5x5 Digraphic Transformation]
  - Pairs mapped across 5x5 key matrix (Secret: "LABYRINTH")
  - Same row: shift right mod 5
  - Same col: shift down mod 5
  - Rectangle: swap column indices
     │
     ▼
[Tier 2: Periodic Keyed Vigenère Substitution]
  - Periodic polyalphabetic addition with secret key "VALIANT" (Length 7):
    S2[i] = (S1[i] + KV[i mod 7]) mod 26
     │
     ▼
[Tier 3: Alternating Digraph Inversion & Positional Dynamic Drift (ADI-PDD)]
  - Part A (ADI): Invert character order for even-indexed digraph blocks:
    If (block_index mod 2 == 0): Swap(c[2b], c[2b+1])
  - Part B (PDD): Apply positional affine modular translation:
    Delta(i) = (3 * i + 7) mod 26
    C[i] = (S2_permuted[i] + Delta(i)) mod 26
     │
     ▼
Ciphertext (C)
```

### Encryption Algorithm Pseudocode

```text
Algorithm 1: KTCC Encryption
Input : Plaintext P, Playfair Key K_P, Vigenère Key K_V, Drift Parameters (delta, theta)
Output: Ciphertext C

1. P_clean <- Clean text, map 'J' -> 'I'
2. Digraphs <- Split into pairs (c1, c2); split doubles with 'X'; pad odd with 'Z'
3. S1 <- Playfair_Encrypt(Digraphs, K_P)
4. S2 <- Array of length Length(S1)
5. For i <- 0 to Length(S1) - 1 Do
6.     shift <- Ord(K_V[i mod Length(K_V)]) - 65
7.     S2[i] <- (Ord(S1[i]) - 65 + shift) mod 26
8. End For
9. For b <- 0 to (Length(S2) / 2) - 1 Do
10.    If b mod 2 == 0 Then
11.        Swap(S2[2*b], S2[2*b + 1])
12.    End If
13. End For
14. Initialize Ciphertext array C of length Length(S2)
15. For i <- 0 to Length(S2) - 1 Do
16.    delta_i <- (delta * i + theta) mod 26
17.    C[i] <- Chr(((S2[i] + delta_i) mod 26) + 65)
18. End For
19. Return string representation of C
```

### Decryption Algorithm Pseudocode

```text
Algorithm 2: KTCC Decryption
Input : Ciphertext C, Playfair Key K_P, Vigenère Key K_V, Drift Parameters (delta, theta)
Output: Original Plaintext P

1. Assert Length(C) mod 2 == 0
2. S2_prime <- Array of length Length(C)
3. For i <- 0 to Length(C) - 1 Do
4.     delta_i <- (delta * i + theta) mod 26
5.     S2_prime[i] <- (Ord(C[i]) - 65 - delta_i + 26) mod 26
6. End For
7. For b <- 0 to (Length(S2_prime) / 2) - 1 Do
8.     If b mod 2 == 0 Then
9.         Swap(S2_prime[2*b], S2_prime[2*b + 1])
10.    End If
11. End For
12. S1_recovered <- Array of length Length(S2_prime)
13. For i <- 0 to Length(S2_prime) - 1 Do
14.     shift <- Ord(K_V[i mod Length(K_V)]) - 65
15.     S1_recovered[i] <- Chr(((S2_prime[i] - shift + 26) mod 26) + 65)
16. End For
17. P_recovered <- Playfair_Decrypt(S1_recovered, K_P)
18. Return P_recovered
```

---

## Deliverable 3: Keys, Alphabet Mapping, and Special Rules

### 1. Tier 1 (Playfair) Key & 5x5 Alphabet Matrix
* **Key Keyword:** `LABYRINTH` (Length 9)
* **Alphabet Size:** 25 letters ('I' and 'J' share a single cell).
* **5x5 Matrix Layout:**

| Row / Col | Col 0 | Col 1 | Col 2 | Col 3 | Col 4 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Row 0** | **L** | **A** | **B** | **Y** | **R** |
| **Row 1** | **I/J** | **N** | **T** | **H** | **C** |
| **Row 2** | **D** | **E** | **F** | **G** | **K** |
| **Row 3** | **M** | **O** | **P** | **Q** | **S** |
| **Row 4** | **U** | **V** | **W** | **X** | **Z** |

### 2. Tier 2 (Vigenère) Keystream
* **Secret Key Keyword:** `VALIANT` (Length $L_V = 7$)
* **Numeric Shift Offsets:** $K_V = [21, 0, 11, 8, 0, 13, 19]$

### 3. Tier 3 (ADI-PDD) Transformation Parameters
* **Alternating Inversion Rule (ADI):** Inverts character positions within even digraph blocks ($b \equiv 0 \pmod{2}$).
* **Dynamic Drift Parameters (PDD):** Multiplier $\delta = 3$, seed offset $\theta = 7$.
  $$\Delta(i) = (3 \cdot i + 7) \pmod{26}$$

---

## Deliverable 4: Ten Plaintext-Ciphertext Challenge Pairs

| Pair # | Plaintext (Input) | Ciphertext (Output) | Len | True Status | Flaw Type (Red Team Target) |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **1** | `DEFEND THE PERIMETER AT ONCE` | `MJEDKEZZENDOEKXNLBKMOGIT` | 24 | **GENUINE** | Valid multi-tier encryption |
| **2** | `ZERO TRUST ARCHITECTURE SECURES DATA` | `RAYQHYRJRVVYXJFFSZIKYVFWMLERYPRF` | 32 | **GENUINE** | Valid multi-tier encryption |
| **3** | `CRYPTOGRAPHIC PROTOCOL FAILURE DETECTED` | `JPZOVNCVEJVBCASSAEWRNMGWMUUNSPRJTKDH` | 36 | <font color="#B91C1C">**POISONED**</font> | Tampered substitution at index 5 |
| **4** | `INCIDENT RESPONSE TEAM ENGAGED IMMEDIATELY` | `ASGLLALEAIFEOCGKQEUNOZZHGWGGHBSHPOZQWRQR` | 40 | **GENUINE** | Valid multi-tier encryption |
| **5** | `QUANTUM COMPUTING THREATENS TRADITIONAL RSA` | `ERLCCEKFEXFKXOZENYJJXMJNDBFEQXLRQXZDVQQP` | 40 | **GENUINE** | Valid multi-tier encryption |
| **6** | `MALWARE EXFILTRATING SENSITIVE AUDIT LOGS` | `STSZRXYSLOWHSIDBYYQDUZXXIZHXAZPQTPYPMY` | 38 | <font color="#B91C1C">**POISONED**</font> | Parity inversion swapped on odd block |
| **7** | `FIREWALL BLOCKS UNTRUSTED NETWORK TRAFFIC` | `AIYIHRQROITACREZSKUYMAANPQZENDJGNNEZPRJL` | 40 | **GENUINE** | Valid multi-tier encryption |
| **8** | `AUTHENTICATION TOKEN EXPIRES SOON REFRESH` | `CQFAKKZKHVABOCFPQUNNAHXUPWGSRGEONMIRTQ` | 38 | **GENUINE** | Valid multi-tier encryption |
| **9** | `DENIAL OF SERVICE ATTACK FLOODS ROUTER` | `MJRLGXHBAWTNSUGNHYWACVYKWCGHPKQZCALF` | 36 | <font color="#B91C1C">**POISONED**</font> | Suffix desynchronization (+11 shift) |
| **10** | `ELLIPTIC CURVE DIGITAL SIGNATURE STANDARD` | `HIGBLSFFPQTNOMZDSEKZMXZQONTOBVRFQKZOQY` | 38 | **GENUINE** | Valid multi-tier encryption |

---

## Deliverable 5: Final Post-Challenge Architecture Explanation

Step-by-step cryptographic trace for **Pair #1** (`DEFEND THE PERIMETER AT ONCE`):

| Processing Stage | Data State | Cryptographic Significance |
| :--- | :--- | :--- |
| **Raw Input** | `DEFEND THE PERIMETER AT ONCE` | Original plaintext. |
| **Digraph Preparation** | `DE FE ND TH EP ER IM ET ER AT ON CE` | Filtered, uppercase, paired into 12 digraphs. |
| **Tier 1: Playfair** | `EF GF IE HC FO KA DU FN KA BN VE NK` | Digraphic substitution masks unigram frequencies. |
| **Tier 2: Vigenère** | `ZF RN IR AX FZ SA QN AN VI BA OZ NV` | Polyalphabetic keystream breaks geometric symmetries. |
| **Tier 3A: ADI Inversion** | `FZ RN RI AX ZF SA NQ AN IV BA ZO NV` | Parity inversion on even digraph blocks (0, 2, 4...). |
| **Tier 3B: Dynamic Drift** | `MJ ED KE ZZ EN DO EK XN LB KM OG IT` | Positional affine drift $\Delta(i) = (3i + 7) \pmod{26}$. |
| **Final Ciphertext** | `MJEDKEZZENDOEKXNLBKMOGIT` | Transmitted challenge ciphertext (Length 24). |

---

# PART II: RED TEAM DELIVERABLES (DELIVERABLES 6 – 10)

## Deliverable 6: Statistical Profiling and Technique Identification

All findings in Deliverables 6–10 are computed by `cca_attack.py` from the public pairs (`challenge_dataset_public.json`) only. The attack is never given any key; `test_cca.py` re-runs it against a cipher with unseen keys (`MONARCHY`, `SECRET`, δ=5, θ=11) to prove this.

### 1. Structural Invariant: Digraphic Even Length
Every ciphertext has even length ($N \equiv 0 \pmod{2}$), and its length equals the Playfair-prepared plaintext length (J→I, X filler, Z pad) in **10/10** pairs, versus the raw plaintext length in only **3/10**. This points to a Playfair-family digraphic layer.

### 2. Index of Coincidence (IoC) Profiling

$$IC = \frac{\sum_{i=A}^Z f_i (f_i - 1)}{N (N - 1)}$$

Values reproduced by `cca_benchmark.py` over the 10 challenge plaintexts (350 letters):

| Cipher Scheme | Measured IoC | Cryptanalytic Deductions |
| :--- | :---: | :--- |
| **Challenge Plaintexts (English)** | $0.0688$ | Highly uneven; heavy bias toward 'E', 'T', 'A'. |
| **Caesar (k=3)** | $0.0688$ | Identical to plaintext: a shift only relabels letters. |
| **Playfair only (`LABYRINTH`)** | $0.0551$ | Partially flattened; digraphic bias remains. |
| **Vigenère only (`VALIANT`)** | $0.0441$ | Flattened further by the polyalphabetic shift. |
| **Uniform Random Baseline** | $0.0385$ | $1/26$. |
| **KTCC Challenge Ciphertext** | **0.0388** | Near random; indicates a polyalphabetic layer. |

### 3. Shared Positional Keystream (the decisive weakness)
Tiers 2 and 3 only add shifts that depend on the character position, plus a fixed swap. Together they act as **one fixed position-dependent keystream**. So under the correct Playfair matrix, every genuine pair implies the *same* shift at each position. Simulated annealing over Playfair matrices, scored by how many pairs agree, converged to a matrix where **355 of 362** positions agree. The 7 disagreeing positions are exactly the tampered characters.

---

## Deliverable 7: Rigorous Identification and Mathematical Proofs of Corrupted Pairs

A pair is flagged when its implied keystream disagrees with the consensus of the other pairs. This isolated **Pairs 3, 6, and 9**:

| Pair # | Anomaly Category | Exact Location | Observed vs. Expected | Evidence (generated by `cca_attack.py`) |
| :---: | :--- | :--- | :--- | :--- |
| **3** | Substitution Tampering | Index 5 (Block 2, Char 1) | Observed: `'N'`<br/>Expected: `'J'`<br/>Delta: $+4 \pmod{26}$ | Only index 5 disagrees with the keystream shared by every other pair. All other positions agree. |
| **6** | Transposition Error | Indices 2 & 3 (Block 1, Odd) | Observed: `'SZ'`<br/>Expected: `'ZS'`<br/>Delta: Reversed | Only indices 2–3 disagree, and the observed pair is exactly the prediction reversed. Block 1 is odd, and the cipher only swaps even blocks. |
| **9** | Tail Desynchronization | Indices 32–35 (Terminal 4 chars) | Observed: `'CALF'`<br/>Expected: `'RPAU'`<br/>Delta: $+11 \pmod{26}$ | Positions 0–31 agree. The last four all differ by the same $+11 \pmod{26}$, so the tail was shifted after encryption. |

---

## Deliverable 8: Key Recovery and Pipeline Decoupling

| Layer | Parameter | Recovered Value | Method of Discovery |
| :--- | :--- | :--- | :--- |
| **Tier 1** | Playfair Keyword | `LABYRINTH` | Simulated annealing over 5x5 matrices scored by cross-pair keystream agreement (355/362). The keyword is the one of the 25 equivalent row/column rotations whose tail is the unused alphabet in order. |
| **Tier 1** | Alphabet Grid | 25 letters (I/J merged) | CT length = J→I / X / Z prepared PT length in 10/10 pairs |
| **Tier 2** | Vigenère Keyword | `VALIANT` (Length 7) | After removing the drift, the keystream is exactly periodic with period 7 (the only fit at the smallest period) |
| **Tier 3A** | Transposition Rule | Swap on even blocks ($b \pmod 2 == 0$) | Per block, the swapped orientation gives consensus only on even blocks |
| **Tier 3B** | Multiplier ($\delta$) | `3` | Exhaustive $\delta = 0..25$: only $\delta = 3$ leaves a period-7 residual |
| **Tier 3B** | Offset ($\theta$) | `7` | The data fixes only $V[i] + \theta$. All 26 splits encrypt identically, and $\theta = 7$ is the one that makes the key an English word. |

**Layer order** was also derived, not assumed. Of the four possible orders of Vigenère, swap and drift, only *Vigenère → swap → drift* fits the keystream exactly.

---

## Deliverable 9: Inverted Decryption Pipeline Reconstruction

```
Received Ciphertext (C)
     │
     ▼
[Step 1: Reverse Positional Dynamic Drift]
  S2'[i] = (C[i] - (3*i + 7) + 26) mod 26
     │
     ▼
[Step 2: Reverse Alternating Digraph Inversion]
  If (b mod 2 == 0): Swap(S2'[2b], S2'[2b+1])
     │
     ▼
[Step 3: Reverse Vigenère Subtraction]
  S1[i] = (S2'[i] - (Ord(VALIANT[i mod 7]) - 65) + 26) mod 26
     │
     ▼
[Step 4: Reverse Playfair Matrix Decryption]
  Apply inverse row (-1), col (-1), and rectangle rules using matrix "LABYRINTH"
     │
     ▼
Original Plaintext (P)
```

**Invertibility:** The drift, swap and Vigenère stages are bijections on $\mathbb{Z}_{26}^{N}$, and Playfair is a bijection on prepared digraphs. Therefore:
$$D(C) = E_1^{-1}(E_2^{-1}(E_3^{-1}(E_3(E_2(E_1(P')))))) = P'$$
Here $P'$ is the *prepared* plaintext. The preparation step (dropping spaces, J→I, X filler, Z pad) is lossy, so decryption returns $P'$, not the raw $P$.

---

## Deliverable 10: Verification Evidence and Round-Trip Plaintext Inversion

| Pair # | Challenge Ciphertext | Plaintext (decrypts to its prepared form) | Match Status | Verification Fidelity |
| :---: | :--- | :--- | :---: | :---: |
| **1** | `MJEDKEZZENDOEKXNLBKMOGIT` | `DEFEND THE PERIMETER AT ONCE` | **VERIFIED VALID** | **100.0% Exact Match** |
| **2** | `RAYQHYRJRVVYXJFFSZIKYVFWMLERYPRF` | `ZERO TRUST ARCHITECTURE SECURES DATA` | **VERIFIED VALID** | **100.0% Exact Match** |
| **3** | `JPZOVNCVEJVBCASSAEWRNMGWMUUNSPRJTKDH` | *[Rejected: Tampered at index 5]* | **FLAGGED CORRUPT** | **Rejected (does not round-trip)** |
| **4** | `ASGLLALEAIFEOCGKQEUNOZZHGWGGHBSHPOZQWRQR` | `INCIDENT RESPONSE TEAM ENGAGED IMMEDIATELY` | **VERIFIED VALID** | **100.0% Exact Match** |
| **5** | `ERLCCEKFEXFKXOZENYJJXMJNDBFEQXLRQXZDVQQP` | `QUANTUM COMPUTING THREATENS TRADITIONAL RSA` | **VERIFIED VALID** | **100.0% Exact Match** |
| **6** | `STSZRXYSLOWHSIDBYYQDUZXXIZHXAZPQTPYPMY` | *[Rejected: letters transposed at idx 2-3]* | **FLAGGED CORRUPT** | **Rejected (does not round-trip)** |
| **7** | `AIYIHRQROITACREZSKUYMAANPQZENDJGNNEZPRJL` | `FIREWALL BLOCKS UNTRUSTED NETWORK TRAFFIC` | **VERIFIED VALID** | **100.0% Exact Match** |
| **8** | `CQFAKKZKHVABOCFPQUNNAHXUPWGSRGEONMIRTQ` | `AUTHENTICATION TOKEN EXPIRES SOON REFRESH` | **VERIFIED VALID** | **100.0% Exact Match** |
| **9** | `MJRLGXHBAWTNSUGNHYWACVYKWCGHPKQZCALF` | *[Rejected: +11 offset at idx 32-35]* | **FLAGGED CORRUPT** | **Rejected (does not round-trip)** |
| **10** | `HIGBLSFFPQTNOMZDSEKZMXZQONTOBVRFQKZOQY` | `ELLIPTIC CURVE DIGITAL SIGNATURE STANDARD` | **VERIFIED VALID** | **100.0% Exact Match** |

* **Verification Summary:** The cipher was rebuilt from the *recovered* keys only. All 7 genuine pairs re-encrypt to the exact challenge ciphertext and decrypt to their prepared plaintext. All 3 corrupted pairs fail. Automated test suite (`test_cca.py`): **8/8 Tests Passed**.

---

## 5. Performance Benchmarks and Complexity Analysis

Measured with `cca_benchmark.py` (best of 50 runs on one development machine, Python 3.14). Absolute times vary by hardware, but the linear scaling does not.

| Payload Size ($N$) | KTCC Encrypt (ms) | KTCC Decrypt (ms) | Caesar Shift (ms) | Overhead Factor | Throughput (chars/s) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **100 chars** | 0.124 ms | 0.099 ms | 0.021 ms | $5.9\times$ | 824,576 chars/s |
| **1,000 chars** | 1.208 ms | 0.962 ms | 0.190 ms | $6.4\times$ | 844,091 chars/s |
| **10,000 chars** | 11.805 ms | 9.273 ms | 1.770 ms | $6.7\times$ | 865,425 chars/s |

* **Complexity:** Time complexity is strictly linear $\mathcal{O}(N)$. Memory complexity is $\mathcal{O}(N)$ for buffer allocations with $\mathcal{O}(1)$ constant storage for the 5x5 matrix. Measured throughput was above 800,000 characters/second on the test machine.

---

## 6. Suggestions for Improving the Cipher's Security

1. **Autokey Keystream Dynamic Scheduling:** Replace periodic Vigenère repetitions with an autokey mechanism ($K[i] = P[i - L_V]$) to eliminate keystream periodicity.
2. **Non-Linear S-Box Insertion:** Introduce non-linear substitution (AES/DES S-box style) between Tier 2 and Tier 3 to break linear modular solvability over $\mathbb{Z}_{26}$.
3. **Cipher Block Chaining (CBC) Feedback:** Modularly add previous ciphertext digraphs into current plaintext digraphs ($P'[b] = (P[b] + C[b-1]) \pmod{26}$) to prevent repeated block patterns.
4. **Expanded 6x6 Matrix:** Incorporate numbers 0–9 and eliminate the I/J merger, enabling native encryption of IP addresses and cryptographic hashes.

---

## 7. Code Submission & Execution Details

All project source files, automated test suites, and cryptanalysis solvers are publicly hosted on GitHub at:  
**Repository Link:** [https://github.com/ameemakhtr/NIS_CCA](https://github.com/ameemakhtr/NIS_CCA)

### Automated Execution Commands:
```bash
# 1. Run Complete Blue Team + Red Team Demonstration:
python cca_main.py --all

# 2. Run Red Team Automated Cryptanalysis Solver:
python cca_main.py --red

# 3. Inspect Blue Team Deliverables & Dataset:
python cca_main.py --blue

# 4. Run Automated Test Suite (8/8 Tests Passing):
python test_cca.py

# 5. Interactive Encryption/Decryption Terminal:
python cca_main.py --interactive

# 6. Reproduce every IoC and timing number in this report:
python cca_benchmark.py

# 6. Recompile Publication-Grade PDF and Word Reports:
python build_report_pdf.py
python build_report_docx.py
```

---

## 8. Academic References

1. Al-Kindi, Abu Yusuf Ya'qub ibn Ishaq (c. 850 CE). *Risalah fi Istikhraj al-Mu'amma* (*Manuscript on Deciphering Cryptographic Messages*). House of Wisdom, Baghdad.
2. Shannon, Claude E. (1949). "Communication Theory of Secrecy Systems." *Bell System Technical Journal*, 28(4), 656–715.
3. Friedman, William F. (1922). *The Index of Coincidence and Its Applications in Cryptography*. Department of Ciphers, Publication No. 22, Riverbank Laboratories.
4. Stallings, William (2020). *Cryptography and Network Security: Principles and Practice* (8th Edition). Pearson Education.
5. Wheatstone, Charles & Playfair, Lyon (1854). "On the Playfair System of Cipher." *Minutes of the Royal Society of Arts*, London.
6. Vigenère, Blaise de (1586). *Traicté des Chiffres ou Secrètes Manières d'Escrire*. Paris, France.
