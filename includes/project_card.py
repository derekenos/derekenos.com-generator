
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
         images, **kwargs):
    image = images[0]
    image_base_filename = image['base_filename']
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
                srcsets=(
                    context.static(fn:=f'{image_base_filename}.webp'),
                ),
                src=context.static(f'{image_base_filename}.png'),
                name=image['name'],
                description=image['description'],
                upload_date=context.static_last_modified_iso8601(fn)
            )
        )
    )
