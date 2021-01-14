
from lib.htmlephant import (
    NOEL,
    Div,
    Meta,
    Title,
)
from lib.htmlephant_extensions import (
    StdMeta,
    OGMeta,
)

from includes import project as _project

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
    author = getattr(context, 'author')
    if author:
        tags.append(StdMeta('author', author))
    # Description.
    description = f'{project["name"]} - {project["short_description"]}'
    tags.extend((
        StdMeta('description', description),
        OGMeta('description', description),
    ))
    # Image
    tags.append(
        OGMeta(
            'image',
            context.static_url(f'{project["thumb_img_base_fn"]}.webp')
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
        Title(f'Derek Enos | {context.generator_item["name"]}'),
        *get_meta_tags(context)
    )

Body = lambda context: (
    Div(
        _class='content',
        children=_project.Body(context, **context.generator_item)
    ),
)
