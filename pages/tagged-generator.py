
from itertools import chain

from lib import microdata as md
from lib.htmlephant import (
    NOEL,
    Anchor,
    Div,
    H1,
    MDMeta,
    OGMeta,
    Span,
    StdMeta,
    Title,
)

from includes import (
    collection,
    project_card,
)

CONTEXT_ITEMS_GETTER = lambda context: \
    set(chain(*[project['tags'] for project in context.projects]))
FILENAME_GENERATOR = lambda tag: f'tagged-{tag}.html'

def Head(context):
    return (
        Title(f'{context.name} | #{context.generator_item}'),
    )

def Nav(context):
    # Add the tags sub-navigation.
    outer = Div(id='sub-nav-outer')
    inner = Div(id='sub-nav-inner')
    outer.children.append(inner)
    current_tag = context.generator_item
    tags = set(chain(*[project['tags'] for project in context.projects]))
    for i, tag in enumerate(sorted(
            tags,
            key=lambda x: x == current_tag,
            reverse=True
    )):
        if i == 0:
            inner.children.append(
                Span(f'#{tag}')
            )
        else:
            inner.children.append(
                Anchor(
                    f'#{tag}',
                    href=f'/tagged-{tag}'
                )
            )
    return (outer,)


Body = lambda context: (
    Div(
        _class='content projects',
        children=(
            H1(desc:=f'Projects Tagged #{(tag:=context.generator_item)}'),
            *collection.Body(
                context,
                name=desc,
                items=[
                    project_card.Body(context, **project)
                    for project in context.projects
                    if tag in project['tags']
                ]
            )
        )
    ),
)
