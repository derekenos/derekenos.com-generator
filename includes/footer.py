
from datetime import date

from lib import NotDefined
from lib.htmlephant import (
    Anchor,
    Div,
)

Head = NotDefined

Body = lambda context: (
    Div(
        f'Generated on {date.today()} by ',
        _class='footer',
        children=(
            Anchor(
                'derekenos.com-generator',
                href='https://github.com/derekenos/derekenos.com-generator'
            ),
        )
    ),
)
