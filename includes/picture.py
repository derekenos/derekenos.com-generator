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

srcset_to_srcset_str = lambda srcset: \
    ', '.join(f'{path} {width}w' for path, width in srcset)

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
    fallback_mimetype, (fallback_url, fallback_width) = srcsets[-1]
    return (
        Span(
            itemprop=itemprop,
            itemscope='',
            itemtype=md.Types.ImageObject,
            children=(
                MDMeta(md.Props.contentUrl, fallback_url),
                MDMeta(md.Props.thumbnailUrl, fallback_url),
                MDMeta(md.Props.name, name),
                MDMeta(md.Props.description, description),
                MDMeta(md.Props.encodingFormat, fallback_mimetype),
                MDMeta(md.Props.uploadDate, upload_date),
                Picture(
                    children=(
                        *[
                            PictureSource(
                                srcset=srcset_to_srcset_str(srcset),
                                sizes=sizes,
                                type=mimetype
                            )
                            for mimetype, srcset in srcsets[:-1]
                        ],
                        Img(src=fallback_url, alt=description),
                    )
                )
            )
        ),
    )
