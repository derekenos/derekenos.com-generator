
import mimetypes

from lib import NotDefined
from lib import microdata as md

from lib.htmlephant import (
    MDMeta,
    NOEL,
    Video,
    VideoSource,
)

Head = NotDefined

Body = lambda context, src, poster, name, description, upload_date, \
    itemprop=None, type=None: (
    Video(
        itemprop=itemprop,
        itemscope='',
        itemtype=md.Types.VideoObject,
        children=(
            VideoSource(src=src, type=type),
            MDMeta(md.Props.contentUrl, src),
            MDMeta(md.Props.thumbnailUrl, poster),
            MDMeta(md.Props.name, name),
            MDMeta(md.Props.description, description),
            MDMeta(
                md.Props.encodingFormat,
                type:=type or mimetypes.guess_type(src)[0]
            ),
            MDMeta(md.Props.uploadDate, upload_date),
        ),
        controls='',
        poster=poster,
    )
)
