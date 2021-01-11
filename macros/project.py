
from lib.htmlephant import (
    H1,
    H2,
    H3,
)

from macros.picture import Picture

Project = lambda context, name, desc, tags, img_base_fn, img_alt: (
    H1(name),
    H2(desc),
    H3(' '.join(f'#{tag}' for tag in tags)),
    *Picture(context, img_base_fn, img_alt)
)
