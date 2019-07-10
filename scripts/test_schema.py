from jsonschema import validate
import json

def _read_json(filename):
    with open(filename, 'r') as fp:
        js = json.load(fp)
    return js

schema = _read_json('schema.json')

def test_schema(json_filename='example_collection.json'):
    sample = _read_json(json_filename)
    validate(instance=sample, schema=schema)
    return True


if __name__ == "__main__":
    import sys
    assert len(sys.argv) > 1, "You're supposed to give a json filename as argument"

    filename = sys.argv[1]
    print("Testing", filename)

    ok = test_schema(filename)
    
    if ok:
        print("..OK")
