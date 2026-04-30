from lib import (
    NotDefined,
    microdata as md,
)

from lib.htmlephant import (
    MDMeta,
    NOEL,
    Audio,
    Br,
    Hn,
    Paragraph,
)

Head = NotDefined

Body = lambda context, src, name, description, h_level, itemprop=None: (
    Hn[h_level](name),
    Paragraph(description),
    Br(),
    Audio(
        itemprop=itemprop,
        itemscope="",
        itemtype=md.Types.AudioObject,
        children=(
            MDMeta(md.Props.contentUrl, src),
            MDMeta(md.Props.name, name),
            MDMeta(md.Props.description, description),
        ),
        controls="",
        src=src,
    ),
)
