"""
Compatibility Wrapper for CT-486 CCA Report Generator
Delegates to build_report_pdf.py to generate publication-grade PDF reports.
"""

from build_report_pdf import build_cca_pdf

if __name__ == "__main__":
    build_cca_pdf("CCA_REPORT.pdf")
