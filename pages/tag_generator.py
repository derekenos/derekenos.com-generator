
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

FILENAME_GENERATOR = lambda tag: f'tag-{tag["name"]}.html'

slugify = lambda tag_name: \
    f'/{FILENAME_GENERATOR({"name": tag_name}).rsplit(".", 1)[0]}'

CONTEXT_ITEMS_GETTER = lambda context: [
    {
        'name': tag_name,
        'slug': slugify(tag_name)
    }
    for tag_name in
    sorted(set(chain(*[project['tags'] for project in context.projects])))
]

def Head(context):
    return (
        Title(f'{context.name} | #{context.generator_item["name"]}'),
    )

def Nav(context):
    current_tag = context.generator_item
    name_url_pairs = [
        (f'#{current_tag["name"]}', current_tag['slug']),
        *[
            (f'#{tag_name}', slugify(tag_name))
            for tag_name in context.all_tags
            if tag_name != current_tag['name']
        ]
    ]
    return subnav.Body(context, name_url_pairs)

Body = lambda context: (
    Div(
        _class='content tag',
        children=(
            H1(desc:=f'Projects Tagged #{(tag:=context.generator_item["name"])}'),
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
