
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

from macros import picture

Head = NotDefined

def Body(context, name, slug, short_description, tags,
         thumb_base_filename_alt_pairs, **kwargs):
    thumb_base_filename, thumb_alt = thumb_base_filename_alt_pairs[0]
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
        MDMeta(md.IMAGE, context.static(f'{thumb_base_filename}.png')),
        Anchor(
            itemprop=md.URL,
            href=slug,
            children=picture.Body(
                context,
                srcsets=(
                    context.static(f'{thumb_base_filename}.webp'),
                ),
                src=context.static(f'{thumb_base_filename}.png'),
                alt=thumb_alt
            )
        )
    )
