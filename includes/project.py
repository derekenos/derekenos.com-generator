
from lib import NotDefined
from lib.htmlephant import (
    H1,
    H2,
    H3,
)

from macros import picture

Head = NotDefined

Body = lambda context, name, desc, tags, img_base_fn, img_alt: (
    H1(name),
    H2(desc),
    H3(' '.join(f'#{tag}' for tag in tags)),
    *picture.Body(
        context,
        srcsets=(context.static(f'{img_base_fn}.webp'),),
        src=context.static(f'{img_base_fn}.png'),
        alt=img_alt
    )
)
