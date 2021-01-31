
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
    """Return a list of Meta elements comprising tag metadata.
    See:
      https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name
      https://ogp.me/#metadata
    """
    tag = context.generator_item
    els = []
    # Author.
    els.append(StdMeta('author', context.name))
    # Description.
    description = f'A collection of projects associated with the tag #{tag["name"]}.'
    els.extend((
        StdMeta('description', description),
        OGMeta('description', description)
    ))
    # Keywords
    els.append(
        StdMeta('keywords', ', '.join((tag['name'], 'tag', 'projects')))
    )
    # Title
    title = f'{context.name} | #{tag["name"]}'
    els.extend((
        OGMeta('title', title),
        Title(title)
    ))
    # Type
    els.append(OGMeta('type', 'website'))
    # URL
    els.append(OGMeta('url', context.url(tag['slug'])))
    return els

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

def Body(context):
    tag_name = context.generator_item["name"]
    description = f'Projects Tagged #{tag_name}'
    return (
        Div(
            _class='content tag',
            children=(
                H1(description),
                *collection.Body(
                    context,
                    name=description,
                    items=[
                        project_card.Body(context, **project)
                    for project in context.projects
                    if tag_name in project['tags']
                    ]
                )
            )
        ),
    )
