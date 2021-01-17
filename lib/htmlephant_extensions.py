
from .htmlephant import (
    HTMLElement,
    H2,
    Meta,
    Paragraph,
)

class Nav(HTMLElement):
    TAG_NAME = 'nav'

class Picture(HTMLElement):
    TAG_NAME = 'picture'

class Source(HTMLElement):
    IS_VOID = True
    TAG_NAME = 'source'
    REQUIRED_ATTRS = ('srcset',)

class Link(HTMLElement):
    IS_VOID = True
    TAG_NAME='link'
    REQUIRED_ATTRS = ('href', 'rel')

class Em(HTMLElement):
    TAG_NAME = 'em'

class Section(HTMLElement):
    TAG_NAME = 'section'

class UnescapedH4(H2):
    ESCAPE_TEXT = False

class UnescapedParagraph(Paragraph):
    ESCAPE_TEXT = False

StdMeta = lambda k, v: Meta(name=k, content=v)
OGMeta = lambda k, v: Meta(property=f'og:{k}', content=v)
