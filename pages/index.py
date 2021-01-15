
from lib.htmlephant import (
    Div,
    Title,
)

from includes import project_card
from includes import collection

Head = lambda context: (
    Title(f'{context.name} | Projects'),
)

Body = lambda context: (
    Div(
        _class='content',
        children=collection.Body(
            context,
            [
                project_card.Body(context, **prj)
                for prj in context.projects
            ]
        )
    ),
)
