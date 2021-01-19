
from lib import NotDefined
from lib import microdata as md
from lib.htmlephant import Div
from lib.htmlephant_extensions import MDMeta

Head = NotDefined

Body = lambda context, name, items, wide=False: (
    Div(
        _class='collection',
        itemscope='',
        itemtype=md.ITEM_LIST,
        children=(
            MDMeta(md.NAME, name),
            *[
                Div(
                    itemprop=md.ITEM_LIST_ELEMENT,
                    itemscope='',
                    itemtype=md.LIST_ITEM,
                    _class=f'item{" wide" if wide else ""}',
                    children=(
                        MDMeta(md.POSITION, i),
                        *item
                    )
                )
                for i, item in enumerate(items)
            ]
        )
    ),
)
