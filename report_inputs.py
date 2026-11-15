"""
Single source for report Sections 4 and 5. build_report_pdf.py and build_report_docx.py render from here,
and sync_markdown() writes the same content into REPORT.md, so the three outputs cannot drift apart.
Numbers (keyspace, flaw signatures, test count) are computed from code, never typed in.

Run: python report_inputs.py   (refreshes REPORT.md)
"""

import os
import unittest
from cca_analysis import keyspace_rows, compute_flaw_rows, affine_hits

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_COUNT = unittest.defaultTestLoader.loadTestsFromName("test_cca").countTestCases()
AFFINE_TRIALS = 200
_AFFINE_HITS = affine_hits(AFFINE_TRIALS)
_KEYSPACE = keyspace_rows()

# ---------------- Section 4 ----------------
S5_TITLE = "4. Design Rationale and Resistance Analysis"

S5_INTRO = ("This section is the post-challenge explanation of the cipher. Every number below is "
            "computed by cca_analysis.py with the real keys.")

STAGE_ROWS = [
    ("Stage", "What it does", "Why it is there", "Known limit"),
    ("Preparation", "Uppercase A–Z; J→I; split doubled letters with X (Q for XX); pad odd length with Z (X after Z).",
     "Gives Playfair valid digraphs.",
     "Lossy: spaces, J and filler letters are not recovered. Ciphertext length equals prepared length."),
    ("Tier 1: Playfair (LABYRINTH)", "Replaces each digraph using the 5x5 keyed matrix.",
     "Hides single-letter frequencies (IoC 0.0688 → 0.0551).",
     "No letter encrypts to itself; AB→XY implies BA→YX. Only 25 letters."),
    ("Tier 2: Vigenère (VALIANT)", "Adds a period-7 shift to each letter.",
     "Breaks Playfair's fixed digraph mapping and flattens frequencies further.",
     "Linear and key-only: it merges with Tier 3 into one fixed per-position shift."),
    ("Tier 3A: ADI swap", "Swaps the two letters of every even-numbered digraph block.",
     "Each output position carries its neighbour's Vigenère shift, which breaks the plain period-7 pattern.",
     "Fixed and key-independent: it adds no secret."),
    ("Tier 3B: PDD drift", "Adds (3i + 7) mod 26 at position i.",
     "Stretches the period of the total shift from 7 to 364 letters, longer than any challenge message.",
     "Linear in i and independent of the plaintext, so the combined shift is still a fixed keystream."),
]

KEYSPACE_ROWS = [("Component", "Formula", "Size", "Bits")] + _KEYSPACE

S5_AFFINE = (f"Affine finding: Tiers 2 and 3 together compute C[i] = X[perm(i)] + k[i] (mod 26), where X is the "
             f"Playfair output, perm is the even-block swap and k[i] = V[perm(i) mod 7] + δ·i + θ depends only on the "
             f"position. cca_analysis.py confirmed this on {_AFFINE_HITS}/{AFFINE_TRIALS} random string pairs under two "
             f"unrelated key sets: ciphertext differences equal Playfair-output differences, so the Tier 2/3 key cancels. "
             f"The Tier 2/3 secret is therefore only 9 numbers (7 Vigenère shifts, δ, θ). Once the Playfair output for "
             f"one known plaintext is known, they follow directly by subtraction, so nearly all of the difficulty lies in "
             f"the Playfair matrix ({_KEYSPACE[0][3]}). Known equivalent keys (25 cyclic shifts of the matrix; θ "
             f"absorbed by the Vigenère key) reduce the nominal {_KEYSPACE[3][3]} to at most {_KEYSPACE[4][3]} "
             f"distinct ciphers.")

FLAW_ROWS = [("Pair", "Status", "Flaw injected", "Damaged blocks", "Wrong letters")] + [
    (str(r["pair_id"]), r["status"], r["flaw"], ", ".join(map(str, r["damaged_blocks"])) or "–",
     f"{r['wrong_letters']} / {r['length']}")
    for r in compute_flaw_rows()
]

S5_FLAWS = ("Flaw signatures: each ciphertext was decrypted with the real keys and compared with its prepared "
            "plaintext. All ten ciphertexts keep the length of their prepared plaintext, so length alone does not "
            "reveal the incorrect pairs. Each flaw stays local: it damages at most two digraph blocks.")

S5_ASSESSMENT = ("Honest assessment: KTCC is a classroom challenge cipher, not a secure one. Its ciphertext IoC (0.0388) "
                 "is close to random text (0.0385), so single-letter frequency analysis gives little, but it is weak "
                 "against known-plaintext analysis: Tiers 2 and 3 reduce to a fixed keystream and the remaining work is "
                 "a search over Playfair matrices. It should not be used to protect real data.")

# ---------------- Section 5 ----------------
S6_TITLE = "5. Team Contributions, Resources and Post-Challenge Outcome"

CONTRIBUTION_ROWS = [
    ("Student", "Seat No.", "Contribution"),
    ("Mr. Hamza Saleem", "CR-23009",
     "Cipher design (Tier 3 rules, keys, parameters) and the write-up of the cipher description, sequence and keys"),
    ("Mr. Ameem Akhtar", "CR-23013",
     "Report layout and formatting, repository setup on GitHub, and the reference list"),
    ("Mr. Minhal Rizvi", "CR-23017",
     "Test suite, performance benchmarks, resistance analysis, and independent verification of the pairs"),
    ("Mr. Muhammad Usman", "CR-23038",
     "Challenge dataset (plaintext selection, three incorrect pairs) and the write-up of the dataset and final explanation"),
    ("Mr. Maaz Wasim", "CR-23041",
     "Implementation of the three cipher tiers and the interactive command-line console"),
]

RESOURCE_ROWS = [
    ("Resource", "Used for"),
    ("CT-486 CCA activity brief", "Deliverable list and rules"),
    ("Academic references 1–6 (Section 8)", "Playfair, Vigenère, Index of Coincidence and product-cipher background"),
    ("Python 3 standard library", "Cipher, dataset generator, analysis and benchmarks"),
    ("unittest", f"{TEST_COUNT} automated tests (test_cca.py)"),
    ("ReportLab, python-docx", "PDF and Word reports"),
    ("Git and GitHub", "Version control and code submission"),
]

# ---------------- REPORT.md ----------------
MD_BEGIN = "<!-- BEGIN GENERATED: report_inputs.py (do not edit by hand) -->"
MD_END = "<!-- END GENERATED -->"


def _md_table(rows):
    esc = lambda s: s.replace("|", "\\|")
    out = ["| " + " | ".join(rows[0]) + " |", "|" + " :--- |" * len(rows[0])]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows[1:]]
    return "\n".join(out)


def _md_par(text):
    head, sep, rest = text.partition(": ")
    return f"**{head}:** {rest}" if sep and len(head) < 30 else text


def markdown():
    return "\n\n".join([
        MD_BEGIN,
        f"## {S5_TITLE}", S5_INTRO,
        "### Stage-by-stage rationale", _md_table(STAGE_ROWS),
        "### Keyspace", _md_table(KEYSPACE_ROWS),
        _md_par(S5_AFFINE),
        "### Flaw signatures of the challenge pairs", _md_par(S5_FLAWS), _md_table(FLAW_ROWS),
        _md_par(S5_ASSESSMENT),
        "---",
        f"## {S6_TITLE}",
        "### Contributions", _md_table(CONTRIBUTION_ROWS),
        "### Resource log", _md_table(RESOURCE_ROWS),
        "---",
        MD_END,
    ])


def sync_markdown(path=os.path.join(HERE, "REPORT.md")):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    a, b = text.index(MD_BEGIN), text.index(MD_END) + len(MD_END)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text[:a] + markdown() + text[b:])


if __name__ == "__main__":
    sync_markdown()
    print(f"REPORT.md Sections 4-5 refreshed ({TEST_COUNT} tests counted).")
