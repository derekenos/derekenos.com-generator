
from lib import NotDefined
from lib.htmlephant import (
    Anchor,
    Div,
    Span,
)

Head = NotDefined

# Return a sub-navigation, assuming that the first name/url pair is the
# currently active item.
Body = lambda context, name_url_pairs: (
    Div(
        id='sub-nav-outer',
        children=(
            Div(
                id='sub-nav-inner',
                children=(
                    Span(name_url_pairs[0][0]),
                    *[
                        Anchor(name, href=url)
                        for name, url in name_url_pairs[1:]
                    ]
                )
            ),
        )
    ),
)
