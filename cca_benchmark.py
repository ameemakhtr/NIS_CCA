"""
Reproduces every IoC and timing number quoted in the reports.
Run: python cca_benchmark.py   (timings vary by machine; IoC values are exact)
"""

import random
from collections import Counter
import time
from cca_cipher import AlKindiCompositeCipher, PlayfairCipher, VigenereCipher, clean_text
from cca_challenge import CHALLENGE_PLAINTEXTS, generate_challenge_dataset


def calculate_ic(text):
    counts = Counter(clean_text(text))
    n = sum(counts.values())
    return sum(f * (f - 1) for f in counts.values()) / (n * (n - 1)) if n > 1 else 0.0


def caesar(text, k=3):
    return "".join(chr((ord(c) - 65 + k) % 26 + 65) for c in clean_text(text))


def best_ms(fn, arg, reps=50):
    """Best-of-reps wall time in ms (least affected by OS noise)."""
    best = float("inf")
    for _ in range(reps):
        t = time.perf_counter()
        fn(arg)
        best = min(best, time.perf_counter() - t)
    return best * 1000


if __name__ == "__main__":
    corpus = "".join(clean_text(p) for p in CHALLENGE_PLAINTEXTS)
    ktcc = AlKindiCompositeCipher()
    pf, vg = PlayfairCipher("LABYRINTH"), VigenereCipher("VALIANT")
    challenge_ct = "".join(p["ciphertext"] for p in generate_challenge_dataset()["pairs"])

    print("Index of Coincidence over the 10 challenge plaintexts (%d letters)" % len(corpus))
    print(f"  Plaintext (English)        : {calculate_ic(corpus):.4f}")
    print(f"  Caesar (k=3)               : {calculate_ic(caesar(corpus)):.4f}  (always equals plaintext IoC)")
    print(f"  Playfair only (LABYRINTH)  : {calculate_ic(pf.encrypt(corpus)):.4f}")
    print(f"  Vigenere only (VALIANT)    : {calculate_ic(vg.encrypt(corpus)):.4f}")
    print(f"  KTCC challenge ciphertexts : {calculate_ic(challenge_ct):.4f}")
    print(f"  Uniform random (1/26)      : {1 / 26:.4f}")

    random.seed(0)
    print("\nTiming, best of 50 runs (ms)")
    print("  N       KTCC-enc  KTCC-dec  Caesar  Playfair  Vigenere  KTCC chars/s")
    for n in (100, 1000, 10000):
        text = "".join(random.choice("ABCDEFGHIKLMNOPQRSTUVWYZ") for _ in range(n))
        ct = ktcc.encrypt(text)[0]
        e, d = best_ms(ktcc.encrypt, text), best_ms(ktcc.decrypt, ct)
        c, p, v = best_ms(caesar, text), best_ms(pf.encrypt, text), best_ms(vg.encrypt, text)
        print(f"  {n:<7} {e:8.3f}  {d:8.3f}  {c:6.3f}  {p:8.3f}  {v:8.3f}  {len(ct) / (e / 1000):,.0f}")

