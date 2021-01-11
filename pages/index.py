
from lib.htmlephant import (
    Div,
    Title,
)

from includes import project

Head = lambda context: (
    Title('Projects'),
)

Body = lambda context: (
    Div(
        _class="content",
        children=[
            Div(_class='item', children=project.Body(context, **prj))
            for prj in context.projects
        ]
    ),
)
