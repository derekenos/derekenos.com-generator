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

image_sources_to_srcset_str = lambda image_sources: \
    ', '.join(f'{path} {width}w' for _, _, path, width in image_sources)

Head = NotDefined

Body = lambda context, sources, sizes, name, description, upload_date, \
    itemprop=None: (
    Span(
        itemprop=itemprop,
        itemscope='',
        itemtype=md.Types.ImageObject,
        children=(
            MDMeta(
                md.Props.contentUrl,
                context.static_url(sources['original'].filename)
            ),
            MDMeta(
                md.Props.thumbnailUrl,
                context.static_url(sources['fallback'].filename)
            ),
            MDMeta(md.Props.name, name),
            MDMeta(md.Props.description, description),
            MDMeta(md.Props.encodingFormat, sources['original'].mimetype),
            MDMeta(md.Props.uploadDate, upload_date),
            Picture(
                children=(
                    *[
                        PictureSource(
                            srcset=image_sources_to_srcset_str(
                                image_sources
                            ),
                            sizes=sizes,
                            type=mimetype
                        )
                        for mimetype, image_sources in sources['derivatives']
                    ],
                    Img(src=sources['fallback'].url, alt=description),
                )
            )
        )
    ),
)
