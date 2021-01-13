
from lib import NotDefined
from lib.htmlephant import Div

Head = NotDefined

Body = lambda context, items: (
    Div(
        _class="collection",
        children=[
            Div(_class='item', children=item)
            for item in items
        ]
    ),
)
