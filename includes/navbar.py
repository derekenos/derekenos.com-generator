
from lib import (
    NotDefined,
    assert_ctx,
)

from lib.htmlephant_extensions import Nav
from lib.htmlephant import (
    Anchor,
    Div,
    Li,
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

    # Determine whether this is a specific project page.
    project = getattr(context, 'generator_item')

    # Return basic nav if this is not a project page.
    if project is None:
        return (nav,)

    # Maybe add the projects sub-navigation element.
    outer = Div(id='project-nav-outer')
    inner = Div(id='project-nav-inner')
    outer.children.append(inner)
    for i, project in enumerate(sorted(
            context.projects,
            key=lambda x: x['name'] == project['name'],
            reverse=True
        )):
        if i == 0:
            inner.children.append(
                Span(project['name'])
            )
        else:
            inner.children.append(
                Anchor(
                    project['name'],
                    href=project['slug']
                )
            )
    nav.children.append(outer)

    return (nav,)
