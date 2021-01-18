
from lib.htmlephant import (
    Anchor,
    Br,
    Div,
    Div,
    Em,
    H1,
    OGMeta,
    StdMeta,
    Title,
)

from includes import section
from includes import links_list

DESCRIPTION = 'How to contact me'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    Title(f'{context.name} | Contact'),
)

Body = lambda context: (
    Div(
        _class='content contact',
        children=(
            H1(DESCRIPTION),
            *section.Body(
                context,
                'Email',
                children=(
                    Anchor(
                        context.email,
                        href=f'mailto:{context.email}'
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
                    context.social_name_url_pairs
                )
            )
        )
    ),
)
