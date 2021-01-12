
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

Head = NotDefined

def Body(context, name, short_description, tags, thumb_img_base_fn,
         thumb_img_alt, description='', collateral_creations=(),
         related_projects=''):
    els = [
        H1(name),
        *picture.Body(
            context,
            srcsets=(context.static(f'{thumb_img_base_fn}.webp'),),
            src=context.static(f'{thumb_img_base_fn}.png'),
            alt=thumb_img_alt
        ),
        H2(short_description),
    ]
    # Add description.
    if description:
        els.extend((H1('Description'), Paragraph(description)))
    # Add collateral creations.
    if collateral_creations:
        els.extend((
            H1('Collateral Creations'),
            H2('New things that I created specifically for this project:'),
            Ol(id='collateral-creations',
               children=[
                   Li(children=(Anchor(name, href="#"),))
                   for name in collateral_creations
               ]
            )
        ))
    # Add related projects.
    if related_projects:
        els.extend((
            H1('Related Projects'),
            Ol(id='related-projects',
               children=[
                   Li(children=(Anchor(name, href="#"),))
                   for name in related_projects
               ]
            )
        ))
    return els
