

from lib.htmlephant_extensions import Main
from lib import (
    flatten,
    pluck,
)
from lib.htmlephant import (
    H1,
    OGMeta,
    StdMeta,
    Title,
)

from includes import project_card
from includes import collection

DESCRIPTION = 'Home page displaying selected projects'

Head = lambda context: (
    StdMeta('description', DESCRIPTION),
    OGMeta('description', DESCRIPTION),
    StdMeta('keywords', ','.join(
        sorted(set(flatten(pluck('tags', context.projects))))
    )),
    Title(f'{context.name} | Home'),
)

Body = lambda context: (
    Main(
        _class='content home',
        children=(
            H1(DESCRIPTION),
            *collection.Body(
                context,
                name='Selected Projects',
                items=[
                    project_card.Body(context, **prj)
                    for prj in context.projects
                    if not prj.get('hide_card', False)
                ]
            )
        )
    ),
)
