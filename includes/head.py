
from lib.htmlephant_extensions import Link
from . import google_analytics

Head = lambda context: () \
    + (() if context.development else google_analytics.Head(context)) \
    + (Link(rel='stylesheet', href=context._static('shared.css')),)
