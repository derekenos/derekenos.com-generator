
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

from includes import picture

Head = NotDefined

def Body(context, name, slug, short_description, tags,
         images, **kwargs):
    image = images[0]
    image_base_filename = image['base_filename']
    return (
        H2(
            itemprop=md.NAME,
            children=(Anchor(name, href=slug),)
        ),
        H3(
            short_description,
            itemprop=md.DESCRIPTION
        ) if short_description else NOEL,
        H4(
            ' '.join(f'#{tag}' for tag in tags)
        ) if tags else NOEL,
        Anchor(
            itemprop=md.URL,
            href=slug,
            children=picture.Body(
                context,
                itemprop=md.SUBJECT_OF,
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
