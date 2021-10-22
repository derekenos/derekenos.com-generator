
from lib.htmlephant import (
    Meta,
    OGMeta,
    StdMeta,
    Title,
)

DESCRIPTION = 'Old site dIndex.html redirect to Home'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    Title(f'{context.name} | {DESCRIPTION}'),
    Meta(_http_equiv='Refresh', content=f'0; URL=/')
)

Body = lambda context: ()
