
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
    Title(f'{context.name} | Contact'),
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
                        context.email,
                        href=f'mailto:{context.email}'
                    ),
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
