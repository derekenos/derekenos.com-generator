
from lib import microdata as md
from lib.htmlephant import (
    Div,
    H1,
    OGMeta,
    StdMeta,
    Title,
)

import includes.project

CONTEXT_ITEMS_GETTER = lambda context: context.projects
FILENAME_GENERATOR = lambda project: f'{project["slug"]}.html'

def get_meta_tags(context):
    """Return a list of Meta elements comprising project metadata.
    See:
      https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name
      https://ogp.me/#metadata
    """
    project = context.generator_item
    tags = []
    # Author.
    tags.append(StdMeta('author', context.name))
    # Description.
    tags.extend((
        StdMeta('description', project['short_description']),
        OGMeta('description', project['short_description'])
    ))
    # Image
    tags.append(
        OGMeta(
            'image',
            context.static_url(f'{project["images"][0]["base_filename"]}.png')
        )
    )
    # Keywords
    if project['tags']:
        tags.append(StdMeta('keywords', ','.join(project['tags'])))
    # Title
    tags.append(OGMeta('title', project['name']))
    # Type
    tags.append(OGMeta('type', 'website'))
    # URL
    tags.append(OGMeta('url', context.url(project['slug'])))
    return tags

def Head(context):
    return (
        Title(f'{context.name} | {context.generator_item["name"]}'),
        *get_meta_tags(context)
    )

Body = lambda context: (
    Div(
        _class='content project',
        itemscope='',
        itemtype=(md.SOFTWARE_SOURCE_CODE
                  if 'github_url' in context.generator_item
                  else md.CREATIVE_WORK),
        children=(
            H1(f'{context.generator_item["name"]} Project Details'),
            *includes.project.Body(context, **context.generator_item)
        )
    ),
)
