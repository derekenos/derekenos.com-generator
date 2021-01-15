
from lib import NotDefined
from lib.htmlephant import (
    Anchor,
    H1,
    H2,
    H3,
    NOEL,
)

from macros import picture

Head = NotDefined

def Body(context, name, slug, short_description, tags, thumb_base_filename_alt_pairs,
         show_card=True, **kwargs):
    thumb_base_filename, thumb_alt = thumb_base_filename_alt_pairs[0]
    return () if not show_card else (
        H1(children=(Anchor(name, href=slug),)),
        H2(short_description) if short_description else NOEL,
        H3(' '.join(f'#{tag}' for tag in tags)) if tags else NOEL,
        Anchor(
            href=slug,
            children=picture.Body(
                context,
                srcsets=(context.static(f'{thumb_base_filename}.webp'),),
                src=context.static(f'{thumb_base_filename}.png'),
                alt=thumb_alt
            )
        )
    )
