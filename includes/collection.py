
from lib import NotDefined
from lib import microdata as md
from lib.htmlephant import (
    Div,
    MDMeta,
)

Head = NotDefined

Body = lambda context, name, items, wide=False: (
    Div(
        _class='collection',
        itemscope='',
        itemtype=md.Types.ItemList,
        children=(
            MDMeta(md.Props.name, name),
            *[
                Div(
                    itemprop=md.Props.itemListElement,
                    itemscope='',
                    itemtype=md.Types.ListItem,
                    _class=f'item{" wide" if wide else ""}',
                    children=(
                        MDMeta(md.Props.position, i),
                        *item
                    )
                )
                for i, item in enumerate(items)
            ]
        )
    ),
)
