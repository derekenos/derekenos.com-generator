
from lib import NotDefined
from lib import microdata as md
from lib.htmlephant_extensions import (
    MDMeta,
    UnescapedParagraph,
)
from lib.htmlephant import (
    Anchor,
    H2,
    H3,
    Section,
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
         additional_img_base_fns=(),
         collateral_creations=(),
         dependent_projects=(),
         description=None,
         github_url=None,
         hide_card=False,
         live_url=None,
    ):
    thumb_base_filename, thumb_alt = thumb_base_filename_alt_pairs[0]
    # Inline includes.section to specify itemprops.
    els = [
        Section(children=(
            H2(name, itemprop=md.NAME),
            H3(short_description, itemprop=md.ABSTRACT),
            MDMeta(md.IMAGE, context.static(f'{thumb_base_filename}.png')),
            *picture.Body(
                context,
                srcsets=(context.static(f'{thumb_base_filename}.webp'),),
                src=context.static(f'{thumb_base_filename}.png'),
                alt=thumb_alt
            )
        ))
    ]
    # Add description.
    if description:
        els.extend(
            section.Body(
                context,
                'Description',
                children=(
                    UnescapedParagraph(
                        description,
                        itemprop=md.DESCRIPTION
                    ),
                )
            )
        )

    # Add Live Link.
    if live_url:
        els.extend(
            section.Body(
                context,
                'Try It Out',
                children=(
                    Anchor(
                        'Launch this application',
                        href=live_url
                    ),
                )
            )
        )

    # Add Github Link.
    if github_url:
        els.extend(
            section.Body(
                context,
                'Source Files',
                children=(
                    Anchor(
                        'Github',
                        href=github_url
                    ),
                )
            )
        )

    # Add collateral creations.
    if collateral_creations:
        els.extend(
            section.Body(
                context,
                'Collateral Creations',
                children=links_list.Body(
                    context,
                    itemprop=md.HAS_PART,
                    itemtype=md.CREATIVE_WORK,
                    name_url_pairs=[
                        (project['name'], project['slug'])
                        for project in context.projects
                        if project['name'] in collateral_creations
                    ]
                )
            )
        )

    # Add dependent projects.
    if dependent_projects:
        els.extend(
            section.Body(
                context,
                'Dependent Projects',
                children=links_list.Body(
                    context,
                    itemprop=md.IS_PART_OF,
                    itemtype=md.CREATIVE_WORK,
                    name_url_pairs=[
                        (project['name'], project['slug'])
                        for project in context.projects
                        if project['name'] in dependent_projects
                    ]
                )
            )
        )

    return els
