
from lib import microdata as md
from lib.htmlephant import (
    NOEL,
    Anchor,
    Div,
    H1,
    MDMeta,
    OGMeta,
    StdMeta,
    Span,
    Title,
)

import includes.project
from includes import subnav

CONTEXT_ITEMS_GETTER = lambda context: context.projects
FILENAME_GENERATOR = lambda project: f'{project["slug"].lstrip("/")}.html'

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

def get_microdata_meta(context):
    """Return a list of MDMeta elements comprising that microdata meta tags
    representing data that is not otherwise represented in includes.project.
    """
    project = context.generator_item
    tags = []
    # Category
    if 'category' in project:
        tags.append(MDMeta(md.Props.applicationCategory, project['category']))
    # Operating system.
    if 'operating_system' in project:
        tags.append(
            MDMeta(md.Props.operatingSystem, project['operating_system'])
        )
    return tags

def Head(context):
    return (
        Title(f'{context.name} | {context.generator_item["name"]}'),
        *get_meta_tags(context)
    )

def Nav(context):
    current_project = context.generator_item
    name_url_pairs = [
        (current_project['name'], current_project['slug']),
        *[
            (project['name'], project['slug'])
            for project in context.projects
            if project != current_project
        ]
    ]
    return subnav.Body(context, name_url_pairs)

Body = lambda context: (
    Div(
        _class='content project',
        itemscope='',
        itemtype=(project:=context.generator_item)['type'],
        children=(
            H1(f'{project["name"]} Project Details'),
            *get_microdata_meta(context),
            *includes.project.Body(context, **project)
        )
    ),
)
