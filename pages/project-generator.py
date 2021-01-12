
from lib import (
    NotDefined,
    stubify,
)

from includes import project as _project

CONTEXT_ITEMS_GETTER = lambda context: context.projects
FILENAME_GENERATOR = lambda project: f'project-{stubify(project["name"])}.html'

Head = NotDefined

Body = lambda context: _project.Body(context, **context.generator_item)
