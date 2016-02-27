"""JSON Schema utilities

Attributes:
    cache: Cache of previously loaded schemas

Resources:
    http://json-schema.org/
    http://json-schema.org/latest/json-schema-core.html
    http://spacetelescope.github.io/understanding-json-schema/index.html

"""

import os
import json

import jsonschema

cache = {}
module_dir = os.path.dirname(__file__)
schema_dir = os.path.join(module_dir, "schema")


def load_all():
    for schema in os.listdir(schema_dir):
        if schema.startswith(("_", ".")):
            continue
        if not schema.endswith(".json"):
            continue
        if not os.path.isfile(os.path.join(schema_dir, schema)):
            continue
        with open(os.path.join(schema_dir, schema)) as f:
            cache[schema] = json.load(f)


def validate(data, schema):
    if isinstance(schema, basestring):
        schema = cache[schema + ".json"]

    resolver = jsonschema.RefResolver(
        "",
        None,
        store=cache,
        cache_remote=True)
    return jsonschema.validate(data, schema, types={"array": (list, tuple)},
                               resolver=resolver)


ValidationError = jsonschema.ValidationError

load_all()

__all__ = ["validate",
           "ValidationError"]
