#! /usr/bin/python3
import json
import sys

def load_schema(filepath):
    raw_data = ''
    with open(filepath, 'r') as f:
        raw_data = f.read()
    data = json.loads(raw_data)
    return data

def merge_schema(schemas):
    super_schema = dict()
    super_version = None
    schemas.sort(key=lambda item: item['version'])

    for schema in schemas:
        version = schema['version']
        build = schema['build']
        version_split = version.split('.')
        sub_schemas = schema['directory']
        print("merging schema version:%s, build:%s, number of items:%d" % (version, build, len(sub_schemas)))
        for item in sub_schemas:
            key = '%s.%s.%s' % (item['path'], item['name'], item['action'])
            if key not in super_schema:
                print('    new item: %s' % (key))
            super_schema[key] = item

    super_top_schema = dict()
    super_top_schema['version'] = 'v6.0.0'
    super_top_schema['directory'] = [super_schema[api_key] for api_key in super_schema]
    with open('./monitor_schema.json', 'w') as f:
        f.write(json.dumps(super_top_schema, indent=2))
        f.flush()



if __name__ == '__main__':
    schemas = list()
    for i in range(1, len(sys.argv)):
        schemas.append(load_schema(sys.argv[i]))
    merge_schema(schemas)


