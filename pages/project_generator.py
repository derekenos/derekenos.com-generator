
from lib import (
    guess_extension,
    microdata as md,
)
from lib.htmlephant_extensions import Main
from lib.htmlephant import (
    NOEL,
    Anchor,
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
    # TODO - expect all project to have an image.
    images = project.get('images')
    if images:
        # Get the first image in the list.
        image = images[0]
        # Parse the filename.
        match_d = context.normalized_image_filename_regex.match(
            image['filename']
        ).groupdict()
        # Get the fallback (i.e. last) image mimetype.
        mimetype = context.prioritized_derivative_image_mimetypes[-1]
        # Use the min of the original and fallback image widths.
        width = min(
            image['sources']['original'].width,
            context.fallback_image_width
        )
        # Generate the matching derivative filename.
        filename = context.derivative_image_filename_template.format(
            item_name=match_d['item_name'],
            asset_id=match_d['asset_id'],
            width=width,
            extension=guess_extension(mimetype)
        )
        tags.append(OGMeta('image', context.static_url(filename)))

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
        *get_meta_tags(context),
        *subnav.Head(context),
    )

def Nav(context):
    current_project = context.generator_item
    name_url_pairs = [
        (project['name'], project['slug'])
        for project in context.projects
    ]
    return subnav.Body(context, name_url_pairs, current_project['name'])

Body = lambda context: (
    Main(
        _class='project',
        itemscope='',
        itemtype=(project:=context.generator_item)['type'],
        children=(
            H1(f'{project["name"]} Project Details'),
            *get_microdata_meta(context),
            *includes.project.Body(context, **project)
        )
    ),
)
