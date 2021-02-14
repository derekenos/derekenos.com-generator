"""A list of links that represent a relationship between the enclosing scope
and a new scope.
"""

from lib import NotDefined
from lib import microdata as md
from lib.htmlephant import (
    Anchor,
    Li,
    Ol,
    Span,
)

Head = NotDefined

Body = lambda context, prop_type_name_url_tuples: (
    Ol(
        _class='links',
        children=[
            Li(
                itemprop=prop,
                itemscope='',
                itemtype=type,
                children=(
                    Anchor(
                        itemprop=md.Props.url,
                        href=url,
                        children=(
                            Span(
                                name,
                                itemprop=md.Props.name
                            ),
                        )
                    ),
                )
            )
            for prop, type, name, url in prop_type_name_url_tuples
        ]
    ),
)
