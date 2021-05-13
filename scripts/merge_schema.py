#! /usr/bin/python3
import json
import sys

def load_schema(filepath):
    raw_data = ''
    with open(filepath, 'r') as f:
        raw_data = f.read()
    data = json.loads(raw_data)
    return data

def _tag_api_item(api_item, version, state=True):
    rdata = dict()
    for key in api_item:
        value = api_item[key]
        rdata[key] = value
    rdata['revisions'] = dict()
    rdata['revisions'][version] = state
    if 'schema' in api_item and type(api_item['schema']) is dict:
        rdata['schema'] = _tag_api_item(api_item['schema'], version, state=state)
    if 'children' in api_item:
        for name in api_item['children']:
            rdata['children'][name] = _tag_api_item(api_item['children'][name], version, state=state)
    if 'options' in api_item:
        assert(type(api_item['options']) is list)
        rdata['options'] = list()
        for option in api_item['options']:
            assert(type(option) is dict)
            revised_option = dict()
            for _key in option:
                revised_option[_key] = option[_key]
            revised_option['revisions'] = dict()
            revised_option['revisions'][version] = state
            rdata['options'].append(revised_option)
    return rdata

def _merge_api_item(api_item0, api_item1, version):
    rdata = dict()
    for key in api_item0:
        value = api_item0[key]
        rdata[key] = value
    assert('revisions' in rdata and type(rdata) is dict)
    rdata['revisions'][version] = True
    # for those removed items
    for key in rdata:
        value = rdata[key]
        if key == 'children' and type(value) is dict:
            for child in rdata[key]:
                child_value = rdata[key][child]
                if 'children' not in api_item1 or child not in api_item1['children']:
                    assert('revisions' in child_value)
                    child_value['revisions'][version] = False

    # for those present and new items.
    for key in api_item1:
        value = api_item1[key]
        if key == 'schema' and type(value) is dict:
            assert(key in rdata)
            assert(type(rdata[key]) is dict)
            rdata[key] = _merge_api_item(rdata[key], value, version)
        elif key == 'children' and type(value) is dict:
            #assert(key in rdata)
            if key not in rdata:
                rdata[key] = dict()
            assert(type(rdata[key]) is dict)
            for child in value:
                child_value = value[child]
                if child in rdata[key]:
                    rdata[key][child] = _merge_api_item(rdata[key][child], child_value, version)
                else:
                    rdata[key][child] = _tag_api_item(child_value, version, True)
        elif key == 'options' and type(value) is list:
            #assert(key in rdata)
            if key not in rdata:
                rdata[key] = list()
            assert(type(rdata[key]) is list)
            for option in value:
                assert(type(option) is dict)
                assert('name' in option)
                option_name = option['name']
                option_present = False
                for i in range(len(rdata[key])):
                    assert('name' in rdata[key][i])
                    if rdata[key][i]['name'] == option_name:
                        assert('revisions' in rdata[key][i])
                        rdata[key][i]['revisions'][version] = True
                        option_present = True
                        break
                if not option_present:
                    new_option = dict()
                    for attr in option:
                        new_option[attr] = option[attr]
                    new_option['revisions'] = dict()
                    new_option['revisions'][version] = True
                    rdata[key].append(new_option)
            for option in rdata[key]:
                assert(type(option) is dict)
                assert('name' in option)
                option_name = option['name']
                option_present = False
                for i in range(len(value)):
                    assert('name' in value[i])
                    if value[i]['name'] == option_name:
                        option_present = True
                        break
                if not option_present:
                    assert('revisions' in option)
                    option['revisions'][version] = False
        else:
            pass
            # FIXED: fix attributes which are different in later versions and new attributes. even though they are not fatal.
            #assert(type(value) in [int, str, bool])
            if key not in rdata:
                rdata[key] = value
            #print(rdata[key], value)
            #assert(rdata[key] == value)


    return rdata

def merge_schema(schemas):
    super_schema = dict()
    super_version = None
    schemas.sort(key=lambda item: item['version'])

    for schema in schemas:
        version = schema['version']
        build = schema['build']
        version_split = version.split('.')
        #if not super_version:
        #    super_version = version_split[:2]
        #else:
        #    assert(super_version[0] == version_split[0])
        #    assert(super_version[1] == version_split[1])
        sub_schemas = schema['results']
        print("merging schema version:%s, build:%s, number of items:%d" % (version, build, len(sub_schemas)))
        for api_item in sub_schemas:
            assert (len(api_item) == 3)
            api_path = '%s-%s' % (api_item['path'], api_item['name'])
            if api_path not in super_schema:
                super_schema[api_path] = _tag_api_item(api_item, version)
            else:
                super_schema[api_path] = _merge_api_item(super_schema[api_path], api_item, version)
    super_top_schema = dict()
    super_top_schema['version'] = 'v6.0.0'
    super_top_schema['action'] = 'schema'
    super_top_schema['results'] = [super_schema[api_path] for api_path in super_schema]
    with open('./fgt_schema.json', 'w') as f:
        f.write(json.dumps(super_top_schema, indent=2))
        f.flush()

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
    schemas = list()
    for i in range(1, len(sys.argv)):
        schemas.append(load_schema(sys.argv[i]))
    merge_schema(schemas)


