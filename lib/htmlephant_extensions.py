
from .htmlephant import (
    H4,
    Paragraph,
)

class UnescapedH4(H4):
    ESCAPE_TEXT = False

class UnescapedParagraph(Paragraph):
    ESCAPE_TEXT = False
