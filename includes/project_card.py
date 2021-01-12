
from lib import (
    NotDefined,
    stubify,
)
from lib.htmlephant import (
    Anchor,
    H1,
    H2,
    H3,
)

from macros import picture

Head = NotDefined

def Body(context, name, short_description, tags, thumb_img_base_fn,
         thumb_img_alt, **kwargs):
    return (
        H1(children=(Anchor(name, href=f'project-{stubify(name)}.html'),)),
        H2(short_description),
        H3(' '.join(f'#{tag}' for tag in tags)),
        Anchor(
            href=f'project-{stubify(name)}.html',
            children=picture.Body(
                context,
                srcsets=(context.static(f'{thumb_img_base_fn}.webp'),),
                src=context.static(f'{thumb_img_base_fn}.png'),
                alt=thumb_img_alt
            )
        )
    )
