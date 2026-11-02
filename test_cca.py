"""
Automated Test Suite for CT-486 Classical Cipher Challenge (CCA)
Title: Al-Kindi Tri-Tiered Composite Cipher (KTCC)
Department of Computer Science & Information Technology
NED University of Engineering & Technology, Karachi, Pakistan
"""

import unittest
import json
from cca_cipher import (
    AlKindiCompositeCipher,
    PlayfairCipher,
    VigenereCipher,
    AlternatingDynamicDiffusion,
    clean_text,
    prepare_playfair_digraphs
)
from cca_challenge import generate_challenge_dataset
from cca_attack import RedTeamCryptanalysis, calculate_ic


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

    def test_red_team_cryptanalysis_detection(self):
        dataset = generate_challenge_dataset()
        analyzer = RedTeamCryptanalysis(dataset["pairs"])

        stats = analyzer.run_preliminary_statistical_profiling()
        self.assertTrue(stats["all_lengths_even"])
        self.assertLess(stats["overall_ic"], 0.05)

        audit = analyzer.audit_and_detect_invalid_pairs()
        self.assertEqual(audit["identified_invalid_pair_ids"], [3, 6, 9])
        self.assertEqual(audit["valid_count"], 7)
        self.assertEqual(audit["invalid_count"], 3)

        keys = analyzer.recover_keys_and_sequence()
        self.assertEqual(keys["tier1_recovered_key"], "LABYRINTH")
        self.assertEqual(keys["tier2_recovered_key"], "VALIANT")

        v_log = analyzer.verify_roundtrip_decryption()
        for entry in v_log:
            if entry["pair_id"] in [3, 6, 9]:
                self.assertFalse(entry["matches_original"])
            else:
                self.assertTrue(entry["matches_original"])


if __name__ == "__main__":
    unittest.main()
