from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import BinaryIO


@dataclass
class ConversionResult:
    markdown: str
    assets: dict[str, bytes] = field(default_factory=dict)


class BaseConverter(ABC):
    @abstractmethod
    def accepts(self, extension: str) -> bool:
        """Return True if this converter handles the given file extension."""
        ...

    @abstractmethod
    def convert(self, stream: BinaryIO) -> ConversionResult:
        """Convert the file stream to a ConversionResult (markdown + optional asset bytes)."""
        ...
