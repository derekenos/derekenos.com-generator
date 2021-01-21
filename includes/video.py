
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
        "Your browser does not support HTML5 video.",
        itemprop=itemprop,
        itemscope='',
        itemtype=md.VIDEO_OBJECT,
        children=(
            MDMeta(md.CONTENT_URL, src),
            MDMeta(md.THUMBNAIL_URL, poster),
            MDMeta(md.NAME, name),
            MDMeta(md.DESCRIPTION, description),
            MDMeta(
                md.ENCODING_FORMAT,
                type:=type or mimetypes.guess_type(src)[0]
            ),
            MDMeta(md.UPLOAD_DATE, upload_date),
            VideoSource(src=src, type=type),
        ),
        controls='',
        poster=poster,
    )
)
