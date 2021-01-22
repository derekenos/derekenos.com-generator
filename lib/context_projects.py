"""Helper to automatically create inverse dependency properties for
Context.projects items.
"""

from collections import defaultdict

COLLATERAL_CREATIONS = 'collateral_creations'
DEPENDS_ON = 'depends_on'
DEPENDENT_OF = 'dependent_of'

def get_enriched_projects(projects):
    """Return a version of the projects list that's enriched with inferables.
    """
    # Create a <project-name> -> <project-copy> map.
    name_project_map = {x['name']: x.copy() for x in projects}

    # Add any missing dependency properties.
    for name, project in name_project_map.items():
        for k in (DEPENDS_ON, DEPENDENT_OF):
            if k not in project:
                continue
            other_k = DEPENDENT_OF if k == DEPENDS_ON else DEPENDS_ON
            for other_name in project[k]:
                other_project = name_project_map[other_name]
                # Do not add a dependent_of relationship for values that already
                # exist in collateral_creations.
                if (COLLATERAL_CREATIONS in other_project
                    and k == DEPENDENT_OF
                    and name in other_project[COLLATERAL_CREATIONS]):
                    continue
                if other_k in other_project:
                    if name not in other_project[other_k]:
                        other_project[other_k].append(name)
                else:
                    other_project[other_k] = [name]

    return name_project_map.values()
