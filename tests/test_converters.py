"""
Run with:
    .venv\\Scripts\\pytest tests/ -v
"""
import io
import os
import pytest

from facade import ConverterFacade, UnsupportedFormatError
from tests._test_vectors import TEST_VECTORS, FileTestVector

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


# ---------------------------------------------------------------------------
# Conversion correctness
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("vector", TEST_VECTORS, ids=lambda v: v.filename)
def test_convert_local(vector: FileTestVector, facade: ConverterFacade):
    """convert(path) must include all required strings and none of the forbidden ones."""
    path = os.path.join(TEST_FILES_DIR, vector.filename)
    result = facade.convert(path)
    for expected in vector.must_include:
        assert expected in result.markdown, f"[{vector.filename}] Missing: {expected!r}"
    for forbidden in vector.must_not_include:
        assert forbidden not in result.markdown, f"[{vector.filename}] Must not contain: {forbidden!r}"


@pytest.mark.parametrize("vector", TEST_VECTORS, ids=lambda v: v.filename)
def test_convert_stream_matches_local(vector: FileTestVector, facade: ConverterFacade):
    """convert_stream() must produce identical output to convert(path).

    Both entry points go through the same converter — any divergence means
    one of the two paths has a bug (e.g. stream position not reset, missing
    stream_info hint).
    """
    path = os.path.join(TEST_FILES_DIR, vector.filename)
    result_local = facade.convert(path)
    with open(path, "rb") as fh:
        result_stream = facade.convert_stream(fh, vector.filename)
    assert result_local == result_stream, (
        f"[{vector.filename}] convert() and convert_stream() produced different output"
    )


# ---------------------------------------------------------------------------
# Stream safety
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("vector", TEST_VECTORS, ids=lambda v: v.filename)
def test_stream_position_reset_after_convert(vector: FileTestVector, facade: ConverterFacade):
    """Converters must not advance the caller's stream position.

    CLAUDE.md §5: accepts() and convert() must not change the stream position.
    """
    path = os.path.join(TEST_FILES_DIR, vector.filename)
    with open(path, "rb") as fh:
        pos_before = fh.tell()
        facade.convert_stream(fh, vector.filename)
        # The facade resets the stream for its own use, but the CALLER's
        # original position at entry should be preserved.
        assert fh.tell() == pos_before, (
            f"[{vector.filename}] Stream position changed after convert_stream()"
        )


# ---------------------------------------------------------------------------
# Facade error handling
# ---------------------------------------------------------------------------

def test_unsupported_format_raises(facade: ConverterFacade):
    """Facade must raise UnsupportedFormatError, not a bare exception, for unknown extensions."""
    with pytest.raises(UnsupportedFormatError):
        facade.convert_stream(io.BytesIO(b"irrelevant"), "file.txt")


def test_unsupported_format_error_message(facade: ConverterFacade):
    """Error message must name the offending extension so the user knows what to fix."""
    with pytest.raises(UnsupportedFormatError, match=r"\.txt"):
        facade.convert_stream(io.BytesIO(b"irrelevant"), "file.txt")


# ---------------------------------------------------------------------------
# Regression: merged cells (bug found and fixed during development)
# ---------------------------------------------------------------------------

def test_xlsx_merged_cells_fill_all_columns(facade: ConverterFacade):
    """Regression: merged cell value must appear in every column it spans.

    Before the fix (openpyxl read_only=True), only the top-left cell carried
    the value; the rest were None and rendered as empty. This test would have
    failed on the old code.
    """
    path = os.path.join(TEST_FILES_DIR, "test.xlsx")
    result = facade.convert(path)

    # The header is merged across A1:C1 — find the markdown table row
    rows_with_value = [
        line for line in result.markdown.splitlines() if "XLSX-MERGED-HEADER" in line
    ]
    assert rows_with_value, "Merged cell value not found anywhere in output"

    count = rows_with_value[0].count("XLSX-MERGED-HEADER")
    assert count == 3, (
        f"Merged cell value should appear in all 3 columns, found it {count} time(s). "
        "This likely means openpyxl was opened in read_only mode — see CLAUDE.md §12."
    )


# ---------------------------------------------------------------------------
# Regression: PPTX title identity (bug found and fixed during development)
# ---------------------------------------------------------------------------

def test_pptx_title_rendered_as_heading(facade: ConverterFacade):
    """Regression: slide title must be rendered as a markdown H1, not plain text.

    Before the fix (shape is title_shape identity comparison), the title shape
    was never matched and was output as plain text without the # prefix.
    """
    path = os.path.join(TEST_FILES_DIR, "test.pptx")
    result = facade.convert(path)

    assert "# PPTX-TITLE-d0e1f2g3" in result.markdown, (
        "Title not rendered as H1. This likely means python-pptx shape identity "
        "comparison is broken — use shape._element is title_el. See CLAUDE.md §12."
    )
    assert "PPTX-TITLE-d0e1f2g3\n" not in result.markdown.replace("# PPTX-TITLE-d0e1f2g3", ""), (
        "Title text appeared without # prefix — heading detection failed."
    )


# ---------------------------------------------------------------------------
# Regression: XLSX image extraction
# ---------------------------------------------------------------------------

def test_xlsx_image_assets_populated(facade: ConverterFacade):
    """Regression: embedded PNG must appear in result.assets under the exact expected key.

    Checks the asset key independently of the Markdown reference so that a naming
    regression is caught even if the ![]() syntax is wrong but the key is right,
    or vice versa.
    """
    path = os.path.join(TEST_FILES_DIR, "test_xlsx_with_images.xlsx")
    result = facade.convert(path)
    expected_key = "images/XLSX-IMG-SHEET-r1s2t3u4_image_1.png"
    assert expected_key in result.assets, (
        f"Expected asset key {expected_key!r} not found in result.assets. "
        "Check that ws._images is populated and image._data() succeeds."
    )


def test_xlsx_multiple_images_both_assets_present(facade: ConverterFacade):
    """Regression: two images on one sheet must produce two distinct asset keys.

    Would fail if the per-sheet counter reset between images, if the second
    image was dropped, or if both images were written under the same key.
    """
    path = os.path.join(TEST_FILES_DIR, "test_xlsx_with_multiple_images.xlsx")
    result = facade.convert(path)
    key1 = "images/XLSX-MULTI-SHEET-a1b2c3d4_image_1.png"
    key2 = "images/XLSX-MULTI-SHEET-a1b2c3d4_image_2.png"
    assert key1 in result.assets, f"First image asset {key1!r} missing from result.assets"
    assert key2 in result.assets, f"Second image asset {key2!r} missing from result.assets"
    assert len(result.assets) == 2, (
        f"Expected exactly 2 assets, got {len(result.assets)}: {list(result.assets)}"
    )
