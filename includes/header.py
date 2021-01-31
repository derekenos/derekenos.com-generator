
from lib import NotDefined
from lib.htmlephant_extensions import Header

from . import navbar

Head = NotDefined

Body = lambda context: (
    Header(
        children=(
            *navbar.Body(context),
        )
    ),
)
