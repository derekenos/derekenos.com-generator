
from . import (
    google_analytics,
    style,
)

Head = lambda context: () \
    + google_analytics.Head(context) \
    + style.Head(context)
