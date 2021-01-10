
from lib.htmlephant import (
    HTMLElement,
    Ol,
    Li,
)

# TODO - MOVE this into htmlephant
class Nav(HTMLElement):
    TAG_NAME = 'nav'

Head = lambda context: ()

Body = lambda context: (
    Nav(
        children=(
            Ol(
                children=[
                    Li(page_name)
                    for page_name in context['page_names']
                ]
            ),
        )
    ),
)
