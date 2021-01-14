
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

def Body(context, name, slug, short_description, tags, thumb_img_base_fn,
         thumb_img_alt, **kwargs):
    return (
        H1(children=(Anchor(name, href=slug),)),
        H2(short_description) if short_description else NOEL,
        H3(' '.join(f'#{tag}' for tag in tags)) if tags else NOEL,
        Anchor(
            href=slug,
            children=picture.Body(
                context,
                srcsets=(context.static(f'{thumb_img_base_fn}.webp'),),
                src=context.static(f'{thumb_img_base_fn}.png'),
                alt=thumb_img_alt
            )
        )
    )
