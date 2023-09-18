import json
from jsonschema import Draft7Validator, validators

def generate_json_schema(json_data):
    schema = {}

    def walk(current_data, current_schema):
        if isinstance(current_data, dict):
            current_schema['type'] = 'object'
            current_schema['properties'] = {}
            for key, value in current_data.items():
                current_schema['properties'][key] = {}
                walk(value, current_schema['properties'][key])
        elif isinstance(current_data, list):
            current_schema['type'] = 'array'
            current_schema['items'] = {}
            if len(current_data) > 0:
                walk(current_data[0], current_schema['items'])
        else:
            current_schema['type'] = 'string'

    walk(json_data, schema)
    return schema





def generate_json_schema_v2(json_data):
    def set_defaults(validator, properties, instance, schema):
        for prop, subschema in properties.items():
            if "type" not in subschema:
                if isinstance(instance, list):
                    subschema["type"] = "array"
                elif isinstance(instance, dict):
                    subschema["type"] = "object"
            if "properties" in subschema:
                set_defaults(validator, subschema["properties"], instance.get(prop, {}), subschema)

    def extend_with_defaults(validator_class):
        ValidateProperties = validator_class.VALIDATORS["properties"]

        def set_defaults(validator, properties, instance, schema):
            for error in ValidateProperties(validator, properties, instance, schema):
                yield error

            for prop in instance:
                if prop not in properties:
                    for error in validator.descend(schema.get("additionalProperties", {}), instance[prop], schema, path=prop):
                        yield error

        return validators.extend(validator_class, {"properties": set_defaults})

    schema = {}
    validator = extend_with_defaults(Draft7Validator)(schema)
    set_defaults(validator, {}, json_data, schema)
    return schema