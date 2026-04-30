from lib import microdata as md
from lib import (
    NotDefined,
    slugify,
)

from lib.htmlephant import MDMeta

from . import (
    audio,
    collection,
)

Head = NotDefined

Body = lambda context, name, items, h_level, wide=False: collection.Body(
    context,
    name=name,
    items=[
        audio.Body(context, src, name, description, h_level)
        for name, description, src in items
    ],
    wide=wide,
)
