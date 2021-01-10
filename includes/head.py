
from . import google_analytics

Head = lambda context: () + google_analytics.Head(context)
