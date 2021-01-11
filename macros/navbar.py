
from lib.htmlephant import (
    HTMLElement,
    Anchor,
    Ol,
    Li,
)

# TODO - MOVE this into htmlephant
class Nav(HTMLElement):
    TAG_NAME = 'nav'

PAGE_NAME_LABEL_PAIRS = (
    ('index', 'projects'),
    ('ambitions', 'ambitions'),
)

def _Li(context, name, label):
    if name == context.current_page:
        return Li(label, _class='current')
    return Li(children=(Anchor(label, href=f'/{name}'),))

NavBar = lambda context: (
    Nav(
        children=(
            Ol(
                children=[
                    _Li(context, name, label)
                    for name, label in PAGE_NAME_LABEL_PAIRS
                ]
            ),
        )
    ),
)
