"""
Academic PDF Report Generator for CT-486 Complex Computing Activity (CCA)
Course: Network and Information Security (CT-486)
Department of Computer Science & Information Technology
NED University of Engineering & Technology, Karachi, Pakistan

Matches the exact academic style, structure, and density of NIS_CCP:
  - Clean Cover Page: Title, Subtitle, Final Year - Cyber Security, Batch: 2023, NED Logo
  - Group Members sorted by roll number: Hamza (09), Ameem (13), Minhal (17), Usman (38), Maaz (41)
  - Submitted to: Ms. Sayyda Sahar Fatima (Lecturer, Department of CS & IT)
  - No redundant cover lines, no duplicate reports, no TOC page
  - All table cells wrapped in Paragraphs with auto-wrapping, zero text overlap
  - Distinct bullet and numbered items on separate lines with proper indentation
  - Blue Team Deliverables 1–5 (our assigned role)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from xml.sax.saxutils import escape
import report_inputs as ri
from report_inputs import TEST_COUNT

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def chunk_cipher(s: str, n: int = 4) -> str:
    """Chunks long unspaced strings into blocks with spaces so ReportLab Paragraphs wrap cleanly."""
    return " ".join([s[i:i+n] for i in range(0, len(s), n)])


class NumberedCanvas(canvas.Canvas):
    """Running academic header and dynamic 'Page X of Y' footer matching NIS_CCP."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:  # Skip cover page
            self.saveState()
            self.setFont("Times-Roman", 9)
            self.setFillColor(colors.HexColor("#555555"))
            
            # Running Header
            self.drawString(54, 746, "Complex Computing Activity Report | CT-486: Network and Information Security")
            self.setStrokeColor(colors.HexColor("#D0D5DD"))
            self.setLineWidth(0.6)
            self.line(54, 738, 558, 738)
            
            # Running Footer
            self.line(54, 46, 558, 46)
            self.drawString(54, 34, "Department of Computer Science & IT, NED University")
            self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
            self.restoreState()


def build_cca_pdf(output_filename="Complex_Computing_Activity_Report.pdf"):
    pdf_path = os.path.join(SCRIPT_DIR, output_filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Academic Typography Styles matching NIS_CCP
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=24,
        leading=28,
        alignment=1,  # Center
        textColor=colors.HexColor("#1A252F")
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        alignment=1,
        textColor=colors.HexColor("#2C3E50")
    )

    dept_style = ParagraphStyle(
        'CoverDept',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12.5,
        leading=16.5,
        alignment=1,
        textColor=colors.HexColor("#333333")
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=13,
        leading=16.5,
        spaceBefore=7,
        spaceAfter=4,
        textColor=colors.HexColor("#1A252F"),
        keepWithNext=True
    )

    sub_heading = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=10,
        leading=13.5,
        spaceBefore=4,
        spaceAfter=2,
        textColor=colors.HexColor("#2C3E50"),
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.8,
        leading=12.4,
        spaceAfter=3,
        alignment=4,  # Justify
        textColor=colors.HexColor("#222222")
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.6,
        leading=12.0,
        leftIndent=14,
        firstLineIndent=-9,
        spaceAfter=2,
        alignment=4,
        textColor=colors.HexColor("#222222")
    )

    numbered_style = ParagraphStyle(
        'NumberedStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.6,
        leading=12.0,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=2,
        alignment=4,
        textColor=colors.HexColor("#222222")
    )

    # Table Cell Typography Styles (Guarantees wrap and prevents text collisions)
    th_style = ParagraphStyle(
        'THStyle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=7.8,
        leading=9.8,
        alignment=1,
        textColor=colors.whitesmoke
    )

    td_style = ParagraphStyle(
        'TDStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7.4,
        leading=9.4,
        alignment=0,  # Left
        textColor=colors.HexColor("#222222")
    )

    td_center = ParagraphStyle(
        'TDCenter',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7.4,
        leading=9.4,
        alignment=1,  # Center
        textColor=colors.HexColor("#222222")
    )

    td_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=7.4,
        leading=9.4,
        alignment=0,
        textColor=colors.HexColor("#1A252F")
    )

    td_code = ParagraphStyle(
        'TDCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.6,
        alignment=0,
        textColor=colors.HexColor("#1A252F")
    )

    td_danger = ParagraphStyle(
        'TDDanger',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=7.4,
        leading=9.4,
        alignment=1,
        textColor=colors.HexColor("#B91C1C")
    )

    td_success = ParagraphStyle(
        'TDSuccess',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=7.4,
        leading=9.4,
        alignment=1,
        textColor=colors.HexColor("#15803D")
    )

    story = []

    # =========================================================
    # PAGE 1: COVER PAGE (EXACT NIS_CCP STYLE)
    # =========================================================
    story.append(Spacer(1, 28))
    story.append(Paragraph("Complex Computing Activity Report", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("CT-486: Network and Information Security", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Final Year - Cyber Security", dept_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Batch: 2023", dept_style))
    story.append(Spacer(1, 24))

    # NED University Crest / Logo
    logo_path = os.path.join(SCRIPT_DIR, "ned_logo_1.png")
    if os.path.exists(logo_path):
        story.append(RLImage(logo_path, width=2.0*inch, height=2.0*inch))
    story.append(Spacer(1, 24))

    story.append(Paragraph("Group Members:", subtitle_style))
    story.append(Spacer(1, 10))

    # Roll-number ordered members: Hamza (09), Ameem (13), Minhal (17), Usman (38), Maaz (41)
    members_data = [
        [Paragraph("<b>Mr. Hamza Saleem</b> ........................................................", body_style), Paragraph("<b>(CR-23009)</b>", body_style)],
        [Paragraph("<b>Mr. Ameem Akhtar</b> .........................................................", body_style), Paragraph("<b>(CR-23013)</b>", body_style)],
        [Paragraph("<b>Mr. Minhal Rizvi</b> .........................................................", body_style), Paragraph("<b>(CR-23017)</b>", body_style)],
        [Paragraph("<b>Mr. Muhammad Usman</b> .....................................................", body_style), Paragraph("<b>(CR-23038)</b>", body_style)],
        [Paragraph("<b>Mr. Maaz Wasim</b> .........................................................", body_style), Paragraph("<b>(CR-23041)</b>", body_style)],
    ]
    t_members = Table(members_data, colWidths=[3.8*inch, 1.8*inch])
    t_members.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_members)

    story.append(Spacer(1, 32))
    story.append(Paragraph("<b>Submitted to:</b> Ms. Sayyda Sahar Fatima (Lecturer, Department of CS & IT)", body_style))
    story.append(Paragraph("<b>Submission Date:</b> November 15, 2026", body_style))
    story.append(PageBreak())

    # =========================================================
    # SECTION 1: ABSTRACT & PROBLEM FORMULATION
    # =========================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("1. Abstract & Problem Formulation", section_heading))
    
    story.append(Paragraph(
        "<b>Complex Computing Activity (CCA) Formulation:</b> In accordance with the PEC / Washington Accord graduate attributes for engineering computing (CLO3: Design of Security Mechanisms), a Complex Computing Activity requires formulating, implementing, and cryptanalyzing multi-layered cryptographic primitives. Such problems demand strict adherence to Kerckhoffs's Principle and Shannon's informational criteria of <i>Confusion</i> and <i>Diffusion</i>, while guaranteeing linear computational efficiency and provable resilience against statistical cryptanalysis.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Project Focus:</b> This project addresses the <b>CT-486 Classical Cipher Challenge</b> by designing the <b>Al-Kindi Tri-Tiered Composite Cipher (KTCC)</b>, named in tribute to Abu Yusuf Al-Kindi (801–873 CE), the pioneer of frequency cryptanalysis. KTCC cascades three mathematically complementary transformation layers: (1) a 5x5 Keyed Playfair digraphic substitution matrix, (2) a polyalphabetic Vigenère stream substitution, and (3) a team-designed Alternating Digraph Inversion with Positional Dynamic Drift (ADI-PDD).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Blue Team Role:</b> Our group was assigned the Blue Team role. We designed the cipher and a corpus of 10 challenge plaintext-ciphertext pairs (7 genuine, 3 intentionally incorrect) that was handed to the Red Team group without the keys, algorithm or incorrect pairs. Breaking the cipher is the Red Team's task and is not part of this submission. Every genuine pair round-trips exactly with the keys in Deliverable 3, and the test suite checks this.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # =========================================================
    # SECTION 2: BLUE TEAM CIPHER DESIGN & SPECIFICATION
    # =========================================================
    story.append(Paragraph("2. Blue Team Deliverables: Cipher Design & Specification", section_heading))
    story.append(Paragraph(
        "<b>Deliverable 1 – Cipher Name & Technical Description:</b> The cipher is formally designated the <b>Al-Kindi Tri-Tiered Composite Cipher (KTCC)</b>. It satisfies Claude Shannon's product cipher criteria by cascading three complementary classical primitives:",
        body_style
    ))

    # DISTINCT NUMBERED ITEMS ON SEPARATE LINES
    story.append(Paragraph(
        "<b>1. Tier 1 (Polygraphic Digraph Substitution):</b> A 5x5 Keyed Playfair Matrix encrypts adjacent character pairs, flattening single-character frequencies (IoC 0.0688 → 0.0551 on the challenge plaintexts) and scrambling word boundaries.",
        numbered_style
    ))
    story.append(Paragraph(
        "<b>2. Tier 2 (Polyalphabetic Stream Substitution):</b> A periodic Vigenère keystream shifts the digram stream, masking geometric Playfair symmetries (same row, column, and rectangle rules).",
        numbered_style
    ))
    story.append(Paragraph(
        "<b>3. Tier 3 (Dynamic Transposition & Affine Drift - ADI-PDD):</b> Alternating Digraph Inversion (ADI) swaps characters in even-indexed blocks, followed by Positional Dynamic Drift (PDD): &Delta;(<i>i</i>) = (3&middot;<i>i</i> + 7) mod 26.",
        numbered_style
    ))

    story.append(Paragraph("<b>Deliverable 2 – Complete Encryption & Decryption Sequence:</b>", sub_heading))

    # Algorithm 1: Encryption Box
    algo1_lines = (
        "<b>Algorithm 1: KTCC Encryption Pipeline</b><br/>"
        "1. <i>P<sub>clean</sub></i> &larr; Filter uppercase A-Z from <i>P</i>; replace 'J' with 'I'<br/>"
        "2. Form digraphs (<i>c</i><sub>1</sub>, <i>c</i><sub>2</sub>); insert 'X' between identical letters ('Q' if XX); pad odd length with 'Z' ('X' if last letter is Z)<br/>"
        "3. <b>Tier 1:</b> <i>S</i><sub>1</sub> &larr; Playfair_Encrypt(Digraphs, 5x5 Matrix Key: <code>LABYRINTH</code>)<br/>"
        "4. <b>Tier 2:</b> For <i>i</i> = 0 to <i>N</i>-1: <i>S</i><sub>2</sub>[<i>i</i>] &larr; (<i>S</i><sub>1</sub>[<i>i</i>] + <i>K<sub>V</sub></i>[<i>i</i> mod 7]) mod 26 (Key: <code>VALIANT</code>)<br/>"
        "5. <b>Tier 3A:</b> For block <i>b</i> = 0 to (<i>N</i>/2)-1: If <i>b</i> mod 2 == 0: Swap(<i>S</i><sub>2</sub>[2<i>b</i>], <i>S</i><sub>2</sub>[2<i>b</i>+1])<br/>"
        "6. <b>Tier 3B:</b> For <i>i</i> = 0 to <i>N</i>-1: <i>C</i>[<i>i</i>] &larr; (<i>S</i><sub>2</sub>[<i>i</i>] + (3&middot;<i>i</i> + 7)) mod 26; Return <i>C</i>"
    )
    t_a1 = Table([[Paragraph(f"<font face='Courier' size=7.2>{algo1_lines}</font>", body_style)]], colWidths=[6.9*inch])
    t_a1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_a1)
    story.append(Spacer(1, 3))

    # Algorithm 2: Decryption Box
    algo2_lines = (
        "<b>Algorithm 2: KTCC Decryption Pipeline</b><br/>"
        "1. Validate Length(<i>C</i>) mod 2 == 0<br/>"
        "2. <b>Inverse Tier 3B:</b> For <i>i</i> = 0 to <i>N</i>-1: <i>S</i><sub>2</sub>'[<i>i</i>] &larr; (<i>C</i>[<i>i</i>] - (3&middot;<i>i</i> + 7) + 26) mod 26<br/>"
        "3. <b>Inverse Tier 3A:</b> For block <i>b</i> = 0 to (<i>N</i>/2)-1: If <i>b</i> mod 2 == 0: Swap(<i>S</i><sub>2</sub>'[2<i>b</i>], <i>S</i><sub>2</sub>'[2<i>b</i>+1])<br/>"
        "4. <b>Inverse Tier 2:</b> For <i>i</i> = 0 to <i>N</i>-1: <i>S</i><sub>1</sub>[<i>i</i>] &larr; (<i>S</i><sub>2</sub>'[<i>i</i>] - <i>K<sub>V</sub></i>[<i>i</i> mod 7] + 26) mod 26<br/>"
        "5. <b>Inverse Tier 1:</b> <i>P</i> &larr; Playfair_Decrypt(<i>S</i><sub>1</sub>, 5x5 Matrix Key: <code>LABYRINTH</code>); Return <i>P</i>"
    )
    t_a2 = Table([[Paragraph(f"<font face='Courier' size=7.2>{algo2_lines}</font>", body_style)]], colWidths=[6.9*inch])
    t_a2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_a2)
    story.append(PageBreak())

    # Deliverable 3: Keys, 5x5 Matrix, Special Rules
    story.append(Paragraph("<b>Deliverable 3 – Secret Keys, 5x5 Keyed Matrix & Alphabet Rules:</b>", sub_heading))
    story.append(Paragraph(
        "&bull; <b>Tier 1 Key & Matrix:</b> Keyword <code>LABYRINTH</code> (9 characters). 'I' and 'J' share cell (1, 0). Remaining letters appended alphabetically.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Tier 2 Key:</b> Vigenère keyword <code>VALIANT</code> (Length 7). Shifts: [21, 0, 11, 8, 0, 13, 19] modulo 26.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Tier 3 Parameters:</b> Parity swap on even digraph blocks (<i>b</i> mod 2 == 0); Dynamic drift multiplier &delta; = 3, seed offset &theta; = 7.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Conditioning Rules:</b> All text uppercase; 'J' replaced with 'I'; duplicate digraph letters split with 'X' ('Q' when the doubled letter is 'X'); odd-length messages padded with 'Z' ('X' when the last letter is 'Z').",
        bullet_style
    ))

    # 5x5 Matrix Table (Wrapped in Paragraphs with High-Contrast Legible Headers)
    matrix_raw = [
        ["Row / Col", "Col 0", "Col 1", "Col 2", "Col 3", "Col 4"],
        ["Row 0", "L", "A", "B", "Y", "R"],
        ["Row 1", "I/J", "N", "T", "H", "C"],
        ["Row 2", "D", "E", "F", "G", "K"],
        ["Row 3", "M", "O", "P", "Q", "S"],
        ["Row 4", "U", "V", "W", "X", "Z"]
    ]
    mat_col0_style = ParagraphStyle(
        'MatCol0',
        parent=td_center,
        fontName='Times-Bold',
        fontSize=7.8,
        textColor=colors.HexColor("#1E293B")
    )
    mat_cell_style = ParagraphStyle(
        'MatCell',
        parent=td_center,
        fontName='Times-Bold',
        fontSize=8.5,
        textColor=colors.HexColor("#0F172A")
    )
    matrix_data = []
    for r_idx, row in enumerate(matrix_raw):
        p_row = []
        for c_idx, val in enumerate(row):
            if r_idx == 0:
                p_row.append(Paragraph(val, th_style))
            elif c_idx == 0:
                p_row.append(Paragraph(f"<b>{val}</b>", mat_col0_style))
            else:
                p_row.append(Paragraph(f"<b>{val}</b>", mat_cell_style))
        matrix_data.append(p_row)

    t_mat = Table(matrix_data, colWidths=[1.15*inch]*6)
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor("#EAEEF4")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (1, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 5))

    # Deliverable 4: Challenge Dataset Table (Wrapped & Spaced Ciphertexts)
    story.append(Paragraph("<b>Deliverable 4 – Standardized Challenge Dataset (10 Plaintext-Ciphertext Pairs):</b>", sub_heading))
    challenge_raw = [
        ["#", "Plaintext (Input)", "Ciphertext (Output)", "Len", "True Status"],
        ["1", "DEFEND THE PERIMETER AT ONCE", "MJEDKEZZENDOEKXNLBKMOGIT", "24", "GENUINE"],
        ["2", "ZERO TRUST ARCHITECTURE SECURES DATA", "RAYQHYRJRVVYXJFFSZIKYVFWMLERYPRF", "32", "GENUINE"],
        ["3", "CRYPTOGRAPHIC PROTOCOL FAILURE DETECTED", "JPZOVNCVEJVBCASSAEWRNMGWMUUNSPRJTKDH", "36", "POISONED (Tampered)"],
        ["4", "INCIDENT RESPONSE TEAM ENGAGED IMMEDIATELY", "ASGLLALEAIFEOCGKQEUNOZZHGWGGHBSHPOZQWRQR", "40", "GENUINE"],
        ["5", "QUANTUM COMPUTING THREATENS TRADITIONAL RSA", "ERLCCEKFEXFKXOZENYJJXMJNDBFEQXLRQXZDVQQP", "40", "GENUINE"],
        ["6", "MALWARE EXFILTRATING SENSITIVE AUDIT LOGS", "STSZRXYSLOWHSIDBYYQDUZXXIZHXAZPQTPYPMY", "38", "POISONED (Tampered)"],
        ["7", "FIREWALL BLOCKS UNTRUSTED NETWORK TRAFFIC", "AIYIHRQROITACREZSKUYMAANPQZENDJGNNEZPRJL", "40", "GENUINE"],
        ["8", "AUTHENTICATION TOKEN EXPIRES SOON REFRESH", "CQFAKKZKHVABOCFPQUNNAHXUPWGSRGEONMIRTQ", "38", "GENUINE"],
        ["9", "DENIAL OF SERVICE ATTACK FLOODS ROUTER", "MJRLGXHBAWTNSUGNHYWACVYKWCGHPKQZCALF", "36", "POISONED (Tampered)"],
        ["10", "ELLIPTIC CURVE DIGITAL SIGNATURE STANDARD", "HIGBLSFFPQTNOMZDSEKZMXZQONTOBVRFQKZOQY", "38", "GENUINE"]
    ]
    challenge_data = []
    for r_idx, row in enumerate(challenge_raw):
        p_row = []
        for c_idx, val in enumerate(row):
            if r_idx == 0:
                p_row.append(Paragraph(val, th_style))
            elif c_idx == 0:
                p_row.append(Paragraph(val, td_center))
            elif c_idx == 1:
                p_row.append(Paragraph(val, td_style))
            elif c_idx == 2:
                # Chunked into groups of 4 for natural wrapping without collision!
                p_row.append(Paragraph(chunk_cipher(val, 4), td_code))
            elif c_idx == 3:
                p_row.append(Paragraph(val, td_center))
            elif c_idx == 4:
                if "POISONED" in val:
                    p_row.append(Paragraph(val, td_danger))
                else:
                    p_row.append(Paragraph(val, td_success))
        challenge_data.append(p_row)

    t_chal = Table(challenge_data, colWidths=[0.35*inch, 2.25*inch, 2.55*inch, 0.45*inch, 1.3*inch])
    t_chal.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_chal)
    story.append(Spacer(1, 5))

    # Deliverable 5: Walkthrough Trace Table (Wrapped)
    story.append(Paragraph("<b>Deliverable 5 – Step-by-Step Transformation Trace (Pair #1):</b>", sub_heading))
    trace_raw = [
        ["Processing Stage", "Intermediate State", "Cryptographic Purpose"],
        ["Raw Input", "DEFEND THE PERIMETER AT ONCE", "Original plaintext security payload."],
        ["Digraph Preparation", "DE FE ND TH EP ER IM ET ER AT ON CE", "Stripped whitespace, 12 digram blocks."],
        ["Tier 1: Playfair Matrix", "EF GF IE HC FO KA DU FN KA BN VE NK", "Digraphic substitution (flattens unigrams)."],
        ["Tier 2: Vigenère Stream", "ZF RN IR AX FZ SA QN AN VI BA OZ NV", "Polyalphabetic keystream masks symmetries."],
        ["Tier 3A: Digraph Inversion", "FZ RN RI AX ZF SA NQ AN IV BA ZO NV", "Alternating Parity Inversion on even blocks."],
        ["Tier 3B: Dynamic Drift", "MJ ED KE ZZ EN DO EK XN LB KM OG IT", "Affine Drift Δ(i) = (3i + 7) mod 26."],
        ["Final Ciphertext", "MJEDKEZZENDOEKXNLBKMOGIT", "Transmitted challenge ciphertext (Length 24)."]
    ]
    trace_data = []
    for r_idx, row in enumerate(trace_raw):
        p_row = []
        for c_idx, val in enumerate(row):
            if r_idx == 0:
                p_row.append(Paragraph(val, th_style))
            elif c_idx == 0:
                p_row.append(Paragraph(val, td_bold))
            elif c_idx == 1:
                p_row.append(Paragraph(val, td_code))
            else:
                p_row.append(Paragraph(val, td_style))
        trace_data.append(p_row)

    t_trace = Table(trace_data, colWidths=[1.6*inch, 3.1*inch, 2.2*inch])
    t_trace.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_trace)
    story.append(PageBreak())

    # =========================================================
    # SECTION 4: BENCHMARKS & COMPLEXITY
    # =========================================================
    story.append(Paragraph("3. Performance Metrics and Empirical Complexity", section_heading))
    story.append(Paragraph(
        "Measured with cca_benchmark.py (best of 50 runs on one development machine; absolute times vary by hardware) for payload sizes from <i>N</i> = 100 to 10,000 characters. The challenge ciphertexts have an Index of Coincidence of 0.0388, against 0.0385 for uniform random text and 0.0688 for the plaintexts (also from cca_benchmark.py).",
        body_style
    ))

    bench_raw = [
        ["Payload Length (N)", "KTCC Encrypt (ms)", "KTCC Decrypt (ms)", "Caesar Shift (ms)", "Overhead Factor", "Throughput (chars/s)"],
        ["100 chars", "0.124 ms", "0.099 ms", "0.021 ms", "5.9×", "824,576 chars/s"],
        ["1,000 chars", "1.208 ms", "0.962 ms", "0.190 ms", "6.4×", "844,091 chars/s"],
        ["10,000 chars", "11.805 ms", "9.273 ms", "1.770 ms", "6.7×", "865,425 chars/s"]
    ]
    bench_data = []
    for r_idx, row in enumerate(bench_raw):
        p_row = []
        for c_idx, val in enumerate(row):
            if r_idx == 0:
                p_row.append(Paragraph(val, th_style))
            else:
                p_row.append(Paragraph(val, td_center))
        bench_data.append(p_row)

    t_bench = Table(bench_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.1*inch, 1.0*inch, 1.2*inch])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<b>Asymptotic Scaling:</b> Time complexity is strictly linear <i>O(N)</i> across all three stages (Playfair: <i>N/2</i> lookups; Vigenère: <i>N</i> modular shifts; ADI-PDD: <i>N/4</i> swaps and <i>N</i> affine operations). Memory is <i>O(N)</i> with constant <i>O(1)</i> matrix storage.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # =========================================================
    # SECTIONS 4-5: shared content from report_inputs.py
    # =========================================================
    def lead_par(text):
        head, sep, rest = text.partition(": ")
        if sep and len(head) < 30:
            return Paragraph(f"<b>{escape(head)}:</b> {escape(rest)}", body_style)
        return Paragraph(escape(text), body_style)

    def grid(rows, widths):
        data = [[Paragraph(escape(c), th_style if r == 0 else (td_bold if i == 0 else td_style))
                 for i, c in enumerate(row)] for r, row in enumerate(rows)]
        t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
        ]))
        return t

    def titled_grid(title, rows, widths, intro=None):
        parts = [Paragraph(f"<b>{escape(title)}</b>", sub_heading)] + ([lead_par(intro)] if intro else [])
        story.append(KeepTogether(parts + [grid(rows, widths), Spacer(1, 5)]))

    story.append(Paragraph(ri.S5_TITLE, section_heading))
    story.append(Paragraph(escape(ri.S5_INTRO), body_style))
    titled_grid("Stage-by-stage rationale", ri.STAGE_ROWS, [1.3, 1.9, 1.75, 1.95])
    titled_grid("Keyspace", ri.KEYSPACE_ROWS, [2.0, 1.9, 1.5, 1.5])
    story.append(lead_par(ri.S5_AFFINE))
    titled_grid("Flaw signatures of the challenge pairs", ri.FLAW_ROWS, [0.5, 0.9, 2.9, 1.3, 1.3], intro=ri.S5_FLAWS)
    story.append(lead_par(ri.S5_ASSESSMENT))
    story.append(Spacer(1, 6))

    story.append(Paragraph(ri.S6_TITLE, section_heading))
    titled_grid("Contributions", ri.CONTRIBUTION_ROWS, [1.8, 1.0, 4.1])
    titled_grid("Resource log", ri.RESOURCE_ROWS, [2.4, 4.5])
    for p in ri.S6_PARAGRAPHS:
        story.append(lead_par(p))
    story.append(PageBreak())

    # =========================================================
    # SECTION 6: SUGGESTIONS FOR IMPROVEMENT
    # =========================================================
    story.append(Paragraph("6. Suggestions for Improving the Cipher's Security", section_heading))
    story.append(Paragraph(
        "<b>Known limitation:</b> Tiers 2 and 3 only add position-dependent shifts plus a fixed swap, so together they act as one fixed keystream. With the Playfair matrix and a few known pairs, that keystream can be read off directly. Suggestions 1 and 3 make the keystream depend on the plaintext instead of being fixed, which weakens this attack; Suggestion 2 targets the linear structure itself. To raise KTCC resilience without increasing asymptotic complexity:",
        body_style
    ))

    # DISTINCT NUMBERED ITEMS ON SEPARATE LINES
    story.append(Paragraph(
        "<b>1. Dynamic Autokey Keystream Scheduling:</b> Replace the periodic repeating Vigenère key with an autokey mechanism (<i>K[i] = P[i - L<sub>V</sub>]</i>) to eliminate keystream periodicity and defeat Kasiski autocorrelation.",
        numbered_style
    ))
    story.append(Paragraph(
        "<b>2. Non-Linear S-Box Permutation:</b> Insert an 8-bit non-linear substitution box between Tier 2 and Tier 3 to break linear modular arithmetic over <i>Z</i><sub>26</sub>, preventing modular equation solvers from decoupling the stages.",
        numbered_style
    ))
    story.append(Paragraph(
        "<b>3. Cipher Block Chaining (CBC) Feedback:</b> Modularly add previous ciphertext digraphs into current plaintext digraphs (<i>P'[b] = (P[b] + C[b-1]) mod 26</i>) to eliminate identical ciphertext outputs for repeating phrases.",
        numbered_style
    ))
    story.append(Paragraph(
        "<b>4. Expanded 6x6 Matrix Alphabet:</b> Expand the Playfair grid to 6x6 (36 alphanumeric cells: A–Z and 0–9) to eliminate the 'I'/'J' merger and allow native encryption of IP addresses and cryptographic tokens.",
        numbered_style
    ))
    story.append(Spacer(1, 5))

    # =========================================================
    # SECTION 6: CODE SUBMISSION & EXECUTION DETAILS
    # =========================================================
    story.append(Paragraph("7. Code Submission & Execution Details", section_heading))
    story.append(Paragraph(
        "All project source files and automated test suites are publicly hosted on GitHub at: <b><u>https://github.com/ameemakhtr/NIS_CCA</u></b>",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Execution Commands Box
    cmd_lines = (
        "<b># Automated Execution & Verification Commands</b><br/>"
        "python cca_main.py --blue &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Show cipher design and challenge dataset<br/>"
        f"python test_cca.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Run automated unit test suite ({TEST_COUNT}/{TEST_COUNT} tests passing)<br/>"
        "python cca_analysis.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Post-challenge resistance analysis (Section 4)<br/>"
        "python build_report_pdf.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Recompile publication-grade PDF report<br/>"
        "python build_report_docx.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Recompile publication-grade Word DOCX report"
    )
    t_cmd = Table([[Paragraph(f"<font face='Courier' size=7.2>{cmd_lines}</font>", body_style)]], colWidths=[6.9*inch])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 5))

    # =========================================================
    # SECTION 7: REFERENCES
    # =========================================================
    story.append(Paragraph("8. Academic References", section_heading))
    refs = [
        "1. Al-Kindi, Abu Yusuf Ya'qub ibn Ishaq (c. 850 CE). <i>Risalah fi Istikhraj al-Mu'amma</i> (Manuscript on Deciphering Cryptographic Messages). House of Wisdom, Baghdad.",
        "2. Shannon, Claude E. (1949). 'Communication Theory of Secrecy Systems.' <i>Bell System Technical Journal</i>, 28(4), 656–715.",
        "3. Friedman, William F. (1922). <i>The Index of Coincidence and Its Applications in Cryptography</i>. Department of Ciphers, Publication No. 22, Riverbank Laboratories.",
        "4. Stallings, William (2020). <i>Cryptography and Network Security: Principles and Practice</i> (8th Edition). Pearson Education.",
        "5. Wheatstone, Charles & Playfair, Lyon (1854). 'On the Playfair System of Cipher.' <i>Minutes of the Royal Society of Arts</i>, London.",
        "6. Vigenère, Blaise de (1586). <i>Traicté des Chiffres ou Secrètes Manières d'Escrire</i>. Paris, France."
    ]
    for ref in refs:
        story.append(Paragraph(ref, bullet_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Publication-grade PDF successfully built: {pdf_path}")
    ri.sync_markdown()
    ri.warn_placeholders("build_report_pdf.py")


if __name__ == "__main__":
    build_cca_pdf()
