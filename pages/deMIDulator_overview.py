
from lib.htmlephant import (
    Meta,
    OGMeta,
    StdMeta,
    Title,
)

DESCRIPTION = 'Old site deMIDulator_overview.html redirect to project-demidulator'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    Title(f'{context.name} | {DESCRIPTION}'),
    Meta(_http_equiv='Refresh', content=f'0; URL=/project-demidulator')
)

Body = lambda context: ()
