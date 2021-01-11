
from lib.htmlephant_extensions import Link
from . import google_analytics

Head = lambda context: () \
    + (google_analytics.Head(context) if context.production else ()) \
    + (Link(rel='stylesheet', href=context.static('shared.css')),)
