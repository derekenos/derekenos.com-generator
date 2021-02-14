
from .htmlephant import (
    HTMLElement,
    H4,
    Paragraph,
)

class Footer(HTMLElement):
    TAG_NAME = 'footer'

class Main(HTMLElement):
    TAG_NAME = 'main'

class Header(HTMLElement):
    TAG_NAME = 'header'

class UnescapedH4(H4):
    ESCAPE_TEXT = False

class UnescapedParagraph(Paragraph):
    ESCAPE_TEXT = False
