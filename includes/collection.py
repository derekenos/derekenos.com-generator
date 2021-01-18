
from lib import NotDefined
from lib.htmlephant import Div

Head = NotDefined

Body = lambda context, itemtype, items: (
    Div(
        _class="collection",
        children=[
            Div(
                itemscope='',
                itemtype=itemtype,
                _class='item',
                children=item
            )
            for item in items
        ]
    ),
)
