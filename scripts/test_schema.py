from jsonschema import validate
import json

with open('schema.json', 'r') as fp:
    schema = json.load(fp)
with open('example_collection.json', 'r') as fp:
    example = json.load(fp)

def test_schema():
    validate(instance=example, schema=schema)
