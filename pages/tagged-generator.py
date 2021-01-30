
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
    subnav,
)

CONTEXT_ITEMS_GETTER = lambda context: \
    set(chain(*[project['tags'] for project in context.projects]))
FILENAME_GENERATOR = lambda tag: f'tagged-{tag}.html'

slugify = lambda tag: f'/{FILENAME_GENERATOR(tag).rsplit(".", 1)[0]}'

def Head(context):
    return (
        Title(f'{context.name} | #{context.generator_item}'),
    )

def Nav(context):
    current_tag = context.generator_item
    name_url_pairs = [
        (f'#{current_tag}', slugify(current_tag)),
        *[
            (f'#{tag}', slugify(tag))
            for tag in context.all_tags
            if tag != current_tag
        ]
    ]
    return subnav.Body(
        context,
        name_url_pairs,
        title="Tags"
    )

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
