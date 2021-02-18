
from lib.htmlephant import (
    Link,
    StdMeta,
)

from . import google_analytics
from . import live_dev

def Head(context):
    els = [
        StdMeta(
            'generator',
            'https://github.com/derekenos/derekenos.com-generator'
        ),
        Link(rel='stylesheet', href=context.static('styles/shared.css'))
    ]
    if context.production:
        if getattr(context, 'google_analytics_id', None) is not None:
            els.extend(google_analytics.Head(context))
    else:
         els.extend(live_dev.Head(context))
    return els
