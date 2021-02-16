"""https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture
"""

from lib import NotDefined
from lib import microdata as md
from lib.htmlephant import (
    Span,
    Img,
    MDMeta,
    Picture,
    PictureSource,
)

image_sources_to_srcset_str = lambda image_sources: ', '.join(
    f'{path} {width}w' for _, _, path, width, _, _ in image_sources
)

Head = NotDefined

Body = lambda context, sources, sizes, name, description, itemprop=None: (
    Span(
        itemprop=itemprop,
        itemscope='',
        itemtype=md.Types.ImageObject,
        _class='picture-wrapper',
        style='display: inline-block;',
        children=(
            MDMeta(md.Props.contentUrl, sources['original'].url),
            MDMeta(md.Props.thumbnailUrl, sources['fallback'].url),
            MDMeta(md.Props.name, name),
            MDMeta(md.Props.description, description),
            MDMeta(md.Props.encodingFormat, sources['original'].mimetype),
            MDMeta(
                md.Props.uploadDate,
                sources['original'].last_modified.isoformat()
            ),
            Picture(
                style=f"display: inline-block; width: 100%; height: 0; position: relative; padding-bottom: {sources['original'].height / sources['original'].width * 100}%;",
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
                    Img(
                        src=sources['fallback'].url,
                        loading='lazy',
                        alt=description,
                        style='position: absolute; top: 0; left: 0; width: 100%; height: 100%;'
                    ),
                )
            )
        )
    ),
)
