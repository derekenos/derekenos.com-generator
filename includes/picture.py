"""https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture
"""

import mimetypes

from lib import NotDefined
from lib import microdata as md
from lib.htmlephant import (
    Img,
    MDMeta,
    Picture,
    PictureSource,
    Span,
)

def get_srcset_mimetype(srcset):
    first_src = srcset.split(',')[0].split(' ')[0]
    # Hack in support for webp.
    if first_src.endswith('.webp'):
        return 'image/webp'
    return mimetypes.guess_type(first_src)[0]

Head = NotDefined

def Body(
        context,
        srcsets,
        sizes,
        name,
        description,
        upload_date,
        itemprop=None
    ):
    # Use the first item in the last srcset as the fallback image.
    src = srcsets[-1].split(',')[0].split(' ')[0]
    return (
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
                    mimetypes.guess_type(src)[0]
                ),
                MDMeta(md.Props.uploadDate, upload_date),
                Picture(
                    children=(
                        *[
                            PictureSource(
                                srcset=srcset,
                                sizes=sizes,
                                type=get_srcset_mimetype(srcset)
                            )
                            for srcset in srcsets
                        ],
                        Img(src=src, alt=description),
                    )
                )
            )
        ),
    )
