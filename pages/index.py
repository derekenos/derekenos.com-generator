
from lib.htmlephant_extensions import Main
from lib import (
    flatten,
    pluck,
)
from lib.htmlephant import (
    H1,
    Link,
    OGMeta,
    StdMeta,
    Title,
)

from includes import (
    collection,
    project_card,
    section,
)

DESCRIPTION = 'Home page displaying selected projects'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    StdMeta('keywords', ','.join(
        sorted(set(flatten(pluck('tags', context.projects))))
    )),
    Title(f'{context.name} | Home'),
    # Support http://microformats.org/wiki/RelMeAuth
    *[Link(rel='me', href=url) for _, url in context.social_name_url_pairs]
)

Body = lambda context: (
    Main(
        _class='home',
        children=(
            H1(DESCRIPTION),
            *section.Body(
                context,
                children=collection.Body(
                    context,
                    name='Selected Projects',
                    items=[
                        project_card.Body(context, **prj)
                        for prj in context.projects
                        if not prj.get('hide_card', False)
                    ]
                )
            )
        )
    ),
)
