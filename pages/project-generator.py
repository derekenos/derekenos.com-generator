
from lib import stubify
from lib.htmlephant import (
    Div,
    Title,
)

from includes import project as _project

CONTEXT_ITEMS_GETTER = lambda context: context.projects
FILENAME_GENERATOR = lambda project: f'project-{stubify(project["name"])}.html'

Head = lambda context: (
    Title(f'Derek Enos | {context.generator_item["name"]}'),
)

Body = lambda context: (
    Div(
        _class='content',
        children=_project.Body(context, **context.generator_item)
    ),
)
