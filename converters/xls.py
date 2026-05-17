from typing import BinaryIO
import xlrd
from .base import BaseConverter, ConversionResult


class XlsConverter(BaseConverter):
    def accepts(self, extension: str) -> bool:
        return extension.lower() == ".xls"

    def convert(self, stream: BinaryIO) -> ConversionResult:
        wb = xlrd.open_workbook(file_contents=stream.read())
        parts = []

        for sheet_name in wb.sheet_names():
            ws = wb.sheet_by_name(sheet_name)
            if ws.nrows == 0:
                continue

            rows = [ws.row_values(i) for i in range(ws.nrows)]
            parts.append(f"## {sheet_name}")
            parts.append(_rows_to_markdown(rows))

        return ConversionResult(markdown="\n\n".join(parts))


def _rows_to_markdown(rows: list) -> str:
    if not rows:
        return ""

    col_count = max(len(r) for r in rows)

    def pad(row):
        return list(row) + [""] * (col_count - len(row))

    def cell(v):
        if v is None:
            return ""
        s = str(int(v)) if isinstance(v, float) and v == int(v) else str(v)
        return s.replace("|", "\\|").replace("\n", " ")

    header = pad(rows[0])
    lines = []
    lines.append("| " + " | ".join(cell(c) for c in header) + " |")
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(cell(c) for c in pad(row)) + " |")

    return "\n".join(lines)
