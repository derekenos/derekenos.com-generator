
from itertools import chain

from lib import stubify

from includes import project as _project
from includes import project_nav

CONTEXT_ITEMS_GETTER = lambda context: context.projects
FILENAME_GENERATOR = lambda project: f'project-{stubify(project["name"])}.html'

Head = lambda project: lambda context: project_nav.Head(context)

Body = lambda project: lambda context: chain(
    project_nav.Body(context, project),
    _project.Body(context, **project)
)
