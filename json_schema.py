import json

from jsonschema import Draft7Validator, validators


def generate_json_schema(json_data):
    """_summary_

    Args:
        json_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    schema = {}

    def walk(current_data, current_schema):
        if isinstance(current_data, dict):
            current_schema["type"] = "object"
            current_schema["properties"] = {}
            for key, value in current_data.items():
                current_schema["properties"][key] = {}
                walk(value, current_schema["properties"][key])
        elif isinstance(current_data, list):
            current_schema["type"] = "array"
            current_schema["items"] = {}
            if len(current_data) > 0:
                walk(current_data[0], current_schema["items"])
        else:
            current_schema["type"] = "string"

    walk(json_data, schema)
    return schema


def generate_json_schema_v2(json_data):
    """_summary_

    Args:
        json_data (_type_): _description_
    """

    def parse_object(obj):
        schema = {"type": "object", "properties": {}, "required": []}
        for key, value in obj.items():
            schema["properties"][key] = parse(value)
            schema["required"].append(key)
        return schema

    def parse_array(arr):
        if len(arr) == 0:
            return {"type": "array", "items": {}}
        else:
            return {"type": "array", "items": parse(arr[0])}

    def parse(value):
        """_summary_

        Args:
            value (_type_): _description_

        Returns:
            _type_: _description_
        """
        type_mapping = {
            dict: parse_object,
            list: parse_array,
            bool: "boolean",
            int: "integer",
            float: "number",
            type(None): "null",
        }
        value_type = type(value)
        if isinstance(value, dict) or isinstance(value, list):
            return type_mapping[value_type](value)
        else:
            return {"type": type_mapping.get(value_type, "string")}

    def parse_old(value):
        if isinstance(value, dict):
            return parse_object(value)
        elif isinstance(value, list):
            return parse_array(value)
        elif isinstance(value, bool):
            return {"type": "boolean"}
        elif isinstance(value, int):
            return {"type": "integer"}
        elif isinstance(value, float):
            return {"type": "number"}
        elif value is None:
            return {"type": "null"}
        else:
            return {"type": "string"}

    schema = parse(json_data)
    return schema
