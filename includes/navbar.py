
from lib import NotDefined
from lib.htmlephant_extensions import Nav
from lib.htmlephant import (
    Anchor,
    Li,
    Ol,
)

PAGE_NAME_LABEL_PAIRS = (
    ('index', 'projects'),
    ('ambitions', 'ambitions'),
)

def _Li(context, name, label):
    if name == context.current_page:
        return Li(label, _class='current')
    if name == 'index':
        name = ''
    return Li(children=(Anchor(label, href=f'/{name}'),))

Head = NotDefined

Body = lambda context: (
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
