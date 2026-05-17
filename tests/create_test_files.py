"""
Run this script once to generate the test files used by the test suite.
    python tests/create_test_files.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

OUT = os.path.join(os.path.dirname(__file__), "test_files")

# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------
def make_docx():
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    doc.add_heading("DOCX-HEADING-a1b2c3d4", level=1)
    doc.add_paragraph("DOCX-PARA-e5f6g7h8")

    doc.add_heading("Section Two", level=2)
    p = doc.add_paragraph()
    p.add_run("DOCX-BOLD-i9j0k1l2").bold = True
    p.add_run(" normal ")
    p.add_run("DOCX-ITALIC-m3n4o5p6").italic = True

    table = doc.add_table(rows=2, cols=3)
    table.rows[0].cells[0].text = "DOCX-TH-COL1"
    table.rows[0].cells[1].text = "DOCX-TH-COL2"
    table.rows[0].cells[2].text = "DOCX-TH-COL3"
    table.rows[1].cells[0].text = "DOCX-TD-R1C1"
    table.rows[1].cells[1].text = "DOCX-TD-R1C2"
    table.rows[1].cells[2].text = "DOCX-TD-R1C3"

    doc.save(os.path.join(OUT, "test.docx"))
    print("Created test.docx")


# ---------------------------------------------------------------------------
# XLSX (with a merged cell)
# ---------------------------------------------------------------------------
def make_xlsx():
    import openpyxl

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "XLSX-SHEET-q7r8s9t0"

    ws["A1"] = "XLSX-MERGED-HEADER"
    ws.merge_cells("A1:C1")   # merged across 3 columns

    ws["A2"] = "XLSX-TH-COL1"
    ws["B2"] = "XLSX-TH-COL2"
    ws["C2"] = "XLSX-TH-COL3"
    ws["A3"] = "XLSX-TD-u1v2w3"
    ws["B3"] = "XLSX-TD-x4y5z6"
    ws["C3"] = "XLSX-TD-a7b8c9"

    wb.save(os.path.join(OUT, "test.xlsx"))
    print("Created test.xlsx")


# ---------------------------------------------------------------------------
# PPTX
# ---------------------------------------------------------------------------
def make_pptx():
    from pptx import Presentation
    from pptx.util import Inches, Pt

    prs = Presentation()
    layout = prs.slide_layouts[1]  # title + content

    slide1 = prs.slides.add_slide(layout)
    slide1.shapes.title.text = "PPTX-TITLE-d0e1f2g3"
    slide1.placeholders[1].text = "PPTX-BODY-h4i5j6k7"

    slide2 = prs.slides.add_slide(prs.slide_layouts[5])  # blank
    txBox = slide2.shapes.add_textbox(Inches(1), Inches(1), Inches(6), Inches(2))
    txBox.text_frame.text = "PPTX-SLIDE2-l8m9n0o1"

    prs.save(os.path.join(OUT, "test.pptx"))
    print("Created test.pptx")


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------
def make_pdf():
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)
    pdf.cell(0, 10, "PDF-HEADING-p2q3r4s5", ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, "PDF-PARA-t6u7v8w9", ln=True)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, "PDF-PAGE2-x0y1z2a3", ln=True)

    pdf.output(os.path.join(OUT, "test.pdf"))
    print("Created test.pdf")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    make_docx()
    make_xlsx()
    make_pptx()
    make_pdf()
    print("All test files created.")
