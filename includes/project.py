
from itertools import chain

from lib import NotDefined
from lib import microdata as md
from lib.htmlephant_extensions import UnescapedParagraph
from lib.htmlephant import (
    Anchor,
    Div,
    H2,
    H3,
    H4,
    Section,
)

from includes import (
    picture,
    prop_links_list,
    scope_links_list,
    section,
    video,
)

Head = NotDefined

def Body(context,
         name,
         slug,
         short_description,
         tags,
         type,
         images,
         category=None,
         collateral_creations=None,
         dependent_of=None,
         depends_on=None,
         description=None,
         external_link_prop_name_url_tuples=None,
         github_url=None,
         hide_card=False,
         live_url=None,
         media_name_url_pairs=None,
         operating_system=None,
         videos=None,
    ):
    image = images[0]
    image_base_filename = image['base_filename']
    # Inline includes.section to specify itemprops.
    els = [
        Section(children=(
            H2(name, itemprop=md.Props.name),
            Div(children=[
                Anchor(
                    f'#{tag}',
                    _class='tag',
                    itemprop=md.Props.isPartOf,
                    href=f'/tagged-{tag}'
                )
                for tag in tags
            ]),
            H3(short_description, itemprop=md.Props.abstract),
            *picture.Body(
                context,
                itemprop=md.Props.subjectOf,
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
                        itemprop=md.Props.description
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
                        itemprop=md.Props.codeRepository,
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
                children=scope_links_list.Body(
                    context,
                    prop_type_name_url_tuples=[
                        (
                            md.Props.hasPart,
                            md.Types.CreativeWork,
                            project['name'],
                            project['slug']
                        )
                        for project in context.projects
                        if project['name'] in collateral_creations
                    ]
                )
            )
        )

    # Add dependencies.
    if depends_on:
        els.extend(
            section.Body(
                context,
                'Uses',
                children=scope_links_list.Body(
                    context,
                    prop_type_name_url_tuples=[
                        (
                            md.Props.hasPart,
                            md.Types.CreativeWork,
                            project['name'],
                            project['slug']
                        )
                        for project in context.projects
                        if project['name'] in depends_on
                    ]
                )
            )
        )

    # Add dependent projects.
    if dependent_of:
        els.extend(
            section.Body(
                context,
                'Used By',
                children=scope_links_list.Body(
                    context,
                    prop_type_name_url_tuples=[
                        (
                            md.Props.isPartOf,
                            md.Types.CreativeWork,
                            project['name'],
                            project['slug']
                        )
                        for project in context.projects
                        if project['name'] in dependent_of
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
                        itemprop=md.Props.subjectOf,
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

    # Add external links.
    if external_link_prop_name_url_tuples:
        els.extend(
            section.Body(
                context,
                'External Links',
                children=prop_links_list.Body(
                    context,
                    prop_name_url_tuples=external_link_prop_name_url_tuples
                )
            )
        )

    return els
