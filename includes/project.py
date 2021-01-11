
from lib import NotDefined
from lib.htmlephant import (
    H1,
    H2,
    H3,
)

from macros import picture

Head = NotDefined

def Body(context, name, description, tags, thumb_img_base_fn, thumb_img_alt):
    return (
        H1(name),
        H2(description),
        H3(' '.join(f'#{tag}' for tag in tags)),
        *picture.Body(
            context,
            srcsets=(context.static(f'{thumb_img_base_fn}.webp'),),
            src=context.static(f'{thumb_img_base_fn}.png'),
            alt=thumb_img_alt
        )
    )
