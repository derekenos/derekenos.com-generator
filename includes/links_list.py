
from lib import NotDefined
from lib import microdata as md
from lib.htmlephant import (
    Anchor,
    Li,
    Ol,
    Span,
)

Head = NotDefined

Body = lambda context, prop_type_name_urltype_url_tuples: (
    Ol(
        _class='links',
        children=[
            Li(
                itemprop=prop,
                itemscope='' if type is not None else None,
                itemtype=type,
                children=(
                    Anchor(
                        itemprop=urltype,
                        href=url,
                        children=(
                            Span(
                                name,
                                itemprop=md.Props.name if type is not None else None
                            ),
                        )
                    ),
                )
            )
            for prop, type, name, urltype, url in \
            prop_type_name_urltype_url_tuples
        ]
    ),
)
