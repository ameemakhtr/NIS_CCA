"""
Automated Test Suite for CT-486 Classical Cipher Challenge (CCA)
Title: Al-Kindi Tri-Tiered Composite Cipher (KTCC)
Department of Computer Science & Information Technology
NED University of Engineering & Technology, Karachi, Pakistan
"""

import unittest
import json
import os
import subprocess
import sys
from cca_cipher import (
    AlKindiCompositeCipher,
    PlayfairCipher,
    VigenereCipher,
    AlternatingDynamicDiffusion,
    clean_text,
    prepare_playfair_digraphs
)
from cca_challenge import generate_challenge_dataset
from cca_analysis import affine_structure_check, compute_flaw_rows

HERE = os.path.dirname(os.path.abspath(__file__))
CORRUPTED = {3, 6, 9}


class TestAlKindiCompositeCCA(unittest.TestCase):

    def setUp(self):
        self.playfair_key = "LABYRINTH"
        self.vigenere_key = "VALIANT"
        self.delta = 3
        self.theta = 7
        self.cipher = AlKindiCompositeCipher(
            playfair_key=self.playfair_key,
            vigenere_key=self.vigenere_key,
            delta=self.delta,
            theta=self.theta
        )

    def test_playfair_digraph_rules(self):
        digraphs = prepare_playfair_digraphs("BALLOON")
        expected = [('B', 'A'), ('L', 'X'), ('L', 'O'), ('O', 'N')]
        self.assertEqual(digraphs, expected)

        digraphs_odd = prepare_playfair_digraphs("HELLO")
        self.assertEqual(len(digraphs_odd), 3)

    def test_playfair_roundtrip(self):
        pf = PlayfairCipher("SECRETKEY")
        pt = "ATTACKATDAWN"
        ct = pf.encrypt(pt)
        dt = pf.decrypt(ct)
        self.assertEqual(len(ct), len(dt))
        self.assertEqual(dt, "AT"+"TA"+"CK"+"AT"+"DA"+"WN")

    def test_vigenere_roundtrip(self):
        vig = VigenereCipher("KEYWORD")
        msg = "NETWORKSECURITY"
        ct = vig.encrypt(msg)
        dt = vig.decrypt(ct)
        self.assertEqual(msg, dt)

    def test_alternating_dynamic_diffusion_roundtrip(self):
        diff = AlternatingDynamicDiffusion(delta=5, theta=11)
        text = "HELLOSECURITYTEST"
        if len(text) % 2 != 0:
            text += 'X'
        ct = diff.encrypt(text)
        dt = diff.decrypt(ct)
        self.assertEqual(text, dt)

    def test_composite_cipher_roundtrip(self):
        test_strings = [
            "DEFEND THE PERIMETER AT ONCE",
            "NETWORK AND INFORMATION SECURITY COMPLEX COMPUTING",
            "CLASSICAL CRYPTOGRAPHY CHALLENGE",
            "CYBER DEFENSE IN DEPTH",
            "SHORT"
        ]
        for s in test_strings:
            ct, trace = self.cipher.encrypt(s)
            dt, _ = self.cipher.decrypt(ct)
            self.assertEqual(dt, trace["prepared_plaintext"])

    def test_challenge_dataset_composition(self):
        dataset = generate_challenge_dataset()
        pairs = dataset["pairs"]
        ground_truth = dataset["ground_truth"]

        self.assertEqual(len(pairs), 10, "Dataset must contain exactly 10 pairs")
        
        valid_count = sum(1 for gt in ground_truth if gt["is_valid"])
        invalid_count = sum(1 for gt in ground_truth if not gt["is_valid"])

        self.assertEqual(valid_count, 7, "Dataset must contain exactly 7 correct pairs")
        self.assertEqual(invalid_count, 3, "Dataset must contain exactly 3 incorrect pairs")

        invalid_ids = [gt["pair_id"] for gt in ground_truth if not gt["is_valid"]]
        self.assertEqual(invalid_ids, [3, 6, 9])

    # ---------- frozen dataset & post-challenge checks ----------

    def _public_pairs(self):
        with open(os.path.join(HERE, "challenge_dataset_public.json"), encoding="utf-8") as f:
            return json.load(f)["pairs"]

    def _prepared(self, text):
        return "".join(a + b for a, b in prepare_playfair_digraphs(text))

    def test_known_answer_pair_1(self):
        self.assertEqual(self.cipher.encrypt("DEFEND THE PERIMETER AT ONCE")[0], "MJEDKEZZENDOEKXNLBKMOGIT")

    def test_genuine_public_pairs_roundtrip(self):
        for p in self._public_pairs():
            if p["pair_id"] in CORRUPTED:
                continue
            self.assertEqual(self.cipher.encrypt(p["plaintext"])[0], p["ciphertext"], p["pair_id"])
            self.assertEqual(self.cipher.decrypt(p["ciphertext"])[0], self._prepared(p["plaintext"]), p["pair_id"])

    def test_corrupted_public_pairs_fail_both_ways(self):
        for p in self._public_pairs():
            if p["pair_id"] not in CORRUPTED:
                continue
            self.assertNotEqual(self.cipher.encrypt(p["plaintext"])[0], p["ciphertext"], p["pair_id"])
            self.assertNotEqual(self.cipher.decrypt(p["ciphertext"])[0], self._prepared(p["plaintext"]), p["pair_id"])

    def test_public_json_matches_generator(self):
        generated = generate_challenge_dataset()["pairs"]
        public = self._public_pairs()
        self.assertEqual([(p["plaintext"], p["ciphertext"]) for p in public],
                         [(p["plaintext"], p["ciphertext"]) for p in generated])

    def test_committed_dataset_matches_generator(self):
        with open(os.path.join(HERE, "challenge_dataset.json"), encoding="utf-8") as f:
            committed = json.load(f)["pairs"]
        self.assertEqual([p["ciphertext"] for p in committed],
                         [p["ciphertext"] for p in generate_challenge_dataset()["pairs"]])

    def test_public_json_leaks_no_secrets(self):
        with open(os.path.join(HERE, "challenge_dataset_public.json"), encoding="utf-8") as f:
            text = f.read().lower()
        for word in ["labyrinth", "valiant", "ground_truth", "is_valid", "delta", "theta",
                     "cleaned_prepared", "reason", "trace"]:
            self.assertNotIn(word, text)

    def test_tiers_2_3_are_affine(self):
        self.assertTrue(affine_structure_check(50))

    def test_flaw_damage_is_local(self):
        for r in compute_flaw_rows():
            if r["pair_id"] in CORRUPTED:
                self.assertTrue(1 <= len(r["damaged_blocks"]) <= 2, r)
            else:
                self.assertEqual(r["damaged_blocks"], [], r)
            self.assertTrue(r["length_preserved"], r)

    def test_interactive_mode_exits_on_eof(self):
        result = subprocess.run([sys.executable, "cca_main.py", "--interactive"], input="enc HELLO\n",
                                capture_output=True, text=True, timeout=20, cwd=HERE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Final CT", result.stdout)
        self.assertNotIn("EOF when reading a line", result.stdout)


if __name__ == "__main__":
    unittest.main()
