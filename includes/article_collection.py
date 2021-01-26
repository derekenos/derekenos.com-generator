
from lib import microdata as md
from lib import (
    NotDefined,
    slugify,
)

from lib.htmlephant import MDMeta
from lib.htmlephant_extensions import (
    UnescapedH4,
    UnescapedParagraph,
)

from . import collection

Head = NotDefined

Body = lambda context, name, items, wide=False: collection.Body(
    context,
    name=name,
    items=[
        [
            UnescapedH4(
                title,
                id=(id:=slugify(title)), itemprop=md.Props.name
            ),
            MDMeta(md.Props.url, context.url(f'{context.current_page}#{id}')),
            UnescapedParagraph(text, itemprop=md.Props.description)
        ]
        for title, text in items
    ],
    wide=wide
)
