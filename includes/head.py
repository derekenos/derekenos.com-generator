
from itertools import chain

from lib.htmlephant_extensions import Link
from . import google_analytics
from . import auto_reload

Head = lambda context: chain(
    auto_reload.Head(context) if not context.production else (),
    google_analytics.Head(context) if context.production else (),
    (Link(rel='stylesheet', href=context.static('shared.css')),)
)
