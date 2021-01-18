
from lib import NotDefined
from lib import microdata as md
from lib.htmlephant_extensions import (
    UnescapedH4,
    UnescapedParagraph,
)

from . import collection

Head = NotDefined

Body = lambda context, items: collection.Body(
    context,
    itemtype=md.INTANGIBLE,
    items=[
        [
            UnescapedH4(name, itemprop=md.NAME),
            UnescapedParagraph(text, itemprop=md.DESCRIPTION)
        ]
        for name, text in items
    ]
)
