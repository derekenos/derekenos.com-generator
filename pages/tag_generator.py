
from itertools import chain

from lib import microdata as md
from lib.htmlephant_extensions import Main
from lib.htmlephant import (
    NOEL,
    Anchor,
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

get_title = \
    lambda context: f'{context.name} | #{context.generator_item["name"]}'

def get_meta_tags(context):
    """Return a list of Meta elements comprising tag metadata.
    See:
      https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name
      https://ogp.me/#metadata
    """
    tag = context.generator_item
    description = f'A collection of projects associated with the tag #{tag["name"]}.'
    return (
        StdMeta('author', context.name),
        StdMeta('description', description),
        OGMeta('description', description),
        StdMeta('keywords', ', '.join((tag['name'], 'tag', 'projects'))),
        OGMeta('title', get_title(context)),
        OGMeta('type', 'website'),
        OGMeta('url', context.url(tag['slug'])),
    )

Head = lambda context: (
    Title(get_title(context)),
    *get_meta_tags(context),
    *subnav.Head(context),
)

def Nav(context):
    current_tag = context.generator_item
    name_url_pairs = [
        (f'#{tag_name}', slugify(tag_name))
        for tag_name in context.all_tags
    ]
    return subnav.Body(context, name_url_pairs, f'#{current_tag["name"]}')

def Body(context):
    tag_name = context.generator_item["name"]
    description = f'Projects Tagged #{tag_name}'
    return (
        Main(
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
