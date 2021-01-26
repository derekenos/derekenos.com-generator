"""Microdata constants.
"""
from types import SimpleNamespace


Types = SimpleNamespace(**{
    k: f'https://schema.org/{k}'
    for k in (
            'ContactPoint',
            'CreativeWork',
            'ImageObject',
            'Intangible',
            'ItemList',
            'ListItem',
            'MediaObject',
            'Person',
            'SoftwareApplication',
            'SoftwareSourceCode',
            'VideoObject',
    )
})

Props = SimpleNamespace(**{
    k: k for k in (
        'abstract',
        'applicationCategory',
        'associatedMedia',
        'codeRepository',
        'contactPoint',
        'contentUrl',
        'description',
        'email',
        'encodingFormat',
        'hasPart',
        'image',
        'installUrl',
        'isPartOf',
        'itemListElement',
        "mainEntityOfPage",
        'name',
        'operatingSystem',
        'position',
        'sameAs',
        'subjectOf',
        'thumbnailUrl',
        'uploadDate',
        'url',
    )
})
