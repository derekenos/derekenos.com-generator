
from lib.htmlephant import Img
from lib.htmlephant_extensions import (
    Picture as _Picture,
    Source,
)

def Picture(context, base_fn, alt):
    # base_fn is image filename without any extension. Both .webp and .png
    # variants of the file are expected to be present and will be used to set
    # source.srcset and img.src respectively.
    return (
        _Picture(
            children=(
                Source(srcset=context.static(f'{base_fn}.webp')),
                Img(src=context.static(f'{base_fn}.png'), alt=alt)
            )
        ),
    )
