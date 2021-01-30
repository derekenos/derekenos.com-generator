
from lib import NotDefined

from lib.htmlephant import Meta

Head = lambda context, url: (
    Meta(_http_equiv='Refresh', content=f'0; URL={url}'),
)

Body = NotDefined
