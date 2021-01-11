
from lib.htmlephant import (
    HTMLElement,
    Img,
)

class _Picture(HTMLElement):
    TAG_NAME = 'picture'

class Source(HTMLElement):
    TAG_NAME = 'picture'
    REQUIRED_ATTRS = ('srcset',)

def Picture(context, base_fn, alt):
    return (
        _Picture(
            children=(
                Source(srcset=context._static(f'{base_fn}.webp')),
                Img(src=context._static(f'{base_fn}.png'), alt=alt)
            )
        ),
    )
