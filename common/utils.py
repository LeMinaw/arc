from json import JSONEncoder


class JSONSetEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return super().default(self, obj)


def make_default_object_schema():
    return {
        "$defs": {
            "range": {
                "type": "array",
                "items": {
                    "type": "number",
                },
                "minItems": 2,
                "maxItems": 2,
                "widget": "range",
            },
        },
        "type": "object",
        "properties": {},
        "required": set(),
        "additionalProperties": False,
    }


def short_description(description: str):
    def decorator(function):
        function.short_description = description
        return function

    return decorator
