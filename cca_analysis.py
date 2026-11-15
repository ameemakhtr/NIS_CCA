"""
Post-challenge resistance analysis of KTCC (uses the real keys, so run it only after the challenge).
Run: python cca_analysis.py

1. Keyspace size.
2. Affine check: Tiers 2+3 add a key-dependent offset that cancels in ciphertext differences.
3. Flaw signatures: what each corrupted pair looks like after decryption with the correct keys.
"""

import math
import random
import sys
from cca_cipher import AlKindiCompositeCipher, AlternatingDynamicDiffusion, VigenereCipher, prepare_playfair_digraphs
from cca_challenge import generate_challenge_dataset

ALPHABET25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Playfair output alphabet (no J)
KEYSETS = [("VALIANT", 3, 7), ("ZEBRAXY", 11, 19)]
FLAW_LABELS = {  # short form of the ground-truth reasons in cca_challenge.py
    3: "One letter changed (+4) at index 5",
    6: "Letters at indices 2-3 swapped (odd block 1)",
    9: "Last 4 letters shifted +11",
}


def _sci(n):
    if n < 10**6:
        return f"{n:,}"
    exp = int(math.floor(math.log10(n)))
    return f"{n / 10**exp:.3f}e{exp}"


def keyspace_rows():
    """(component, formula, size, bits). Last rows: nominal total and total after known equivalent keys."""
    parts = [("Playfair 5x5 matrix", "25!", math.factorial(25)),
             ("Vigenère key (length 7)", "26^7", 26**7),
             ("Drift (δ, θ)", "26^2", 26**2)]
    total = math.prod(n for _, _, n in parts)
    # 25 cyclic row/column shifts of a Playfair matrix encrypt identically; θ can be absorbed into the
    # Vigenère key (26 equivalent splits). So distinct ciphers are at most total / (25 * 26).
    effective = total // (25 * 26)
    rows = parts + [("Total (nominal)", "25! x 26^7 x 26^2", total),
                    ("Distinct ciphers (at most)", "total / (25 x 26)", effective)]
    return [(name, f, _sci(n), f"~2^{math.log2(n):.1f}") for name, f, n in rows]


def _swap_perm(n):
    """Index map of the ADI step: position i of the output holds input position perm[i]."""
    p = list(range(n))
    for b in range(0, n // 2, 2):
        p[2 * b], p[2 * b + 1] = p[2 * b + 1], p[2 * b]
    return p


def _tiers23(x, vkey, delta, theta):
    return AlternatingDynamicDiffusion(delta, theta).encrypt(VigenereCipher(vkey).encrypt(x))


def affine_hits(trials=200, length=24, seed=486):
    """How many random (X, Y) pairs satisfy C(X) - C(Y) = X[perm] - Y[perm] under every key set."""
    rng = random.Random(seed)
    perm = _swap_perm(length)
    hits = 0
    for _ in range(trials):
        x = "".join(rng.choice(ALPHABET25) for _ in range(length))
        y = "".join(rng.choice(ALPHABET25) for _ in range(length))
        expected = [(ord(x[perm[i]]) - ord(y[perm[i]])) % 26 for i in range(length)]
        diffs = []
        for vkey, d, t in KEYSETS:
            cx, cy = _tiers23(x, vkey, d, t), _tiers23(y, vkey, d, t)
            diffs.append([(ord(a) - ord(b)) % 26 for a, b in zip(cx, cy)])
        hits += all(df == expected for df in diffs)
    return hits


def affine_structure_check(trials=200):
    return affine_hits(trials) == trials


def compute_flaw_rows():
    """Decrypt every challenge ciphertext with the real keys and locate the damage. No printing."""
    data = generate_challenge_dataset()
    valid = {g["pair_id"]: g["is_valid"] for g in data["ground_truth"]}
    cipher = AlKindiCompositeCipher()
    rows = []
    for p in data["pairs"]:
        prepared = "".join(a + b for a, b in prepare_playfair_digraphs(p["plaintext"]))
        decrypted = cipher.decrypt(p["ciphertext"])[0]
        wrong = [i for i, (a, b) in enumerate(zip(prepared, decrypted)) if a != b]
        rows.append({
            "pair_id": p["pair_id"],
            "status": "Genuine" if valid[p["pair_id"]] else "Corrupted",
            "flaw": FLAW_LABELS.get(p["pair_id"], "None"),
            "damaged_blocks": sorted({i // 2 for i in wrong}),
            "wrong_letters": len(wrong),
            "length": len(prepared),
            "length_preserved": len(p["ciphertext"]) == len(prepared),
        })
    return rows


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # labels contain è, δ, θ; Windows pipes default to cp1252
    print("1. Keyspace")
    for name, f, size, bits in keyspace_rows():
        print(f"   {name:28s} {f:20s} {size:>12s}  {bits}")

    print("\n2. Affine structure of Tiers 2+3")
    hits = affine_hits(200)
    print(f"   C(X) - C(Y) = X[perm] - Y[perm] (mod 26) under both key sets {KEYSETS}: {hits}/200")
    print("   The Tier 2/3 key cancels in differences, so it adds only a fixed offset per position.")

    print("\n3. Flaw signatures (decrypted with the real keys)")
    for r in compute_flaw_rows():
        blocks = ", ".join(map(str, r["damaged_blocks"])) or "-"
        print(f"   Pair {r['pair_id']:2d}  {r['status']:9s}  blocks [{blocks:6s}]  "
              f"{r['wrong_letters']}/{r['length']} wrong  length kept: {r['length_preserved']}  {r['flaw']}")
