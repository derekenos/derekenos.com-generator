
from lib import microdata as md
from lib.htmlephant_extensions import Main
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
    scope_links_list,
    section,
)

DESCRIPTION = 'How to contact me'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    Title(f'{context.name} | Contact'),
)

Body = lambda context: (
    Main(
        _class='contact',
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
                )
            ),
            *section.Body(
                context,
                'Other channels',
                children=scope_links_list.Body(
                    context,
                    prop_type_name_url_tuples=[
                        (
                            md.Props.contactPoint,
                            md.Types.ContactPoint,
                            name,
                            url
                        )
                        for name, url in context.social_name_url_pairs
                    ]
                )
            ),
            *section.Body(
                context,
                'Old Websites',
                children=scope_links_list.Body(
                    context,
                    prop_type_name_url_tuples=[
                        (
                            md.Props.url,
                            md.Types.CreativeWork,
                            name,
                            url
                        )
                        for name, url in context.old_website_name_url_pairs
                    ]
                )
            )
        )
    ),
)
