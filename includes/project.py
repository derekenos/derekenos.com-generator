
from itertools import chain

from lib import NotDefined
from lib import microdata as md
from lib.htmlephant_extensions import UnescapedParagraph
from lib.htmlephant import (
    Anchor,
    Div,
    H2,
    H3,
    MDMeta,
    Section,
)

from includes import (
    links_list,
    picture,
    section,
    video,
)

Head = NotDefined

def Body(context,
         name,
         slug,
         short_description,
         tags,
         images,
         collateral_creations=None,
         dependent_projects=None,
         description=None,
         github_url=None,
         hide_card=False,
         live_url=None,
         media_name_url_pairs=None,
         videos=None,
    ):
    image = images[0]
    image_base_filename = image['base_filename']
    # Inline includes.section to specify itemprops.
    els = [
        Section(children=(
            H2(name, itemprop=md.NAME),
            H3(short_description, itemprop=md.ABSTRACT),
            *picture.Body(
                context,
                itemprop=md.SUBJECT_OF,
                srcsets=(context.static(fn:=f'{image_base_filename}.webp'),),
                src=context.static(f'{image_base_filename}.png'),
                name=image['name'],
                description=image['description'],
                upload_date=context.static_last_modified_iso8601(fn)
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

    # Add videos.
    if videos:
        els.extend(
            section.Body(
                context,
                'Videos',
                children=chain((
                    video.Body(
                        context,
                        itemprop=md.SUBJECT_OF,
                        src=context.static(vid['filename']),
                        poster=context.static(vid['thumb_filename']),
                        name=vid['name'],
                        description=vid['description'],
                        upload_date=context.static_last_modified_iso8601(
                            vid['filename']
                        )
                    )
                    for vid in videos
                )),
            )
        )

    # Add media links.
    if media_name_url_pairs:
        els.extend(
            section.Body(
                context,
                'Additional Media',
                children=links_list.Body(
                    context,
                    itemprop=md.ASSOCIATED_MEDIA,
                    itemtype=md.MEDIA_OBJECT,
                    name_url_pairs=media_name_url_pairs
                )
            )
        )

    return els
