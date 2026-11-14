"""
Red Team Cryptanalysis & Automated Reverse-Engineering Suite
Course: Network and Information Security (CT-486 CCA)
Department of Computer Science & Information Technology
NED University of Engineering & Technology, Karachi, Pakistan

Target Cipher: Al-Kindi Tri-Tiered Composite Cipher (KTCC)

Nothing in this file knows the Blue Team's keys. Everything is derived from the
10 public (plaintext, ciphertext) pairs only.

Attack idea (known-plaintext):
  If the cipher is "Playfair, then a shift that depends only on the character
  position" (with an optional fixed swap inside some digraphs), then under the
  CORRECT Playfair matrix every genuine pair implies the SAME shift at each
  position. So:
    1. Simulated annealing searches Playfair matrices, scoring each by how many
       pairs agree on the implied per-position shift (key-free fitness).
    2. The consensus shift per position is the combined Tier 2 + Tier 3 keystream.
       A pair that disagrees with the consensus is a corrupted pair.
    3. The keystream is split into linear drift (delta*i + theta) plus a periodic
       Vigenere key by exhaustive search over delta and period.

Deliverables Covered:
  - Deliverable 6: Identification of cipher techniques used.
  - Deliverable 7: Identification and isolation of the 3 incorrect pairs.
  - Deliverable 8: Recovery of encryption keys and parameters.
  - Deliverable 9: Reconstruction of the full encryption sequence and algorithm.
  - Deliverable 10: Analytical evidence, statistical proofs, and verification.
"""

from typing import List, Dict, Any
import collections
import json
import math
import random
from cca_cipher import AlKindiCompositeCipher, clean_text, prepare_playfair_digraphs

ALPHABET25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Playfair alphabet, I/J merged

# Relative English letter frequencies (%), used only to pick the most English-like
# Vigenere keyword among the 26 cryptographically equivalent (key, theta) splits.
ENGLISH_FREQ = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 2.4,
                6.7, 7.5, 1.9, 0.095, 6.0, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2.0, 0.074]


def calculate_ic(text: str) -> float:
    """
    Computes Index of Coincidence (IC) for a given ciphertext.
    Formula: IC = sum(f_i * (f_i - 1)) / (N * (N - 1))
    English Plaintext IC: ~0.067
    Random / Polyalphabetic IC: ~0.038
    """
    cleaned = clean_text(text)
    n = len(cleaned)
    if n <= 1:
        return 0.0
    counts = collections.Counter(cleaned)
    numerator = sum(f * (f - 1) for f in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator


def _playfair_pair(pos, mat, a, b):
    """Encrypt one digraph with a flat 25-letter matrix (standard Playfair rules)."""
    r1, c1 = pos[a]
    r2, c2 = pos[b]
    if r1 == r2:
        return mat[r1 * 5 + (c1 + 1) % 5], mat[r2 * 5 + (c2 + 1) % 5]
    if c1 == c2:
        return mat[((r1 + 1) % 5) * 5 + c1], mat[((r2 + 1) % 5) * 5 + c2]
    return mat[r1 * 5 + c2], mat[r2 * 5 + c1]


class RedTeamCryptanalysis:
    """
    Key-free cryptanalysis engine: detects corrupted pairs, recovers keys,
    and verifies the reconstructed algorithm.
    """
    ANNEAL_ITERS = 25000      # ~80% of single runs converge; restarts cover the rest
    MAX_RESTARTS = 20
    CONVERGED = 0.95          # fraction of positions in agreement that counts as solved

    def __init__(self, challenge_pairs: List[Dict[str, Any]]):
        self.pairs = challenge_pairs
        self.statistical_profiles = {}
        self.invalid_pairs = []
        self.valid_pairs = []
        self.recovered_keys = {}
        self._solution = None

        # blocks[j] = [(pair_id, pt_a, pt_b, ct0, ct1), ...] for every pair that has digraph block j
        blocks = collections.defaultdict(list)
        for p in self.pairs:
            ct = [ord(c) - 65 for c in clean_text(p["ciphertext"])]
            for j, (a, b) in enumerate(prepare_playfair_digraphs(p["plaintext"])):
                if 2 * j + 1 < len(ct):
                    blocks[j].append((p["pair_id"], a, b, ct[2 * j], ct[2 * j + 1]))
        self._blocks = [blocks[j] for j in sorted(blocks)]
        self._max_score = sum(2 * len(b) for b in self._blocks)

    # ------------------------------------------------------------------ D6
    def run_preliminary_statistical_profiling(self) -> Dict[str, Any]:
        """
        Deliverable 6 & 10: structural and statistical evidence, all computed.
          - Even ciphertext lengths              -> digraphic (Playfair-like) grouping.
          - len(CT) == len(Playfair-prepared PT) -> J->I merge, X filler and Z pad are used.
          - Index of Coincidence                 -> polyalphabetic layer on top.
        """
        lengths = [len(clean_text(p["ciphertext"])) for p in self.pairs]
        all_even = all(n % 2 == 0 for n in lengths)
        prep_len = [2 * len(prepare_playfair_digraphs(p["plaintext"])) for p in self.pairs]
        raw_len = [len(clean_text(p["plaintext"])) for p in self.pairs]
        matches_prep = sum(c == q for c, q in zip(lengths, prep_len))
        matches_raw = sum(c == r for c, r in zip(lengths, raw_len))
        ic = calculate_ic("".join(p["ciphertext"] for p in self.pairs))
        if ic > 0.060:
            ic_note = "English-like: monoalphabetic or transposition only"
        elif ic > 0.045:
            ic_note = "Partially flattened: digraphic or short-period polyalphabetic"
        else:
            ic_note = "Near random (~0.0385): polyalphabetic / multi-stage substitution"

        profiles = {
            "total_pairs": len(self.pairs),
            "all_lengths_even": all_even,
            "overall_ic": round(ic, 4),
            "ic_interpretation": ic_note,
            "length_equals_playfair_prepared_pt": f"{matches_prep}/{len(self.pairs)}",
            "length_equals_raw_pt": f"{matches_raw}/{len(self.pairs)}",
            "detected_signatures": [
                f"All ciphertext lengths even: {all_even} -> digraphic block cipher (Playfair family)",
                f"CT length equals Playfair-prepared PT length (X filler, Z pad) in {matches_prep}/{len(self.pairs)} "
                f"pairs vs raw PT length in only {matches_raw}/{len(self.pairs)}",
                f"IC = {ic:.4f}: {ic_note}",
            ],
        }
        self.statistical_profiles = profiles
        return profiles

    # ------------------------------------------------------------------ core attack
    def _score(self, mat) -> int:
        """Key-free fitness: positions where pairs agree on the implied keystream (best of swap / no swap per block)."""
        pos = {ch: divmod(i, 5) for i, ch in enumerate(mat)}
        total = 0
        for blk in self._blocks:
            s = [[0] * 26 for _ in range(4)]
            for _, a, b, c0, c1 in blk:
                x, y = _playfair_pair(pos, mat, a, b)
                x, y = ord(x) - 65, ord(y) - 65
                s[0][(c0 - x) % 26] += 1
                s[1][(c1 - y) % 26] += 1
                s[2][(c0 - y) % 26] += 1
                s[3][(c1 - x) % 26] += 1
            total += max(max(s[0]) + max(s[1]), max(s[2]) + max(s[3]))
        return total

    def _anneal(self, rng: random.Random):
        cur = list(ALPHABET25)
        rng.shuffle(cur)
        cs = self._score(cur)
        best, bs = cur, cs
        for k in range(self.ANNEAL_ITERS):
            t = 4.0 * (1 - k / self.ANNEAL_ITERS) + 0.05
            nxt = cur[:]
            r = rng.random()
            if r < 0.9:                                  # swap two letters
                i, j = rng.sample(range(25), 2)
                nxt[i], nxt[j] = nxt[j], nxt[i]
            elif r < 0.95:                               # swap two rows
                a, b = rng.sample(range(5), 2)
                for c in range(5):
                    nxt[a * 5 + c], nxt[b * 5 + c] = nxt[b * 5 + c], nxt[a * 5 + c]
            else:                                        # swap two columns
                a, b = rng.sample(range(5), 2)
                for row in range(5):
                    nxt[row * 5 + a], nxt[row * 5 + b] = nxt[row * 5 + b], nxt[row * 5 + a]
            ns = self._score(nxt)
            if ns >= cs or rng.random() < math.exp((ns - cs) / t):
                cur, cs = nxt, ns
                if cs > bs:
                    best, bs = cur, cs
        return best, bs

    @staticmethod
    def _keyword_from_matrix(mat) -> str:
        """
        A Playfair matrix is only defined up to row/column rotation (25 equivalent grids).
        The keyword is the rotation whose tail is the unused alphabet in order.
        """
        best = None
        for dr in range(5):
            for dc in range(5):
                s = [mat[((r + dr) % 5) * 5 + (c + dc) % 5] for r in range(5) for c in range(5)]
                for k in range(1, 26):
                    if s[k:] == sorted(set(ALPHABET25) - set(s[:k])):
                        if best is None or k < len(best):
                            best = "".join(s[:k])
                        break
        return best or "".join(mat)

    def _solve(self) -> Dict[str, Any]:
        if self._solution:
            return self._solution
        rng = random.Random(486)  # fixed seed: reproducible run for the report
        restarts, mat, score = 0, None, -1
        while restarts < self.MAX_RESTARTS and score < self.CONVERGED * self._max_score:
            mat, score = self._anneal(rng)
            restarts += 1

        # Consensus keystream + orientation per block under the recovered matrix
        pos = {ch: divmod(i, 5) for i, ch in enumerate(mat)}
        keystream, swapped, implied = {}, {}, collections.defaultdict(dict)
        for j, blk in enumerate(self._blocks):
            outs = []
            for pid, a, b, c0, c1 in blk:
                x, y = _playfair_pair(pos, mat, a, b)
                outs.append((pid, ord(x) - 65, ord(y) - 65, c0, c1))
            options = []
            for sw in (False, True):
                k0 = collections.Counter(((c0 - (y if sw else x)) % 26) for _, x, y, c0, _ in outs)
                k1 = collections.Counter(((c1 - (x if sw else y)) % 26) for _, x, y, _, c1 in outs)
                options.append((k0.most_common(1)[0][1] + k1.most_common(1)[0][1], sw, k0, k1))
            _, sw, k0, k1 = max(options, key=lambda o: o[0])
            swapped[j] = sw
            keystream[2 * j] = k0.most_common(1)[0][0]
            keystream[2 * j + 1] = k1.most_common(1)[0][0]
            for pid, x, y, c0, c1 in outs:
                implied[pid][2 * j] = (c0 - (y if sw else x)) % 26
                implied[pid][2 * j + 1] = (c1 - (x if sw else y)) % 26

        # Positions where each pair disagrees with the consensus keystream
        deviations = {p["pair_id"]: [i for i, k in sorted(implied[p["pair_id"]].items()) if k != keystream[i]]
                      for p in self.pairs}

        self._solution = {
            "matrix": mat, "score": score, "restarts": restarts,
            "keystream": keystream, "swapped": swapped, "deviations": deviations,
        }
        self._solution.update(self._decompose_keystream(keystream, swapped))
        return self._solution

    @staticmethod
    def _decompose_keystream(keystream, swapped) -> Dict[str, Any]:
        """
        Split K[i] into drift (delta * w(i) + theta) plus a periodic Vigenere key V[u(i) mod p].
        u, w are either the position before or after the in-block swap; all four orderings
        are tested, so the data (not an assumption) decides the order of the layers.
        Returns the smallest period that fits exactly.
        """
        perm = lambda i: i ^ 1 if swapped[i // 2] else i
        ident = lambda i: i
        orders = {
            ("Vigenere", "swap", "drift"): (perm, ident),    # Vigenere indexed before swap, drift after
            ("swap", "Vigenere", "drift"): (ident, ident),
            ("Vigenere", "drift", "swap"): (perm, perm),
            ("swap", "drift", "Vigenere"): (ident, perm),
        }
        fits = []
        for period in range(1, 14):
            for order, (u, w) in orders.items():
                for delta in range(26):
                    groups = collections.defaultdict(set)
                    for i, k in keystream.items():
                        groups[u(i) % period].add((k - delta * w(i)) % 26)
                    if all(len(g) == 1 for g in groups.values()) and len(groups) == period:
                        fits.append((period, order, delta, [groups[r].pop() for r in range(period)]))
            if fits:
                break
        if not fits:
            return {"decomposition": None}
        period, order, delta, combined = fits[0]
        # V[r] + theta is all the data fixes; choose theta so V reads most like English.
        def english(theta):
            return sum(math.log(ENGLISH_FREQ[(c - theta) % 26]) for c in combined)
        theta = max(range(26), key=english)
        vig = "".join(chr((c - theta) % 26 + 65) for c in combined)
        return {"decomposition": {"period": period, "order": order, "delta": delta, "theta": theta,
                                  "vigenere_key": vig, "alternatives_at_min_period": len(fits)}}

    # ------------------------------------------------------------------ D7
    def audit_and_detect_invalid_pairs(self) -> Dict[str, Any]:
        """
        Deliverable 7: a pair is corrupted if its implied keystream disagrees with the
        consensus of the other pairs. The proof text is generated from the data.
        """
        sol = self._solve()
        pf_key = self._keyword_from_matrix(sol["matrix"])
        invalid, valid = [], []
        for p in self.pairs:
            pid, ct = p["pair_id"], clean_text(p["ciphertext"])
            dev = sol["deviations"][pid]
            if not dev:
                valid.append({"pair_id": pid, "status": "VALID", "plaintext": p["plaintext"], "ciphertext": ct,
                              "confidence": "Keystream agrees with consensus at every position"})
                continue
            # Predicted ciphertext letter = Playfair(PT) under recovered matrix + consensus keystream
            pf = AlKindiCompositeCipher(pf_key, "A", 0, 0).playfair.encrypt(p["plaintext"])
            pred = {}
            for i in dev:
                src = i ^ 1 if sol["swapped"][i // 2] else i
                pred[i] = chr((ord(pf[src]) - 65 + sol["keystream"][i]) % 26 + 65)
            offsets = {i: (ord(ct[i]) - ord(pred[i])) % 26 for i in dev}
            obs, exp = "".join(ct[i] for i in dev), "".join(pred[i] for i in dev)
            if len(dev) == 2 and dev[1] == dev[0] + 1 and obs == exp[::-1]:
                kind = f"letters at indices {dev[0]}-{dev[1]} are transposed (observed '{obs}', predicted '{exp}')"
            elif len(set(offsets.values())) == 1:
                kind = (f"uniform +{next(iter(offsets.values()))} mod 26 offset at indices {dev} "
                        f"(observed '{obs}', predicted '{exp}')")
            else:
                kind = f"offsets {offsets} at indices {dev} (observed '{obs}', predicted '{exp}')"
            invalid.append({
                "pair_id": pid, "status": "INVALID / TAMPERED", "plaintext": p["plaintext"],
                "received_ciphertext": ct, "diff_indices": dev,
                "mathematical_proof": (f"Implied keystream disagrees with the consensus of the other pairs at "
                                       f"{len(dev)} position(s): {kind}."),
            })
        self.valid_pairs, self.invalid_pairs = valid, invalid
        return {
            "valid_count": len(valid), "invalid_count": len(invalid),
            "identified_invalid_pair_ids": [x["pair_id"] for x in invalid],
            "invalid_details": invalid, "valid_details": valid,
        }

    # ------------------------------------------------------------------ D8 / D9
    def recover_keys_and_sequence(self) -> Dict[str, Any]:
        """Deliverable 8 & 9: keys and layer order, all taken from the solved data."""
        sol = self._solve()
        dec = sol["decomposition"] or {}
        pf_key = self._keyword_from_matrix(sol["matrix"])
        grid = [sol["matrix"][r * 5:(r + 1) * 5] for r in range(5)]
        swap_blocks = [j for j, s in sorted(sol["swapped"].items()) if s]
        swap_rule = ("even blocks (b mod 2 == 0)" if swap_blocks == list(range(0, len(sol["swapped"]), 2))
                     else f"blocks {swap_blocks}")
        order = dec.get("order", ())
        self.recovered_keys = {
            "annealing_restarts": sol["restarts"],
            "consistency_score": f"{sol['score']}/{self._max_score} positions agree",
            "tier1_technique": "5x5 Playfair Digraphic Matrix",
            "tier1_recovered_matrix_rows": [" ".join(r) for r in grid],
            "tier1_recovered_key": pf_key,
            "tier2_technique": "Polyalphabetic Vigenere Cipher",
            "tier2_recovered_key": dec.get("vigenere_key"),
            "tier2_key_length": dec.get("period"),
            "tier3_technique": "Alternating Digraph Inversion & Positional Dynamic Drift (ADI-PDD)",
            "tier3_swap_rule": swap_rule,
            "tier3_recovered_parameters": {"delta (slope multiplier)": dec.get("delta"),
                                           "theta (seed offset)": dec.get("theta")},
            "key_ambiguity_note": ("Only Vigenere[i] + theta is fixed by the data; all 26 (key, theta) splits "
                                   "encrypt identically. theta was chosen so the key reads most like English."),
            "complete_encryption_sequence": ("Plaintext -> Digraph Prep (J->I, X-filler, Z-pad) -> Playfair -> "
                                             + " -> ".join(order) + " -> Ciphertext"),
        }
        return self.recovered_keys

    # ------------------------------------------------------------------ D10
    def verify_roundtrip_decryption(self) -> List[Dict[str, Any]]:
        """Deliverable 10: rebuild the cipher from RECOVERED keys only and re-check every pair."""
        keys = self.recover_keys_and_sequence()
        params = keys["tier3_recovered_parameters"]
        cipher = AlKindiCompositeCipher(keys["tier1_recovered_key"], keys["tier2_recovered_key"],
                                        params["delta (slope multiplier)"], params["theta (seed offset)"])
        log = []
        for p in self.pairs:
            ct = clean_text(p["ciphertext"])
            expected = "".join(a + b for a, b in prepare_playfair_digraphs(p["plaintext"]))
            decrypted, _ = cipher.decrypt(ct)
            ok = decrypted == expected and cipher.encrypt(p["plaintext"])[0] == ct
            log.append({
                "pair_id": p["pair_id"],
                "original_plaintext": p["plaintext"],
                "prepared_plaintext": expected,
                "decrypted_plaintext": decrypted,
                "matches_original": ok,
                "verdict": "PASSED (exact round-trip with recovered keys)" if ok
                           else "REJECTED (does not round-trip with recovered keys)",
            })
        return log


if __name__ == "__main__":
    with open("challenge_dataset_public.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    analyzer = RedTeamCryptanalysis(data["pairs"])
    print("=== RED TEAM CRYPTANALYSIS INITIATED (no keys given) ===")

    stats = analyzer.run_preliminary_statistical_profiling()
    print("\n1. Statistical Profiles:")
    for s in stats["detected_signatures"]:
        print(f"   - {s}")

    audit = analyzer.audit_and_detect_invalid_pairs()
    print(f"\n2. Pair Verification Audit: Identified {audit['invalid_count']} Corrupted Pairs:")
    for inv in audit["invalid_details"]:
        print(f"   - Pair #{inv['pair_id']}: {inv['mathematical_proof']}")

    keys = analyzer.recover_keys_and_sequence()
    print("\n3. Recovered Cryptographic Keys & Architecture:")
    for k, v in keys.items():
        print(f"   {k}: {v}")

    print("\n4. Round-Trip Verification of Challenge Pairs:")
    for entry in analyzer.verify_roundtrip_decryption():
        print(f"   Pair #{entry['pair_id']}: [{entry['verdict']}]")
