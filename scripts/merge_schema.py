#! /usr/bin/python3
import json
import sys

def load_schema(filepath):
    raw_data = ''
    with open(filepath, 'r') as f:
        raw_data = f.read()
    data = json.loads(raw_data)
    return data
 
def process_schema(schema1, schema2):
    assert(schema1 and schema2)
    version1 = schema1['version']
    version2 = schema2['version']
    assert(version1 == version2)
    print('schema version: %s' % (version1))
    result1 = schema1['results']
    result2 = schema2['results']
    print('schema1: %d' % (len(result1)))
    print('schema2: %d' % (len(result2)))

    invt = dict()
    for item in result1:
        key = item['path'] + '.' + item['name']
        invt[key] = item
    
    for item in result2:
        key = item['path'] + '.' + item['name']
        if key in invt:
            continue
        else:
            invt[key] = item
    print('after merge: %d' % (len(invt)))

    new_schema = dict()
    for key in schema1:
        item = schema1[key]
        if key != 'results':
            new_schema[key] = item
        else:
            new_schema[key] = [invt[_key] for _key in invt]
    return json.dumps(new_schema, indent=2)


if __name__ == '__main__':
    print('merge %s and %s' % (sys.argv[1], sys.argv[2]))
    schema1 = load_schema(sys.argv[1])
    schema2 = load_schema(sys.argv[2])
    new_schema = process_schema(schema1, schema2)
    with open(sys.argv[3], 'w') as f:
        f.write(new_schema)


