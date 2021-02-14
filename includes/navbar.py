
from lib import (
    NotDefined,
    assert_ctx,
)

from lib.htmlephant import (
    Anchor,
    Li,
    Nav,
    Ol,
)

def _Li(context, name, label):
    is_current = name == context.current_page or (
        context.current_page.endswith('_generator')
        and name == f'{context.current_page[:-10]}s'
    )
    if is_current:
        return Li(label, id='active-main-nav-tab')
    return Li(children=(Anchor(label, href=f'/{"" if name == "index" else name}'),))

Head = NotDefined

def Body(context):
    assert_ctx(context, 'navbar_page_name_label_pairs')
    nav = Nav(
        id="main-nav",
        _aria_label='primary',
        children=[
            Ol(
                children=[
                    _Li(context, name, label)
                    for name, label in context.navbar_page_name_label_pairs
                ]
            )
        ]
    )

    # If page module defines a Nav function, invoke and include its elements.
    if hasattr(context.current_page_mod, 'Nav'):
        return (
            nav,
            *context.current_page_mod.Nav(context)
        )

    return (nav,)
