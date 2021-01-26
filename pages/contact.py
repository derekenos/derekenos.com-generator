
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
        itemtype=md.Types.Person,
        children=(
            MDMeta(md.Props.name, context.name),
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
                                itemprop=md.Props.email,
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
                    prop_type_name_urltype_url_tuples=[
                        (
                            md.Props.contactPoint,
                            md.Types.ContactPoint,
                            name,
                            md.Props.url,
                            url
                        )
                        for name, url in context.social_name_url_pairs
                    ]
                )
            )
        )
    ),
)
