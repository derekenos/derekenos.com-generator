
from lib import NotDefined
from lib.htmlephant_extensions import UnescapedParagraph
from lib.htmlephant import (
    Anchor,
    H2,
    H3,
    Li,
    Section,
    Span,
    Ol,
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
         dependent_projects=(),
         github_url=None,
         additional_img_base_fns=(),
         **kwargs
    ):
    thumb_base_filename, thumb_alt = thumb_base_filename_alt_pairs[0]
    # Inline includes.section to specify itemprops.
    els = [
        Section(children=(
            H2(name, itemprop='name'),
            H3(short_description, itemprop='abstract'),
            *picture.Body(
                context,
                itemprop='image',
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
                        itemprop='description'
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
                children=(
                    # Inline includes.links_list to specify itemprops.
                    Ol(
                        _class='links',
                        children=[
                            Li(
                                itemprop='hasPart',
                                itemscope='',
                                itemtype='https://schema.org/CreativeWork',
                                children=(
                                    Anchor(
                                        itemprop='url',
                                        href=project['slug'],
                                        children=(
                                            Span(
                                                project['name'],
                                                itemprop='name'
                                            ),
                                        )
                                    ),
                                )
                            )
                            for project in context.projects
                            if project['name'] in collateral_creations
                        ]
                    ),
                )
            )
        )
    # Add dependent projects.
    if dependent_projects:
        els.extend(
            section.Body(
                context,
                'Dependent Projects',
                children=(
                    # Inline includes.links_list to specify itemprops.
                    Ol(
                        _class='links',
                        children=[
                            Li(
                                itemprop='isPartOf',
                                itemscope='',
                                itemtype='https://schema.org/CreativeWork',
                                children=(
                                    Anchor(
                                        itemprop='url',
                                        href=project['slug'],
                                        children=(
                                            Span(
                                                project['name'],
                                                itemprop='name'
                                            ),
                                        )
                                    ),
                                )
                            )
                            for project in context.projects
                            if project['name'] in dependent_projects
                        ]
                    ),
                )
            )
        )
    return els
