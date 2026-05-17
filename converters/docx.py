from typing import BinaryIO
from docx import Document
from docx.oxml.ns import qn
from .base import BaseConverter, ConversionResult
from .math.omml import oMath2Latex, OMML_NS

_HEADING_MAP = {
    "Heading 1": "#",
    "Heading 2": "##",
    "Heading 3": "###",
    "Heading 4": "####",
    "Heading 5": "#####",
    "Heading 6": "######",
}

_W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_W_R = _W_NS + "r"
_W_T = _W_NS + "t"
_W_RPR = _W_NS + "rPr"
_W_B = _W_NS + "b"
_W_I = _W_NS + "i"
_W_HYPERLINK = _W_NS + "hyperlink"
_M_OMATH = OMML_NS + "oMath"
_M_OMATPARA = OMML_NS + "oMathPara"


class DocxConverter(BaseConverter):
    def accepts(self, extension: str) -> bool:
        return extension.lower() == ".docx"

    def convert(self, stream: BinaryIO) -> ConversionResult:
        doc = Document(stream)
        parts = []

        for block in _iter_blocks(doc):
            if block["type"] == "paragraph":
                text = _render_paragraph(block["element"])
                if text:
                    parts.append(text)
            elif block["type"] == "table":
                md = _render_table(block["element"])
                if md:
                    parts.append(md)
        return ConversionResult(markdown="\n\n".join(parts))


def _iter_blocks(doc):
    """Yield paragraphs and tables in document order."""
    body = doc.element.body
    for child in body:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag == "p":
            from docx.text.paragraph import Paragraph
            yield {"type": "paragraph", "element": Paragraph(child, doc)}
        elif tag == "tbl":
            from docx.table import Table
            yield {"type": "table", "element": Table(child, doc)}


def _render_omath_para(el) -> str:
    """Render a block-level <m:oMathPara> element as $$...$$ LaTeX."""
    parts = []
    for omath in el.findall(_M_OMATH):
        try:
            latex = oMath2Latex(omath).latex
            if latex.strip():
                parts.append(f"$${latex}$$")
        except Exception:
            pass
    return "\n".join(parts)


def _render_paragraph(para) -> str:
    style = para.style.name if para.style else ""
    prefix = _HEADING_MAP.get(style, "")

    inline = _render_inline(para)
    if not inline.strip():
        return ""

    return f"{prefix} {inline}".strip() if prefix else inline


def _render_inline(para) -> str:
    """Render paragraph inline content, handling both text runs and inline equations."""
    parts = []
    for child in para._element:
        if child.tag == _W_R:
            text = _run_element_to_md(child)
            if text:
                parts.append(text)
        elif child.tag == _W_HYPERLINK:
            # Recurse into hyperlink runs
            for sub in child:
                if sub.tag == _W_R:
                    text = _run_element_to_md(sub)
                    if text:
                        parts.append(text)
        elif child.tag == _M_OMATH:
            try:
                latex = oMath2Latex(child).latex
                if latex.strip():
                    parts.append(f"${latex}$")
            except Exception:
                pass
        elif child.tag == _M_OMATPARA:
            for omath in child.findall(_M_OMATH):
                try:
                    latex = oMath2Latex(omath).latex
                    if latex.strip():
                        parts.append(f"$${latex}$$")
                except Exception:
                    pass
    return "".join(parts)


def _run_element_to_md(r_el) -> str:
    """Extract text from a <w:r> element and apply bold/italic markdown."""
    t_el = r_el.find(_W_T)
    if t_el is None or not t_el.text:
        return ""
    text = t_el.text
    rPr = r_el.find(_W_RPR)
    bold = rPr is not None and rPr.find(_W_B) is not None
    italic = rPr is not None and rPr.find(_W_I) is not None
    if bold and italic:
        return f"***{text}***"
    elif bold:
        return f"**{text}**"
    elif italic:
        return f"*{text}*"
    return text


def _render_table(table) -> str:
    rows = table.rows
    if not rows:
        return ""

    def cell_text(cell):
        return " ".join(p.text for p in cell.paragraphs).replace("|", "\\|").replace("\n", " ")

    header = [cell_text(c) for c in rows[0].cells]
    lines = []
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(cell_text(c) for c in row.cells) + " |")

    return "\n".join(lines)
