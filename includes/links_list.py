
from lib import NotDefined
from lib import microdata as md
from lib.htmlephant import (
    Anchor,
    Li,
    Ol,
    Span,
)

Head = NotDefined

Body = lambda context, itemprop, itemtype, name_url_pairs: (
    Ol(
        _class='links',
        children=[
            Li(
                itemprop=itemprop,
                itemscope='',
                itemtype=itemtype,
                children=(
                    Anchor(
                        itemprop=md.URL,
                        href=url,
                        children=(
                            Span(name, itemprop=md.NAME),
                        )
                    ),
                )
            )
            for name, url in name_url_pairs
        ]
    ),
)
