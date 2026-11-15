"""
CT-486 Classical Cipher Challenge (CCA) - Unified CLI Console
Course: Network and Information Security (CT-486)
Department of Computer Science & Information Technology
NED University of Engineering & Technology, Karachi, Pakistan

Target Cipher: Al-Kindi Tri-Tiered Composite Cipher (KTCC)
               Historical Basis: Abu Yusuf Al-Kindi (Father of Cryptanalysis)

Usage:
  python cca_main.py --blue          # Inspect Blue Team Cipher Design & Challenge Pairs
  python cca_main.py --verify        # Run the automated unit test suite (test_cca.py)
  python cca_main.py --interactive   # Enter interactive encryption / cryptanalysis shell
"""

import sys
import argparse
import json
from cca_cipher import AlKindiCompositeCipher, clean_text
from cca_challenge import generate_challenge_dataset, export_challenge_markdown


def run_blue_team():
    print("=" * 85)
    print("BLUE TEAM SUBMISSION: AL-KINDI TRI-TIERED COMPOSITE CIPHER (KTCC)")
    print("Historical Pedigree: Honors Abu Yusuf Al-Kindi (Father of Cryptanalysis)")
    print("=" * 85)
    print("1. Cipher Architecture (Three Cascaded Tiers):")
    print("   - Tier 1 (Classical Polygraphic)   : 5x5 Playfair Digraphic Matrix (Key: LABYRINTH)")
    print("   - Tier 2 (Classical Polyalphabetic): Keyed Vigenere Cipher (Key: VALIANT)")
    print("   - Tier 3 (Team-Designed Technique) : Alternating Digraph Inversion & Positional Dynamic Drift")
    print("                                        Alternating Parity Inversion on Even Digrams (ADI)")
    print("                                        Positional Dynamic Drift (PDD): Delta(i) = (3*i + 7) mod 26")
    print("-" * 85)
    
    dataset = generate_challenge_dataset()
    print("2. Challenge Dataset (10 Pairs with 7 Genuine & 3 Corrupted):")
    print(export_challenge_markdown(dataset))
    print("-" * 85)
    print("3. Ground-Truth Flaw Analysis (Kept Confidential during challenge):")
    for gt in dataset["ground_truth"]:
        status = "GENUINE" if gt["is_valid"] else "CORRUPTED"
        print(f"   [Pair {gt['pair_id']:02d}] {status:9s} : {gt['reason']}")
    print("=" * 85)


def interactive_mode():
    cipher = AlKindiCompositeCipher("LABYRINTH", "VALIANT", delta=3, theta=7)
    print("=" * 85)
    print("INTERACTIVE AL-KINDI COMPOSITE CIPHER TERMINAL")
    print("Commands: 'enc <text>', 'dec <ciphertext>', 'quit'")
    print("=" * 85)
    while True:
        try:
            line = input("KTCC> ").strip()
            if not line:
                continue
            if line.lower() in ["quit", "exit", "q"]:
                break
            parts = line.split(" ", 1)
            cmd = parts[0].lower()
            if cmd == "enc" and len(parts) > 1:
                ct, trace = cipher.encrypt(parts[1])
                print(f"   Prepared PT   : {trace['prepared_plaintext']}")
                print(f"   Tier 1 (PF)   : {trace['stage1_playfair']}")
                print(f"   Tier 2 (VG)   : {trace['stage2_vigenere']}")
                print(f"   Final CT (T3) : {ct}")
            elif cmd == "dec" and len(parts) > 1:
                pt, trace = cipher.decrypt(parts[1])
                print(f"   Decrypted PT  : {pt}")
            else:
                print("   Unknown command. Use 'enc <text>', 'dec <text>', or 'quit'.")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except Exception as e:
            print(f"   Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="CT-486 CCA Al-Kindi Composite Cipher Console")
    parser.add_argument("--blue", action="store_true", help="Display Blue Team cipher design & challenge set")
    parser.add_argument("--verify", action="store_true", help="Run automated test suite")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive cipher terminal")

    args = parser.parse_args()

    if args.blue:
        run_blue_team()
    elif args.interactive:
        interactive_mode()
    elif args.verify:
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromName("test_cca")
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    else:
        run_blue_team()


if __name__ == "__main__":
    main()
