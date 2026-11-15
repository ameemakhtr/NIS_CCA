"""
Academic Word DOCX Report Generator for CT-486 Complex Computing Activity (CCA)
Course: Network and Information Security (CT-486)
Department of Computer Science & Information Technology
NED University of Engineering & Technology, Karachi, Pakistan

Matches the exact academic style, structure, and density of NIS_CCP:
  - Clean Cover Page: Title, Subtitle, Final Year - Cyber Security, Batch: 2023, NED Logo
  - Group Members sorted by roll number: Hamza (09), Ameem (13), Minhal (17), Usman (38), Maaz (41)
  - Submitted to: Ms. Sayyda Sahar Fatima (Lecturer, Department of CS & IT)
  - No redundant cover lines, no TOC page, no rubric self-grading table
  - Distinct bullet and numbered items on separate lines with proper indentation
  - Blue Team Deliverables 1–5 (our assigned role)
  - Mathematical formulations, Callout boxes, 5x5 Matrix, Challenge Dataset, Benchmarks
"""

import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=60, bottom=60, left=90, right=90):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>'
    )
    tcPr.append(tcMar)


def add_bullet_item(doc, title, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_b = p.add_run("•  ")
    r_b.font.name = 'Times New Roman'
    r_b.font.size = Pt(10)
    r_b.bold = True
    if title:
        r_t = p.add_run(title + " ")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10)
        r_t.bold = True
    r_txt = p.add_run(text)
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(10)


def add_num_item(doc, num_str, title, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_n = p.add_run(num_str + "  ")
    r_n.font.name = 'Times New Roman'
    r_n.font.size = Pt(10)
    r_n.bold = True
    if title:
        r_t = p.add_run(title + " ")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10)
        r_t.bold = True
    r_txt = p.add_run(text)
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(10)


def add_callout_box(doc, text_lines, bg_hex="F8FAFC", border_hex="CBD5E1"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    
    # Border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:left w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    for i, line in enumerate(text_lines):
        if i > 0:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
        r = p.add_run(line)
        r.font.name = 'Courier New'
        r.font.size = Pt(8.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)


def build_cca_docx(output_filename="Complex_Computing_Activity_Report.docx"):
    docx_path = os.path.join(SCRIPT_DIR, output_filename)
    doc = docx.Document()

    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True

    # Configure Header & Footer matching NIS_CCP
    header = doc.sections[0].header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hrun = hp.add_run("Complex Computing Activity Report | CT-486: Network and Information Security")
    hrun.font.name = 'Times New Roman'
    hrun.font.size = Pt(9)
    hrun.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    footer = doc.sections[0].footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    frun1 = fp.add_run("Department of Computer Science & IT, NED University")
    frun1.font.name = 'Times New Roman'
    frun1.font.size = Pt(9)
    frun1.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # Base typography
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(5)

    # =========================================================
    # PAGE 1: COVER PAGE (EXACT NIS_CCP STYLE)
    # =========================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(28)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("Complex Computing Activity Report")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(24)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(4)
    r_course = p_course.add_run("CT-486: Network and Information Security")
    r_course.font.name = 'Times New Roman'
    r_course.font.size = Pt(15)
    r_course.bold = True
    r_course.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(3)
    r_dept = p_dept.add_run("Final Year - Cyber Security")
    r_dept.font.name = 'Times New Roman'
    r_dept.font.size = Pt(12.5)

    p_batch = doc.add_paragraph()
    p_batch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_batch.paragraph_format.space_after = Pt(20)
    r_batch = p_batch.add_run("Batch: 2023")
    r_batch.font.name = 'Times New Roman'
    r_batch.font.size = Pt(12)

    # Logo
    logo_path = os.path.join(SCRIPT_DIR, "ned_logo_1.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(22)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(2.0))

    # Group Members Header
    p_gm = doc.add_paragraph()
    p_gm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_gm.paragraph_format.space_after = Pt(10)
    run_gm = p_gm.add_run("Group Members:")
    run_gm.font.name = 'Times New Roman'
    run_gm.font.size = Pt(14)
    run_gm.bold = True
    run_gm.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

    # Members Table (Roll-Number Ordered)
    table_members = doc.add_table(rows=5, cols=2)
    table_members.alignment = WD_TABLE_ALIGNMENT.CENTER
    members_data = [
        ("Mr. Hamza Saleem", "CR-23009"),
        ("Mr. Ameem Akhtar", "CR-23013"),
        ("Mr. Minhal Rizvi", "CR-23017"),
        ("Mr. Muhammad Usman", "CR-23038"),
        ("Mr. Maaz Wasim", "CR-23041")
    ]
    for i, (name, roll) in enumerate(members_data):
        row = table_members.rows[i]
        cell_name = row.cells[0]
        cell_roll = row.cells[1]
        cell_name.width = Inches(3.4)
        cell_roll.width = Inches(1.8)

        p0 = cell_name.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(f"{name} " + ".".ljust(30, '.'))
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        r0.bold = True

        p1 = cell_roll.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(f"({roll})")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.bold = True

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subm.paragraph_format.space_before = Pt(26)
    p_subm.paragraph_format.space_after = Pt(2)
    r_subm = p_subm.add_run("Submitted to: Ms. Sayyda Sahar Fatima (Lecturer, Department of CS & IT)")
    r_subm.font.name = 'Times New Roman'
    r_subm.font.size = Pt(11)
    r_subm.bold = True

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_after = Pt(4)
    r_date = p_date.add_run("Submission Date: November 15, 2026")
    r_date.font.name = 'Times New Roman'
    r_date.font.size = Pt(11)

    # =========================================================
    # SECTION 1: ABSTRACT & PROBLEM FORMULATION
    # =========================================================
    doc.add_page_break()

    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.space_before = Pt(8)
    p_s1.paragraph_format.space_after = Pt(6)
    r_s1 = p_s1.add_run("1. Abstract & Problem Formulation")
    r_s1.font.name = 'Times New Roman'
    r_s1.font.size = Pt(14)
    r_s1.bold = True
    r_s1.font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)

    doc.add_paragraph(
        "Complex Computing Activity (CCA) Formulation: In accordance with the PEC / Washington Accord graduate attributes for engineering computing (CLO3: Design of Security Mechanisms), a Complex Computing Activity requires formulating, implementing, and cryptanalyzing multi-layered cryptographic primitives. Such problems demand strict adherence to Kerckhoffs's Principle and Shannon's informational criteria of Confusion and Diffusion, while guaranteeing linear computational efficiency and provable resilience against statistical cryptanalysis."
    )
    doc.add_paragraph(
        "Project Focus: This project addresses the CT-486 Classical Cipher Challenge by designing the Al-Kindi Tri-Tiered Composite Cipher (KTCC), named in tribute to Abu Yusuf Al-Kindi (801–873 CE), the pioneer of frequency cryptanalysis. KTCC cascades three mathematically complementary transformation layers: (1) a 5x5 Keyed Playfair digraphic substitution matrix, (2) a polyalphabetic Vigenère stream substitution, and (3) a team-designed Alternating Digraph Inversion with Positional Dynamic Drift (ADI-PDD)."
    )
    doc.add_paragraph(
        "Blue Team Role: Our group was assigned the Blue Team role. We designed the cipher and a corpus of 10 challenge plaintext-ciphertext pairs (7 genuine, 3 intentionally incorrect) that was handed to the Red Team group without the keys, algorithm or incorrect pairs. Breaking the cipher is the Red Team's task and is not part of this submission. Every genuine pair round-trips exactly with the keys in Deliverable 3, and the test suite checks this."
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================
    # SECTION 2: BLUE TEAM CIPHER DESIGN & SPECIFICATION
    # =========================================================
    p_s2 = doc.add_paragraph()
    p_s2.paragraph_format.space_before = Pt(8)
    p_s2.paragraph_format.space_after = Pt(6)
    r_s2 = p_s2.add_run("2. Blue Team Deliverables: Cipher Design & Specification")
    r_s2.font.name = 'Times New Roman'
    r_s2.font.size = Pt(14)
    r_s2.bold = True
    r_s2.font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)

    doc.add_paragraph(
        "Deliverable 1 – Cipher Name & Technical Description: The cipher is formally designated the Al-Kindi Tri-Tiered Composite Cipher (KTCC). It satisfies Claude Shannon's product cipher criteria by cascading three complementary classical primitives:"
    )

    add_num_item(doc, "1.", "Tier 1 (Polygraphic Digraph Substitution):", "A 5x5 Keyed Playfair Matrix encrypts adjacent character pairs, flattening single-character frequencies (IoC 0.0688 → 0.0551 on the challenge plaintexts) and scrambling word boundaries.")
    add_num_item(doc, "2.", "Tier 2 (Polyalphabetic Stream Substitution):", "A periodic Vigenère keystream shifts the digram stream, masking geometric Playfair symmetries (same row, column, and rectangle rules).")
    add_num_item(doc, "3.", "Tier 3 (Dynamic Transposition & Affine Drift - ADI-PDD):", "Alternating Digraph Inversion (ADI) swaps characters in even-indexed blocks, followed by Positional Dynamic Drift (PDD): Δ(i) = (3·i + 7) mod 26.")

    doc.add_paragraph("Deliverable 2 – Complete Encryption & Decryption Sequence:")

    add_callout_box(doc, [
        "Algorithm 1: KTCC Encryption Pipeline",
        "1. P_clean <- Filter uppercase A-Z from P; replace 'J' with 'I'",
        "2. Form digraphs (c1, c2); insert 'X' between identical letters ('Q' if XX); pad odd length with 'Z' ('X' if last letter is Z)",
        "3. Tier 1: S_1 <- Playfair_Encrypt(Digraphs, 5x5 Matrix Key: LABYRINTH)",
        "4. Tier 2: For i = 0 to N-1: S_2[i] <- (S_1[i] + K_V[i mod 7]) mod 26 (Key: VALIANT)",
        "5. Tier 3A: For block b = 0 to (N/2)-1: If b mod 2 == 0: Swap(S_2[2b], S_2[2b+1])",
        "6. Tier 3B: For i = 0 to N-1: C[i] <- (S_2[i] + (3·i + 7)) mod 26; Return C"
    ])

    add_callout_box(doc, [
        "Algorithm 2: KTCC Decryption Pipeline",
        "1. Validate Length(C) mod 2 == 0",
        "2. Inverse Tier 3B: For i = 0 to N-1: S_2'[i] <- (C[i] - (3·i + 7) + 26) mod 26",
        "3. Inverse Tier 3A: For block b = 0 to (N/2)-1: If b mod 2 == 0: Swap(S_2'[2b], S_2'[2b+1])",
        "4. Inverse Tier 2: For i = 0 to N-1: S_1[i] <- (S_2'[i] - K_V[i mod 7] + 26) mod 26",
        "5. Inverse Tier 1: P <- Playfair_Decrypt(S_1, 5x5 Matrix Key: LABYRINTH); Return P"
    ])

    doc.add_paragraph("Deliverable 3 – Secret Keys, 5x5 Keyed Matrix & Alphabet Rules:")
    add_bullet_item(doc, "Tier 1 Key & Matrix:", "Keyword LABYRINTH (9 characters). 'I' and 'J' share cell (1, 0). Remaining letters appended alphabetically.")
    add_bullet_item(doc, "Tier 2 Key:", "Vigenère keyword VALIANT (Length 7). Shifts: [21, 0, 11, 8, 0, 13, 19] modulo 26.")
    add_bullet_item(doc, "Tier 3 Parameters:", "Parity swap on even digraph blocks (b mod 2 == 0); Dynamic drift multiplier δ = 3, seed offset θ = 7.")
    add_bullet_item(doc, "Conditioning Rules:", "All text capitalized; 'J' -> 'I'; duplicate digraph letters split with 'X' ('Q' when the doubled letter is 'X'); odd-length messages padded with 'Z' ('X' when the last letter is 'Z').")

    # 5x5 Matrix Table
    mat_data = [
        ("Row / Col", "Col 0", "Col 1", "Col 2", "Col 3", "Col 4"),
        ("Row 0", "L", "A", "B", "Y", "R"),
        ("Row 1", "I/J", "N", "T", "H", "C"),
        ("Row 2", "D", "E", "F", "G", "K"),
        ("Row 3", "M", "O", "P", "Q", "S"),
        ("Row 4", "U", "V", "W", "X", "Z")
    ]
    t_m = doc.add_table(rows=len(mat_data), cols=6)
    t_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row_vals in enumerate(mat_data):
        row = t_m.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            if r_idx == 0:
                r.bold = True
                set_cell_background(cell, "2C3E50")
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            elif c_idx == 0:
                r.bold = True
                set_cell_background(cell, "EAEEF4")
                r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Deliverable 4: Challenge Dataset Table
    doc.add_paragraph("Deliverable 4 – Standardized Challenge Dataset (10 Plaintext-Ciphertext Pairs):")
    chal_data = [
        ("#", "Plaintext (Input)", "Ciphertext (Output)", "Len", "True Status"),
        ("1", "DEFEND THE PERIMETER AT ONCE", "MJEDKEZZENDOEKXNLBKMOGIT", "24", "GENUINE"),
        ("2", "ZERO TRUST ARCHITECTURE SECURES DATA", "RAYQHYRJRVVYXJFFSZIKYVFWMLERYPRF", "32", "GENUINE"),
        ("3", "CRYPTOGRAPHIC PROTOCOL FAILURE DETECTED", "JPZOVNCVEJVBCASSAEWRNMGWMUUNSPRJTKDH", "36", "POISONED (Tampered)"),
        ("4", "INCIDENT RESPONSE TEAM ENGAGED IMMEDIATELY", "ASGLLALEAIFEOCGKQEUNOZZHGWGGHBSHPOZQWRQR", "40", "GENUINE"),
        ("5", "QUANTUM COMPUTING THREATENS TRADITIONAL RSA", "ERLCCEKFEXFKXOZENYJJXMJNDBFEQXLRQXZDVQQP", "40", "GENUINE"),
        ("6", "MALWARE EXFILTRATING SENSITIVE AUDIT LOGS", "STSZRXYSLOWHSIDBYYQDUZXXIZHXAZPQTPYPMY", "38", "POISONED (Tampered)"),
        ("7", "FIREWALL BLOCKS UNTRUSTED NETWORK TRAFFIC", "AIYIHRQROITACREZSKUYMAANPQZENDJGNNEZPRJL", "40", "GENUINE"),
        ("8", "AUTHENTICATION TOKEN EXPIRES SOON REFRESH", "CQFAKKZKHVABOCFPQUNNAHXUPWGSRGEONMIRTQ", "38", "GENUINE"),
        ("9", "DENIAL OF SERVICE ATTACK FLOODS ROUTER", "MJRLGXHBAWTNSUGNHYWACVYKWCGHPKQZCALF", "36", "POISONED (Tampered)"),
        ("10", "ELLIPTIC CURVE DIGITAL SIGNATURE STANDARD", "HIGBLSFFPQTNOMZDSEKZMXZQONTOBVRFQKZOQY", "38", "GENUINE")
    ]
    t_ch = doc.add_table(rows=len(chal_data), cols=5)
    t_ch.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row_vals in enumerate(chal_data):
        row = t_ch.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                set_cell_background(cell, "2C3E50")
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            if c_idx == 4 and "POISONED" in val:
                r.bold = True
                r.font.color.rgb = RGBColor(0xB9, 0x1C, 0x1C)
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Deliverable 5: Walkthrough Trace Table
    doc.add_paragraph("Deliverable 5 – Step-by-Step Transformation Trace (Pair #1):")
    tr_data = [
        ("Processing Stage", "Intermediate State", "Cryptographic Purpose"),
        ("Raw Input", "DEFEND THE PERIMETER AT ONCE", "Original plaintext."),
        ("Digraph Preparation", "DE FE ND TH EP ER IM ET ER AT ON CE", "Stripped whitespace, 12 digram blocks."),
        ("Tier 1: Playfair Matrix", "EF GF IE HC FO KA DU FN KA BN VE NK", "Digraphic substitution (flattens unigrams)."),
        ("Tier 2: Vigenère Stream", "ZF RN IR AX FZ SA QN AN VI BA OZ NV", "Polyalphabetic keystream masks symmetries."),
        ("Tier 3A: Digraph Inversion", "FZ RN RI AX ZF SA NQ AN IV BA ZO NV", "Alternating Parity Inversion on even blocks."),
        ("Tier 3B: Dynamic Drift", "MJ ED KE ZZ EN DO EK XN LB KM OG IT", "Affine Drift Δ(i) = (3i + 7) mod 26."),
        ("Final Ciphertext", "MJEDKEZZENDOEKXNLBKMOGIT", "Transmitted challenge ciphertext (Length 24).")
    ]
    t_tr = doc.add_table(rows=len(tr_data), cols=3)
    t_tr.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row_vals in enumerate(tr_data):
        row = t_tr.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                set_cell_background(cell, "2C3E50")
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================
    # SECTION 4: BENCHMARKS & COMPLEXITY
    # =========================================================
    p_s4 = doc.add_paragraph()
    p_s4.paragraph_format.space_before = Pt(8)
    p_s4.paragraph_format.space_after = Pt(6)
    r_s4 = p_s4.add_run("3. Performance Metrics and Empirical Complexity")
    r_s4.font.name = 'Times New Roman'
    r_s4.font.size = Pt(14)
    r_s4.bold = True
    r_s4.font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)

    doc.add_paragraph(
        "Measured with cca_benchmark.py (best of 50 runs on one development machine; absolute times vary by hardware) for payload sizes from N = 100 to 10,000 characters. The challenge ciphertexts have an Index of Coincidence of 0.0388, against 0.0385 for uniform random text and 0.0688 for the plaintexts (also from cca_benchmark.py)."
    )

    bn_data = [
        ("Payload Length (N)", "KTCC Encrypt (ms)", "KTCC Decrypt (ms)", "Caesar Shift (ms)", "Overhead Factor", "Throughput (chars/s)"),
        ("100 chars", "0.124 ms", "0.099 ms", "0.021 ms", "5.9×", "824,576 chars/s"),
        ("1,000 chars", "1.208 ms", "0.962 ms", "0.190 ms", "6.4×", "844,091 chars/s"),
        ("10,000 chars", "11.805 ms", "9.273 ms", "1.770 ms", "6.7×", "865,425 chars/s")
    ]
    t_bn = doc.add_table(rows=len(bn_data), cols=6)
    t_bn.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row_vals in enumerate(bn_data):
        row = t_bn.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                set_cell_background(cell, "2C3E50")
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    doc.add_paragraph(
        "Asymptotic Scaling: Time complexity is strictly linear O(N) across all three stages (Playfair: N/2 lookups; Vigenère: N modular shifts; ADI-PDD: N/4 swaps and N affine operations). Memory is O(N) with constant O(1) matrix storage."
    )

    # =========================================================
    # SECTION 5: CCA ATTRIBUTE MAPPING (no self-grading)
    # =========================================================
    p_s5m = doc.add_paragraph()
    p_s5m.paragraph_format.space_before = Pt(8)
    p_s5m.paragraph_format.space_after = Pt(6)
    r_s5m = p_s5m.add_run("4. CCA Attribute Mapping & Resources")
    r_s5m.font.name = 'Times New Roman'
    r_s5m.font.size = Pt(14)
    r_s5m.bold = True
    r_s5m.font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)

    doc.add_paragraph('How the CCA attributes named in the activity brief appear in this submission:')
    cca_data = [('CCA Attribute', 'Application in This Activity', 'Evidence'), ('CCA-1: Range of Resources', 'Five-member team; the activity brief; six published references (Academic References); the 10-pair challenge dataset; analytical methods (Index of Coincidence, timing benchmarks); Python 3.14 standard library, unittest, ReportLab, python-docx, Git and GitHub.', 'cca_cipher.py, cca_challenge.py, cca_benchmark.py, test_cca.py (6 tests), challenge_dataset_public.json'), ('CCA-3: Innovation', 'Team-designed Tier 3 (ADI-PDD) combining an even-block digraph swap with a position-dependent affine drift, layered on Playfair and Vigenère. The 3 incorrect pairs use three different flaw types (substitution, transposition, tail shift), so no single check catches all of them.', 'Deliverables 1–4'), ('CCA-5: Familiarity', "Classical principles (Playfair geometry, Vigenère periodicity, Friedman's IoC) applied to design an unfamiliar three-layer composite. Ciphertext IoC is 0.0388, close to random (0.0385). The design's own limit is identified, with fixes.", 'Deliverable 5; Benchmarks; Suggestions')]
    t_cca = doc.add_table(rows=len(cca_data), cols=3)
    t_cca.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row_vals in enumerate(cca_data):
        row = t_cca.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                set_cell_background(cell, "2C3E50")
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            elif c_idx == 0:
                r.bold = True
            if r_idx > 0 and r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)

    # =========================================================
    # SECTION 6: SUGGESTIONS FOR IMPROVEMENT
    # =========================================================
    p_s5 = doc.add_paragraph()
    p_s5.paragraph_format.space_before = Pt(8)
    p_s5.paragraph_format.space_after = Pt(6)
    r_s5 = p_s5.add_run("5. Suggestions for Improving the Cipher's Security")
    r_s5.font.name = 'Times New Roman'
    r_s5.font.size = Pt(14)
    r_s5.bold = True
    r_s5.font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)

    doc.add_paragraph('Known limitation: Tiers 2 and 3 only add position-dependent shifts plus a fixed swap, so together they act as one fixed keystream. With the Playfair matrix and a few known pairs, that keystream can be read off directly. Suggestions 1 and 3 remove this.')
    add_num_item(doc, "1.", "Dynamic Autokey Keystream Scheduling:", "Replace the periodic repeating Vigenère key with an autokey mechanism (K[i] = P[i - L_V]) to eliminate keystream periodicity and defeat Kasiski autocorrelation.")
    add_num_item(doc, "2.", "Non-Linear S-Box Permutation:", "Insert an 8-bit non-linear substitution box between Tier 2 and Tier 3 to break linear modular arithmetic over Z_26, preventing modular equation solvers from decoupling the stages.")
    add_num_item(doc, "3.", "Cipher Block Chaining (CBC) Feedback:", "Modularly add previous ciphertext digraphs into current plaintext digraphs (P'[b] = (P[b] + C[b-1]) mod 26) to eliminate identical ciphertext outputs for repeating phrases.")
    add_num_item(doc, "4.", "Expanded 6x6 Matrix Alphabet:", "Expand the Playfair grid to 6x6 (36 alphanumeric cells: A–Z and 0–9) to eliminate the 'I'/'J' merger and allow native encryption of IP addresses and cryptographic tokens.")

    # =========================================================
    # SECTION 6: CODE SUBMISSION & TEAM CONTRIBUTORS
    # =========================================================
    p_s6 = doc.add_paragraph()
    p_s6.paragraph_format.space_before = Pt(8)
    p_s6.paragraph_format.space_after = Pt(6)
    r_s6 = p_s6.add_run("6. Code Submission & Execution Details")
    r_s6.font.name = 'Times New Roman'
    r_s6.font.size = Pt(14)
    r_s6.bold = True
    r_s6.font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)

    doc.add_paragraph(
        "All project source files and automated test suites are publicly hosted on GitHub at: https://github.com/ameemakhtr/NIS_CCA"
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_callout_box(doc, [
        "# Automated Execution & Verification Commands",
        "python cca_main.py --blue         # Show cipher design and challenge dataset",
        "python test_cca.py                # Run automated unit test suite (6/6 tests passing)",
        "python build_report_pdf.py        # Recompile publication-grade PDF report",
        "python build_report_docx.py       # Recompile publication-grade Word DOCX report"
    ])

    # =========================================================
    # SECTION 7: REFERENCES
    # =========================================================
    p_s7 = doc.add_paragraph()
    p_s7.paragraph_format.space_before = Pt(8)
    p_s7.paragraph_format.space_after = Pt(6)
    r_s7 = p_s7.add_run("7. Academic References")
    r_s7.font.name = 'Times New Roman'
    r_s7.font.size = Pt(14)
    r_s7.bold = True
    r_s7.font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)

    refs = [
        "1. Al-Kindi, Abu Yusuf Ya'qub ibn Ishaq (c. 850 CE). Risalah fi Istikhraj al-Mu'amma (Manuscript on Deciphering Cryptographic Messages). House of Wisdom, Baghdad.",
        "2. Shannon, Claude E. (1949). 'Communication Theory of Secrecy Systems.' Bell System Technical Journal, 28(4), 656–715.",
        "3. Friedman, William F. (1922). The Index of Coincidence and Its Applications in Cryptography. Department of Ciphers, Publication No. 22, Riverbank Laboratories.",
        "4. Stallings, William (2020). Cryptography and Network Security: Principles and Practice (8th Edition). Pearson Education.",
        "5. Wheatstone, Charles & Playfair, Lyon (1854). 'On the Playfair System of Cipher.' Minutes of the Royal Society of Arts, London.",
        "6. Vigenère, Blaise de (1586). Traicté des Chiffres ou Secrètes Manières d'Escrire. Paris, France."
    ]
    for ref in refs:
        add_bullet_item(doc, "", ref)

    # Save DOCX
    doc.save(docx_path)
    print(f"[SUCCESS] Publication-grade DOCX successfully built: {docx_path}")


if __name__ == "__main__":
    build_cca_docx()
