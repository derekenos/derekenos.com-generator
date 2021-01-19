
from lib import microdata as md
from lib.htmlephant import (
    Anchor,
    Br,
    Div,
    Em,
    H1,
    Li,
    OGMeta,
    Ol,
    Span,
    StdMeta,
    Title,
)

from includes import section

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
        itemtype=md.CONTACT_POINT,
        children=(
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
                children=(
                    Ol(
                        _class='links',
                        children=[
                            Li(
                                children=(
                                    Anchor(
                                        name,
                                        itemprop=md.SAME_AS,
                                        href=url
                                    ),
                                )
                            )
                            for name, url in context.social_name_url_pairs
                        ]
                    ),
                )
            )
        )
    ),
)
