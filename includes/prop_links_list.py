"""A list of links that represent direct properties of the enclosing scope.
"""

from lib import NotDefined
from lib.htmlephant import (
    Anchor,
    Li,
    Ol
)

Head = NotDefined

Body = lambda context, prop_name_url_tuples: (
    Ol(
        _class='links',
        children=[
            Li(
                children=(
                    Anchor(
                        name,
                        itemprop=prop,
                        href=url
                    ),
                )
            )
            for prop, name, url in prop_name_url_tuples
        ]
    ),
)
