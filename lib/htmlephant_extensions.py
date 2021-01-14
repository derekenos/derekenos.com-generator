
from .htmlephant import HTMLElement

class Nav(HTMLElement):
    TAG_NAME = 'nav'

class Picture(HTMLElement):
    TAG_NAME = 'picture'

class Source(HTMLElement):
    TAG_NAME = 'source'
    REQUIRED_ATTRS = ('srcset',)

class Link(HTMLElement):
    TAG_NAME='link'
    REQUIRED_ATTRS = ('href', 'rel')

class Em(HTMLElement):
    TAG_NAME = 'em'
