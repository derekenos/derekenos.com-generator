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
        itemtype=md.IMAGE_OBJECT,
        children=(
            MDMeta(md.CONTENT_URL, src),
            MDMeta(md.THUMBNAIL_URL, src),
            MDMeta(md.NAME, name),
            MDMeta(md.DESCRIPTION, description),
            MDMeta(
                md.ENCODING_FORMAT,
                type:=type or mimetypes.guess_type(src)[0]
            ),
            MDMeta(md.UPLOAD_DATE, upload_date),
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
