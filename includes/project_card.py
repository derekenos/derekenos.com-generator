
from lib import microdata as md
from lib import NotDefined
from lib.htmlephant import (
    Anchor,
    Div,
    H2,
    H3,
    H4,
    MDMeta,
    NOEL,
)

from pages import tag_generator
from includes import picture

Head = NotDefined

def Body(context, name, slug, short_description, tags,
         images=(), **kwargs):
    # TODO - use the actual project image.
    #image = images[0]
    image = images[0] if images else context.projects[3]['images'][0]
    return (
        H2(
            itemprop=md.Props.name,
            children=(Anchor(name, href=slug),)
        ),
        H3(
            short_description,
            itemprop=md.Props.description
        ) if short_description else NOEL,
        H4(
            children=[
                Anchor(
                    f'#{tag}',
                    _class='tag',
                    itemprop=md.Props.isPartOf,
                    href=tag_generator.slugify(tag)
                )
                for tag in tags
            ]
        ) if tags else NOEL,
        Anchor(
            itemprop=md.Props.url,
            href=slug,
            children=picture.Body(
                context,
                itemprop=md.Props.subjectOf,
                sources=image['sources'],
                sizes='(min-width: 1024px) 20vw, 90vw',
                name=image['name'],
                description=image['description'],
                upload_date=context.static_last_modified_iso8601(
                    image['filename']
                )
            )
        )
    )
