
from lib import NotDefined
from lib.htmlephant import (
    Meta,
    OGMeta,
    StdMeta,
    Title,
)

def Head(context, destination, source='', description=None):
    description = description or f'Redirect {source} to {destination}'
    return (
        StdMeta('description', description),
        OGMeta('description', description),
        Title(f'{context.name} | {description}'),
        Meta(_http_equiv='Refresh', content=f'0; URL={destination}')
    )

Body = NotDefined
