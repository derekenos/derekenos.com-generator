
from lib.htmlephant import (
    Anchor,
    Br,
    Div,
    Div,
    H1,
    Title,
)
from lib.htmlephant_extensions import (
    Em,
    OGMeta,
    StdMeta,
)

from includes import section
from includes import links_list

DESCRIPTION = 'How to contact me'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    Title('Derek Enos | Contact'),
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
                        'derek@derekenos.com',
                        href="mailto:derek@derekenos.com"
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
                    (
                        ('Github', "https://github.com/derekenos"),
                        ('Instagram', "https://www.instagram.com/derekjenos/"),
                        ('YouTube', "https://www.youtube.com/derekenos"),
                        ('LinkedIn', "https://www.linkedin.com/in/derekenos"),
                        ('Patreon', "https://www.patreon.com/derekenos"),
                    )
                )
            )
        )
    ),
)
