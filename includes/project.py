
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
         thumb_base_filename_alt_pairs,
         description=None,
         collateral_creations=(),
         related_projects=(),
         github_url=None,
         additional_img_base_fns=(),
         **kwargs
    ):
    thumb_base_filename, thumb_alt = thumb_base_filename_alt_pairs[0]
    els = [
        *section.Body(
            context,
            name,
            short_description,
            children=picture.Body(
                context,
                srcsets=(context.static(f'{thumb_base_filename}.webp'),),
                src=context.static(f'{thumb_base_filename}.png'),
                alt=thumb_alt

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
            section.Body(context, 'Source Files', children=(
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
