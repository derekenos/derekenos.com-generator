
from lib import NotDefined
from lib import microdata as md
from lib.htmlephant import (
    Div,
    MDMeta,
)

Head = NotDefined

Body = lambda context, itemprop, name, items, wide=False: (
    Div(
        _class='collection',
        itemprop=itemprop,
        itemscope='',
        itemtype=md.Types.Collection,
        children=(
            MDMeta(md.Props.name, name),
            *[
                Div(
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
