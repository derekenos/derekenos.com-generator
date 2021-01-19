
from .htmlephant import (
    H4,
    Meta,
    Paragraph,
)

# Microdata meta helper.
MDMeta = lambda k, v: Meta(itemprop=k, content=v)

class UnescapedH4(H4):
    ESCAPE_TEXT = False

class UnescapedParagraph(Paragraph):
    ESCAPE_TEXT = False
