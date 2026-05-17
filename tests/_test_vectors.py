import dataclasses
from typing import List


@dataclasses.dataclass(frozen=True, kw_only=True)
class FileTestVector:
    filename: str
    must_include: List[str]
    must_not_include: List[str] = dataclasses.field(default_factory=list)


TEST_VECTORS = [
    FileTestVector(
        filename="test.docx",
        must_include=[
            # Heading level preserved
            "# DOCX-HEADING-a1b2c3d4",
            # Plain paragraph preserved
            "DOCX-PARA-e5f6g7h8",
            # Inline formatting preserved — these would fail if bold/italic were stripped
            "**DOCX-BOLD-i9j0k1l2**",
            "*DOCX-ITALIC-m3n4o5p6*",
            # Table rendered as markdown pipes — would fail if table became plain text
            "| DOCX-TH-COL1 | DOCX-TH-COL2 | DOCX-TH-COL3 |",
            "| DOCX-TD-R1C1 | DOCX-TD-R1C2 | DOCX-TD-R1C3 |",
        ],
        must_not_include=[
            # Raw XML must never leak into output
            "<w:t>",
            "<w:p>",
        ],
    ),
    FileTestVector(
        filename="test.xlsx",
        must_include=[
            # Sheet name rendered as heading
            "## XLSX-SHEET-q7r8s9t0",
            # Merged header value present — exact pipe-row checked in regression test
            "XLSX-MERGED-HEADER",
            # Data rows rendered as markdown pipes — would fail if rows became plain text
            "| XLSX-TH-COL1 | XLSX-TH-COL2 | XLSX-TH-COL3 |",
            "| XLSX-TD-u1v2w3 | XLSX-TD-x4y5z6 | XLSX-TD-a7b8c9 |",
        ],
    ),
    FileTestVector(
        filename="test.pptx",
        must_include=[
            # Slide title rendered as H1 — would fail if title lost its heading marker
            "# PPTX-TITLE-d0e1f2g3",
            # Body text preserved
            "PPTX-BODY-h4i5j6k7",
            # Content from slide 2 must be present — would fail if only slide 1 was read
            "PPTX-SLIDE2-l8m9n0o1",
        ],
        must_not_include=[
            # Raw XML must never appear
            "<p:sp>",
        ],
    ),
    FileTestVector(
        filename="test.pdf",
        must_include=[
            # Content from page 1
            "PDF-HEADING-p2q3r4s5",
            "PDF-PARA-t6u7v8w9",
            # Content from page 2 — would fail if only the first page was read
            "PDF-PAGE2-x0y1z2a3",
        ],
    ),
]
