
from lib import microdata as md
from lib.htmlephant import (
    Anchor,
    Br,
    Div,
    Em,
    H1,
    MDMeta,
    OGMeta,
    Span,
    StdMeta,
    Title,
)

from includes import (
    links_list,
    section,
)

DESCRIPTION = 'How to contact me'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    Title(f'{context.name} | Contact'),
)

Body = lambda context: (
    Div(
        _class='content contact',
        itemscope='',
        itemtype=md.PERSON,
        children=(
            MDMeta(md.NAME, context.name),
            H1(DESCRIPTION),
            *section.Body(
                context,
                'Email',
                children=(
                    Anchor(
                        href=f'mailto:{context.email}',
                        children=(
                            Span(
                                context.email,
                                itemprop=md.EMAIL,
                            ),
                        ),
                    ),
                    Br(),
                    Br(),
                    Div(
                        children=(
                            Em(
                                "If I don't respond, please try again or through another channel; AWS SES has got some issues."
                            ),
                        )
                    )
                )
            ),
            *section.Body(
                context,
                'Other channels',
                children=links_list.Body(
                    context,
                    itemprop=md.CONTACT_POINT_PROP,
                    itemtype=md.CONTACT_POINT,
                    name_url_pairs=context.social_name_url_pairs
                )
            )
        )
    ),
)
