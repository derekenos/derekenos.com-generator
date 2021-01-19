
from lib import microdata as md
from lib import (
    NotDefined,
    slugify,
)
from lib.htmlephant_extensions import (
    MDMeta,
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
            UnescapedH4(title, id=(id:=slugify(title)), itemprop=md.NAME),
            MDMeta(md.URL, context.url(f'{context.current_page}#{id}')),
            UnescapedParagraph(text, itemprop=md.DESCRIPTION)
        ]
        for title, text in items
    ],
    wide=wide
)
