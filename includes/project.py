
from lib import NotDefined
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
         short_description,
         tags,
         thumb_img_base_fn,
         thumb_img_alt,
         description=None,
         collateral_creation_name_href_pairs=None,
         related_project_name_href_pairs=None,
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
                children=(Paragraph(description),)
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
    if collateral_creation_name_href_pairs:
        els.extend(
            section.Body(
                context,
                'Collateral Creations',
                'New things that I created specifically for this project:',
                links_list.Body(context, collateral_creation_name_href_pairs)
            )
        )
    # Add related projects.
    if related_project_name_href_pairs:
        els.extend(
            section.Body(
                context,
                'Related Projects',
                '',
                links_list.Body(context, related_project_name_href_pairs)
            )
        )
    return els
