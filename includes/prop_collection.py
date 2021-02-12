
from lib import NotDefined
from lib.htmlephant import Div

Head = NotDefined

Body = lambda context, items, wide=False: (
    Div(
        _class='collection',
        children=[
            Div(
                _class=f'item{" wide" if wide else ""}',
                children=item
            )
            for item in items
        ]
    ),
)
