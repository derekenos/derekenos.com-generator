"""Minimal JSON Schema validation library.
"""

###############################################################################
# Constants
###############################################################################

SUPPORTED_VERSION = "http://json-schema.org/draft-07/schema#"

###############################################################################
# Exceptions
###############################################################################

class Invalid(Exception): pass

###############################################################################
# Validator functions
###############################################################################

def validate_null(data, schema, defs):
    if data is not None:
        raise Invalid

def validate_string(data, schema, defs):
    if not isinstance(data, str):
        raise Invalid

def validate_number(data, schema, defs):
    if not isinstance(data, (int, float)):
        raise Invalid

def validate_boolean(data, schema, defs):
    if data is not True and data is not False:
        raise Invalid

def validate_array(data, schema, defs):
    items_schema = schema['items']
    if isinstance(items_schema, dict):
        for item in data:
            validate_next(item, items_schema, defs)
    elif isinstance(items_schema, list):
        for _data, _schema in zip(data, items_schema):
            validate_next(_data, _schema, defs)
    else:
        raise NotImplementedError

def validate_object(data, schema, defs):
    required_props = schema.get('required', ())
    missing_required = set()
    for prop_name, prop_schema in schema['properties'].items():
        if prop_name in data:
            validate_next(data[prop_name], prop_schema, defs)
        elif prop_name in required_props:
            missing_required.add(prop_name)

    errors = []
    if missing_required:
        errors.append(f'missing required properties: {list(missing_required)}')
    if errors:
        raise Invalid(', '.join(errors))

###############################################################################
# Validate function
###############################################################################

TYPE_VALIDATOR_MAP = {
    'null': validate_null,
    'string': validate_string,
    'number': validate_number,
    'boolean': validate_boolean,
    'array': validate_array,
    'object': validate_object,
}

def validate_next(data, schema, defs):
    # Resolve any definitions reference.
    while '$ref' in schema:
        schema = defs[schema["$ref"].split('/')[-1]]

    # Handle a single string-type type value.
    if isinstance(schema['type'], str):
        return TYPE_VALIDATOR_MAP[schema['type']](data, schema, defs)

    # Assume type is an iterable of possible types, validate against each until
    # one succeeds.
    exceptions = []
    for type in schema['type']:
        try:
            return TYPE_VALIDATOR_MAP[type](data, schema, defs)
        except Invalid as e:
            exceptions.append(e)
    raise Invalid(', '.join(map(str, exceptions)))

def validate(data, schema):
    # Assert that the schema version is supported.
    if schema.get('$schema') != SUPPORTED_VERSION:
        raise InvalidSchema(f'Expected schema.$schema = "{SUPPORTED_VERSION}"')

    # Get any definitions.
    defs = schema.get('definitions', {})

    validate_next(data, schema, defs)

###############################################################################


# DEBUG

if __name__ == '__main__':
    from json import load
    schema = load(open('context.schema.json', 'rb'))
    data = load(open('context.json', 'rb'))
    validate(data, schema)
