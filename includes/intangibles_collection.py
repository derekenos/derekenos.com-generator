
from lib import NotDefined
from lib.htmlephant_extensions import (
    UnescapedH4,
    UnescapedParagraph,
)

from . import collection

Head = NotDefined

Body = lambda context, items: collection.Body(
    context,
    itemtype='https://schema.org/Intangible',
    items=[
        [
            UnescapedH4(name, itemprop='name'),
            UnescapedParagraph(text, itemprop='description')
        ]
        for name, text in items
    ]
)
