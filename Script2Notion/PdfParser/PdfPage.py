from dataclasses import dataclass, field
from PIL.Image import Image

@dataclass
class PdfPage():
    header: str = ""
    textContent: list[str] = field(default_factory=lambda: [])
    images: list[Image] = field(default_factory=lambda: [])
    pageNumber: int = 0