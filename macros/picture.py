"""https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture
"""

from lib import NotDefined
from lib.htmlephant import (
    Img,
    Picture,
    Source,
)

Head = NotDefined

def Body(context, srcsets, src, alt):
    el = Picture(
        children=[
            Source(srcset=srcset) for srcset in srcsets
        ]
    )
    el.children.append(Img(src=src, alt=alt))
    return (el,)
