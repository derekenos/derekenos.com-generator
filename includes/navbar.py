
from lib import (
    NotDefined,
    assert_ctx,
)

from lib.htmlephant import (
    Anchor,
    Div,
    Li,
    Nav,
    Ol,
    Span,
)

def _Li(context, name, label):
    if name == context.current_page:
        return Li(label, _class='current')
    if name == 'index':
        name = ''
    return Li(children=(Anchor(label, href=f'/{name}'),))

Head = NotDefined

def Body(context):
    assert_ctx(context, 'navbar_page_name_label_pairs')
    nav = Nav(
        children=[
            Ol(
                children=[
                    _Li(context, name, label)
                    for name, label in context.navbar_page_name_label_pairs
                ]
            )
        ]
    )

    # Extend with any page module sub-navigation elements.
    if hasattr(context.current_page_mod, 'Nav'):
        nav.children.extend(context.current_page_mod.Nav(context))

    return (nav,)
