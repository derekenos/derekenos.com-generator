"""https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture
"""

from lib import NotDefined
from lib import microdata as md
from lib.htmlephant import (
    Img,
    MDMeta,
    Picture,
    PictureSource,
    Span,
)

Head = NotDefined

import mimetypes

Body = lambda context, srcsets, src, name, description, upload_date, \
    itemprop=None, type=None: (
    Span(
        itemprop=itemprop,
        itemscope='',
        itemtype=md.Types.ImageObject,
        children=(
            MDMeta(md.Props.contentUrl, src),
            MDMeta(md.Props.thumbnailUrl, src),
            MDMeta(md.Props.name, name),
            MDMeta(md.Props.description, description),
            MDMeta(
                md.Props.encodingFormat,
                type:=type or mimetypes.guess_type(src)[0]
            ),
            MDMeta(md.Props.uploadDate, upload_date),
            Picture(
                children=(
                    *[
                        PictureSource(
                            srcset=srcset,
                            type=type
                        )
                        for srcset in srcsets
                    ],
                    Img(src=src, alt=description),
                )
            )
        )
    ),
)
