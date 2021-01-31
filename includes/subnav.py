
from lib import NotDefined
from lib.htmlephant import (
    Anchor,
    Li,
    Nav,
    Ol,
)

Head = NotDefined

# Return a sub-navigation, assuming that the first name/url pair is the
# currently active item.
Body = lambda context, name_url_pairs: (
    Nav(
        id='sub-nav',
        _aria_labelledby="active-main-nav-tab",
        children=(
            Ol(
                children=(
                    Li(name_url_pairs[0][0]),
                    *[
                      Li(
                          children=(
                              Anchor(name, href=url),
                          )
                      )
                        for name, url in name_url_pairs[1:]
                    ]
                )
            ),
        )
    ),
)
