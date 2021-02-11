
from lib import (
    NotDefined,
    guess_mimetype,
    microdata as md,
)

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
            VideoSource(src=context.static(src), type=type),
            MDMeta(
                md.Props.contentUrl,
                context.static_url(src)
            ),
            MDMeta(
                md.Props.thumbnailUrl,
                context.static_url(poster)
            ),
            MDMeta(md.Props.name, name),
            MDMeta(md.Props.description, description),
            MDMeta(
                md.Props.encodingFormat,
                type:=type or guess_mimetype(src)
            ),
            MDMeta(md.Props.uploadDate, upload_date),
        ),
        controls='',
        poster=poster,
    )
)
