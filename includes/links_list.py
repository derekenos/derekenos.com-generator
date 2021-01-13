
from lib import NotDefined
from lib.htmlephant import (
    Anchor,
    Li,
    Ol,
)

Head = NotDefined

Body = lambda context, name_href_pairs: (
    Ol(
        children=[
            Li(
                children=(
                    Anchor(name, href=href),
                )
            )
            for name, href in name_href_pairs
        ]
    ),
)
