
from lib import NotDefined
from lib.htmlephant_extensions import UnescapedParagraph
from lib.htmlephant import (
    Anchor,
    H1,
    H2,
    H3,
    Li,
    Ol,
    Paragraph,
)

from macros import picture
from includes import section
from includes import links_list

Head = NotDefined

def Body(context,
         name,
         slug,
         short_description,
         tags,
         thumb_img_base_fn,
         thumb_img_alt,
         description=None,
         collateral_creations=None,
         related_projects=None,
         github_url=None,
    ):
    els = [
        *section.Body(
            context,
            name,
            short_description,
            picture.Body(
                context,
                srcsets=(context.static(f'{thumb_img_base_fn}.webp'),),
                src=context.static(f'{thumb_img_base_fn}.png'),
                alt=thumb_img_alt
            )
        )
    ]
    # Add description.
    if description:
        els.extend(
            section.Body(
                context,
                'Description',
                children=(UnescapedParagraph(description),)
            )
        )
    # Add Github Link.
    if github_url:
        els.extend(
            section.Body(context, 'Design Files', children=(
                Anchor('Github', href=github_url),
            ))
        )
    # Add collateral creations.
    if collateral_creations:
        els.extend(
            section.Body(
                context,
                'Collateral Creations',
                '',
                links_list.Body(
                    context,
                    [
                        (project['name'], project['slug'])
                         for project in context.projects
                         if project['name'] in collateral_creations

                    ]
                )
            )
        )
    # Add related projects.
    if related_projects:
        els.extend(
            section.Body(
                context,
                'Related Projects',
                '',
                links_list.Body(
                    context,
                    [
                        (project['name'], project['slug'])
                         for project in context.projects
                         if project['name'] in related_projects

                    ]
                )
            )
        )
    return els
