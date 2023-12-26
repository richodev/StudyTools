from dataclasses import dataclass, field
from pdfreader.types.content import InlineImage
from pdfreader.types.objects import Image

@dataclass
class PdfPage():
    header: str = ""
    textContent: list[str] = field(default_factory=lambda: [])
    images: list[InlineImage | Image] = field(default_factory=lambda: [])
    pageNumber: int = 0