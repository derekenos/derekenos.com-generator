
from itertools import chain

from lib.htmlephant import (
    Link,
    StdMeta,
)

from . import google_analytics
from . import live_dev

Head = lambda context: chain(
    (
        StdMeta(
            'generator',
            'https://github.com/derekenos/derekenos.com-generator'
        ),
        Link(rel='stylesheet', href=context.static('shared.css'))
    ),
    live_dev.Head(context) if not context.production else (),
    google_analytics.Head(context) if context.production else ()
)
