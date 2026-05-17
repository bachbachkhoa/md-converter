import os
from io import BytesIO
from typing import BinaryIO, Union
from pathlib import Path

from converters import PdfConverter, DocxConverter, XlsxConverter, XlsConverter, PptxConverter
from converters.base import BaseConverter, ConversionResult

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".xls", ".pptx"}


class UnsupportedFormatError(Exception):
    pass


class ConverterFacade:
    """
    Single entry point for all UI layers.
    UI code only ever calls convert() or convert_stream() — it never
    needs to know which underlying converter is used.
    """

    def __init__(self):
        self._converters: list[BaseConverter] = [
            PdfConverter(),
            DocxConverter(),
            XlsxConverter(),
            XlsConverter(),
            PptxConverter(),
        ]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def convert(self, file_path: Union[str, Path]) -> ConversionResult:
        """Convert a file on disk to a ConversionResult."""
        path = Path(file_path)
        extension = path.suffix.lower()
        self._check_supported(extension)
        with open(path, "rb") as fh:
            return self._dispatch(fh, extension)

    def convert_stream(self, stream: BinaryIO, filename: str) -> ConversionResult:
        """Convert a binary stream to a ConversionResult.

        `filename` is used only to determine the file extension.
        The stream does not need to be seekable.
        """
        extension = os.path.splitext(filename)[-1].lower()
        self._check_supported(extension)

        # Ensure seekable; if not, buffer into BytesIO (caller's stream is consumed, acceptable)
        if not hasattr(stream, "seek") or not stream.seekable():
            stream = BytesIO(stream.read())
            return self._dispatch(stream, extension)

        # Stream is seekable — restore caller's position after conversion
        original_pos = stream.tell()
        try:
            return self._dispatch(stream, extension)
        finally:
            stream.seek(original_pos)

    @staticmethod
    def supported_extensions() -> set[str]:
        return set(SUPPORTED_EXTENSIONS)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _check_supported(self, extension: str) -> None:
        if extension not in SUPPORTED_EXTENSIONS:
            raise UnsupportedFormatError(
                f"Format '{extension}' is not supported. "
                f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )

    def _dispatch(self, stream: BinaryIO, extension: str) -> ConversionResult:
        for converter in self._converters:
            if converter.accepts(extension):
                return converter.convert(stream)
        raise UnsupportedFormatError(f"No converter found for '{extension}'")
