from typing import BinaryIO
import openpyxl
from .base import BaseConverter, ConversionResult


class XlsxConverter(BaseConverter):
    def accepts(self, extension: str) -> bool:
        return extension.lower() == ".xlsx"

    def convert(self, stream: BinaryIO) -> ConversionResult:
        # read_only=False so we can access merged_cells info
        wb = openpyxl.load_workbook(stream, read_only=False, data_only=True)
        parts = []

        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            _fill_merged_cells(ws)
            rows = list(ws.iter_rows(values_only=True))
            if not rows:
                continue

            parts.append(f"## {sheet_name}")
            parts.append(_rows_to_markdown(rows))

        wb.close()
        return ConversionResult(markdown="\n\n".join(parts))


def _fill_merged_cells(ws) -> None:
    """Copy the top-left value of each merge region into every cell it covers."""
    for merge in list(ws.merged_cells.ranges):
        top_left = ws.cell(merge.min_row, merge.min_col).value
        ws.unmerge_cells(str(merge))
        for row in range(merge.min_row, merge.max_row + 1):
            for col in range(merge.min_col, merge.max_col + 1):
                ws.cell(row, col).value = top_left


def _rows_to_markdown(rows: list) -> str:
    if not rows:
        return ""

    col_count = max(len(r) for r in rows)

    def pad(row):
        return list(row) + [None] * (col_count - len(row))

    def cell(v):
        return str(v).replace("|", "\\|").replace("\n", " ") if v is not None else ""

    header = pad(rows[0])
    lines = []
    lines.append("| " + " | ".join(cell(c) for c in header) + " |")
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(cell(c) for c in pad(row)) + " |")

    return "\n".join(lines)
