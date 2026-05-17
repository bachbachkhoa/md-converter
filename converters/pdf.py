from typing import BinaryIO
import pdfplumber
from .base import BaseConverter, ConversionResult


class PdfConverter(BaseConverter):
    def accepts(self, extension: str) -> bool:
        return extension.lower() == ".pdf"

    def convert(self, stream: BinaryIO) -> ConversionResult:
        parts = []
        with pdfplumber.open(stream) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                parts.append(f"## Page {i}")

                # Extract tables first, collect their bounding boxes to exclude from text
                tables = page.extract_tables()
                table_bboxes = [t.bbox for t in page.find_tables()] if tables else []

                # Crop page to exclude table areas, then extract text
                cropped = page
                for bbox in table_bboxes:
                    cropped = cropped.outside_bbox(bbox)
                text = cropped.extract_text(x_tolerance=2, y_tolerance=2)
                if text and text.strip():
                    parts.append(text.strip())

                # Render tables as markdown
                for table in tables:
                    md_table = _table_to_markdown(table)
                    if md_table:
                        parts.append(md_table)

        return ConversionResult(markdown="\n\n".join(parts))


def _table_to_markdown(table: list) -> str:
    if not table or not table[0]:
        return ""

    col_count = max(len(row) for row in table)

    def pad(row):
        return list(row) + [""] * (col_count - len(row))

    def cell(v):
        return str(v).replace("|", "\\|").replace("\n", " ") if v is not None else ""

    header = pad(table[0])
    rows = [pad(r) for r in table[1:]]

    lines = []
    lines.append("| " + " | ".join(cell(c) for c in header) + " |")
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    for row in rows:
        lines.append("| " + " | ".join(cell(c) for c in row) + " |")

    return "\n".join(lines)
