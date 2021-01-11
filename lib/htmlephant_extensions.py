
from .htmlephant import HTMLElement

class Nav(HTMLElement):
    TAG_NAME = 'nav'

class Picture(HTMLElement):
    TAG_NAME = 'picture'

class Source(HTMLElement):
    TAG_NAME = 'picture'
    REQUIRED_ATTRS = ('srcset',)
