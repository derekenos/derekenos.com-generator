
from lib.htmlephant_extensions import Em
from lib.htmlephant import (
    Anchor,
    Br,
    H1,
    Div,
    Li,
    Div,
    Title,
    Ul,
)

from includes import section
from includes import links_list

Head = lambda context: (
    Title('Derek Enos | Contact'),
)

Body = lambda context: (
    Div(
        _class='content',
        children=(
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
