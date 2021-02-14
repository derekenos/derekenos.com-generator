
from lib import (
    NotDefined,
    microdata as md,
)

from lib.htmlephant import (
    MDMeta,
    NOEL,
    Video,
    VideoSource,
)

Head = NotDefined

Body = lambda context, src, mimetype, upload_date, poster_src, name, \
    description, itemprop=None: (
    Video(
        itemprop=itemprop,
        itemscope='',
        itemtype=md.Types.VideoObject,
        children=(
            VideoSource(src=src, type=mimetype),
            MDMeta(md.Props.contentUrl, src),
            MDMeta(md.Props.thumbnailUrl, poster_src),
            MDMeta(md.Props.name, name),
            MDMeta(md.Props.description, description),
            MDMeta(md.Props.encodingFormat, mimetype),
            MDMeta(md.Props.uploadDate, upload_date),
        ),
        controls='',
        preload='none',
        poster=poster_src
    ),
)
