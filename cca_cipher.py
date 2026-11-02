"""
CT-486 Complex Computing Activity (CCA): Classical Cipher Challenge
Title: Al-Kindi Tri-Tiered Composite Cipher (KTCC)
Department of Computer Science & Information Technology
NED University of Engineering & Technology, Karachi, Pakistan

Design Heritage & Conceptual Foundation:
  - Historical Basis: Named in honor of Abu Yusuf Ya'qub ibn Ishaq al-Kindi (801-873 CE),
    universally recognized as the Father of Cryptanalysis (House of Wisdom, Baghdad).
  - Architecture: A Three-Tiered Composite Product Cipher (Claude Shannon, 1949).

Three Cascaded Tiers:
  - Tier 1 (Classical Polygraphic): 5x5 Playfair Digraphic Matrix (Key: LABYRINTH)
  - Tier 2 (Classical Polyalphabetic): Keyed Vigenère Substitution (Key: VALIANT)
  - Tier 3 (Team-Designed Technique): Alternating Digraph Inversion & Positional Dynamic Drift (ADI-PDD)
    [Alternating Digraph Inversion on Even Blocks + Positional Dynamic Caesar Shift: (3i + 7) mod 26]
"""

from typing import List, Tuple, Dict, Optional
import math


def clean_text(text: str) -> str:
    """Preprocess text: uppercase A-Z only."""
    return "".join([c.upper() for c in text if c.isalpha()])


def prepare_playfair_digraphs(text: str) -> List[Tuple[str, str]]:
    """
    Standard Playfair plaintext preparation:
    - Uppercase, alphabetic only.
    - Consolidate 'J' into 'I' (standard 25-letter alphabet convention).
    - If two consecutive letters in a digraph are identical, insert filler 'X' (or 'Q' if duplicate is 'X').
    - If total length is odd, append padding character 'Z' (or 'X' if ends with 'Z').
    """
    cleaned = clean_text(text).replace('J', 'I')
    if not cleaned:
        return []

    digraphs: List[Tuple[str, str]] = []
    i = 0
    while i < len(cleaned):
        c1 = cleaned[i]
        if i + 1 < len(cleaned):
            c2 = cleaned[i + 1]
            if c1 == c2:
                # Duplicate characters in a pair: split with filler
                filler = 'Q' if c1 == 'X' else 'X'
                digraphs.append((c1, filler))
                i += 1
            else:
                digraphs.append((c1, c2))
                i += 2
        else:
            # Trailing odd character: pad
            pad = 'X' if c1 == 'Z' else 'Z'
            digraphs.append((c1, pad))
            i += 1
    return digraphs


class PlayfairCipher:
    """
    Tier 1: Polygraphic Digraphic Substitution (5x5 Keyed Matrix)
    Classical Cipher Technique 1.
    """
    def __init__(self, key: str = "LABYRINTH"):
        self.key_phrase = clean_text(key).replace('J', 'I')
        self.matrix, self.pos_map = self._build_matrix(self.key_phrase)

    def _build_matrix(self, key_phrase: str) -> Tuple[List[List[str]], Dict[str, Tuple[int, int]]]:
        seen = set()
        matrix_chars = []
        for ch in key_phrase + "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # Note: J is consolidated into I
            if ch not in seen and ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
                seen.add(ch)
                matrix_chars.append(ch)

        matrix = [matrix_chars[r * 5:(r + 1) * 5] for r in range(5)]
        pos_map = {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}
        return matrix, pos_map

    def encrypt_digraph(self, c1: str, c2: str) -> Tuple[str, str]:
        r1, col1 = self.pos_map[c1]
        r2, col2 = self.pos_map[c2]

        if r1 == r2:
            # Same row: shift right circular
            return (self.matrix[r1][(col1 + 1) % 5], self.matrix[r2][(col2 + 1) % 5])
        elif col1 == col2:
            # Same column: shift down circular
            return (self.matrix[(r1 + 1) % 5][col1], self.matrix[(r2 + 1) % 5][col2])
        else:
            # Rectangle: swap columns
            return (self.matrix[r1][col2], self.matrix[r2][col1])

    def decrypt_digraph(self, c1: str, c2: str) -> Tuple[str, str]:
        r1, col1 = self.pos_map[c1]
        r2, col2 = self.pos_map[c2]

        if r1 == r2:
            # Same row: shift left circular
            return (self.matrix[r1][(col1 - 1) % 5], self.matrix[r2][(col2 - 1) % 5])
        elif col1 == col2:
            # Same column: shift up circular
            return (self.matrix[(r1 - 1) % 5][col1], self.matrix[(r2 - 1) % 5][col2])
        else:
            # Rectangle: swap columns
            return (self.matrix[r1][col2], self.matrix[r2][col1])

    def encrypt(self, plaintext: str) -> str:
        digraphs = prepare_playfair_digraphs(plaintext)
        res = []
        for c1, c2 in digraphs:
            e1, e2 = self.encrypt_digraph(c1, c2)
            res.extend([e1, e2])
        return "".join(res)

    def decrypt(self, ciphertext: str) -> str:
        cleaned = clean_text(ciphertext).replace('J', 'I')
        if len(cleaned) % 2 != 0:
            raise ValueError("Playfair ciphertext must have even length.")
        res = []
        for i in range(0, len(cleaned), 2):
            d1, d2 = self.decrypt_digraph(cleaned[i], cleaned[i + 1])
            res.extend([d1, d2])
        return "".join(res)


class VigenereCipher:
    """
    Tier 2: Polyalphabetic Periodic Substitution
    Classical Cipher Technique 2.
    Formula: C[i] = (P[i] + K[i mod L]) mod 26
    """
    def __init__(self, key: str = "VALIANT"):
        self.key = clean_text(key)
        if not self.key:
            raise ValueError("Vigenere key cannot be empty.")

    def encrypt(self, text: str) -> str:
        cleaned = clean_text(text)
        k_len = len(self.key)
        res = []
        for i, ch in enumerate(cleaned):
            shift = ord(self.key[i % k_len]) - 65
            c = (ord(ch) - 65 + shift) % 26
            res.append(chr(c + 65))
        return "".join(res)

    def decrypt(self, text: str) -> str:
        cleaned = clean_text(text)
        k_len = len(self.key)
        res = []
        for i, ch in enumerate(cleaned):
            shift = ord(self.key[i % k_len]) - 65
            p = (ord(ch) - 65 - shift) % 26
            res.append(chr(p + 65))
        return "".join(res)


class AlternatingDynamicDiffusion:
    """
    Tier 3: Team-Designed Technique
    Alternating Digraph Inversion & Positional Dynamic Drift (ADI-PDD)
    
    Components:
    1. Alternating Digraph Inversion (ADI):
       For alternating blocks (specifically even-indexed blocks b in {0, 2, 4...}),
       the two characters in the digraph are swapped (c[2b] <-> c[2b+1]).
       Odd-indexed blocks retain standard order.
    2. Positional Dynamic Drift (PDD):
       Dynamic affine shift based on character index i:
       Delta(i) = (i * delta + theta) mod 26
       where delta = 3 (slope multiplier), theta = 7 (seed offset).
       C3[i] = (C2_swapped[i] + Delta(i)) mod 26
    """
    def __init__(self, delta: int = 3, theta: int = 7):
        self.delta = delta % 26
        self.theta = theta % 26

    def get_shift(self, i: int) -> int:
        return (i * self.delta + self.theta) % 26

    def encrypt(self, text: str) -> str:
        cleaned = clean_text(text)
        chars = list(cleaned)
        n = len(chars)

        # Step 1: Alternating Digraph Inversion on even blocks
        for b in range(n // 2):
            if b % 2 == 0:
                chars[2 * b], chars[2 * b + 1] = chars[2 * b + 1], chars[2 * b]

        # Step 2: Positional Dynamic Drift
        res = []
        for i, ch in enumerate(chars):
            shift = self.get_shift(i)
            c = (ord(ch) - 65 + shift) % 26
            res.append(chr(c + 65))
        return "".join(res)

    def decrypt(self, text: str) -> str:
        cleaned = clean_text(text)
        chars = list(cleaned)
        n = len(chars)

        # Step 1: Invert Positional Dynamic Drift
        unrolled = []
        for i, ch in enumerate(chars):
            shift = self.get_shift(i)
            p = (ord(ch) - 65 - shift) % 26
            unrolled.append(chr(p + 65))

        # Step 2: Invert Alternating Digraph Inversion (Swapping even blocks is self-inverting)
        for b in range(n // 2):
            if b % 2 == 0:
                unrolled[2 * b], unrolled[2 * b + 1] = unrolled[2 * b + 1], unrolled[2 * b]

        return "".join(unrolled)


class AlKindiCompositeCipher:
    """
    Al-Kindi Tri-Tiered Composite Cipher (KTCC)
    
    End-to-End Orchestrator:
      Plaintext -> [Tier 1: Playfair 5x5] -> Intermediate 1 (C1)
                -> [Tier 2: Keyed Vigenere] -> Intermediate 2 (C2)
                -> [Tier 3: Alternating Dynamic Diffusion] -> Final Ciphertext (C3)
    """
    def __init__(self, playfair_key: str = "LABYRINTH", vigenere_key: str = "VALIANT", delta: int = 3, theta: int = 7):
        self.playfair = PlayfairCipher(playfair_key)
        self.vigenere = VigenereCipher(vigenere_key)
        self.adi_diffusion = AlternatingDynamicDiffusion(delta, theta)

        self.playfair_key = self.playfair.key_phrase
        self.vigenere_key = self.vigenere.key
        self.delta = delta
        self.theta = theta

    def encrypt(self, plaintext: str) -> Tuple[str, Dict[str, str]]:
        """
        Encrypts plaintext through all 3 tiers.
        Returns:
          final_ciphertext, trace_dictionary
        """
        cleaned = clean_text(plaintext).replace('J', 'I')
        digraphs = prepare_playfair_digraphs(cleaned)
        prepared_pt = "".join([c1 + c2 for c1, c2 in digraphs])

        stage1_out = self.playfair.encrypt(prepared_pt)
        stage2_out = self.vigenere.encrypt(stage1_out)
        stage3_out = self.adi_diffusion.encrypt(stage2_out)

        trace = {
            "plaintext_raw": plaintext,
            "prepared_plaintext": prepared_pt,
            "stage1_playfair": stage1_out,
            "stage2_vigenere": stage2_out,
            "stage3_final": stage3_out,
        }
        return stage3_out, trace

    def decrypt(self, ciphertext: str) -> Tuple[str, Dict[str, str]]:
        """
        Decrypts ciphertext by reversing all 3 tiers in exact reverse order:
        C3 -> [Reverse Tier 3: ADI-PDD] -> C2 -> [Reverse Tier 2: Vigenere] -> C1 -> [Reverse Tier 1: Playfair] -> Plaintext
        """
        cleaned = clean_text(ciphertext)
        if len(cleaned) % 2 != 0:
            raise ValueError("Ciphertext must have an even length.")

        stage2_rev = self.adi_diffusion.decrypt(cleaned)
        stage1_rev = self.vigenere.decrypt(stage2_rev)
        recovered_pt = self.playfair.decrypt(stage1_rev)

        trace = {
            "ciphertext_raw": ciphertext,
            "stage3_reversed": stage2_rev,
            "stage2_reversed": stage1_rev,
            "stage1_reversed_pt": recovered_pt,
        }
        return recovered_pt, trace


# Backward compatibility aliases
OrbitalDynamicDiffusion = AlternatingDynamicDiffusion
InqilabGurdishDiffusion = AlternatingDynamicDiffusion
TeamDesignedDiffusion = AlternatingDynamicDiffusion
AlKindiSeTahaCipher = AlKindiCompositeCipher
ChimeraCompositeCipher = AlKindiCompositeCipher


if __name__ == "__main__":
    cipher = AlKindiCompositeCipher()
    test_msg = "DEFEND THE PERIMETER AT ONCE"
    ct, trace = cipher.encrypt(test_msg)
    pt, rev_trace = cipher.decrypt(ct)
    print("=== AL-KINDI TRI-TIERED COMPOSITE CIPHER (KTCC) ===")
    print(f"Original : {test_msg}")
    print(f"Prepared : {trace['prepared_plaintext']}")
    print(f"Tier 1   : {trace['stage1_playfair']}")
    print(f"Tier 2   : {trace['stage2_vigenere']}")
    print(f"Tier 3   : {ct}")
    print(f"Decrypted: {pt}")
    assert pt == trace['prepared_plaintext'], "Decryption verification failed!"
    print("Verification Successful!")
