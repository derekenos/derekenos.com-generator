
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
    if name.endswith('-generator'):
        is_current = context.current_page.startswith(name[:-9])
        url = f'/{name[:-10]}s'
    else:
        is_current = name == context.current_page
        url = f'/{"" if name == "index" else name}'

    if is_current:
        return Li(label, _class='current')

    return Li(children=(Anchor(label, href=url),))

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
