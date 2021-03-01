from jinja2 import Template, Environment, FileSystemLoader
import json
import os

def generate_cofiguration_fact_rst(schema_results, version):
    file_loader = FileSystemLoader('ansible_templates')
    env = Environment(loader=file_loader,
                      lstrip_blocks=False, trim_blocks=False)
    template = env.get_template('configuration_fact.rst.j2')

    selectors = dict()
    for schema_result in schema_results:
        selector = schema_result['path'] + "_" + schema_result['name']
        mkey = schema_result['schema'].get('mkey', None)
        mkey_type = schema_result['schema'].get('mkey_type', None)
        if mkey_type == 'integer':
            mkey_type = 'int'
        elif mkey_type:
            mkey_type = 'str'
        else:
            assert(mkey_type == None)
        selectors[selector] =dict()
        selectors[selector]['mkey'] = mkey
        selectors[selector]['mkey_type'] = mkey_type
    data = template.render(selectors=selectors)

    output_path = 'output/' + version + '/fortios_configuration_fact.rst'
    with open(output_path, 'w') as f:
        f.write(data)
        f.flush()


def generate_monitor_fact(version):
    monitor_schema_file = open('monitor_schema.json').read()
    monitor_schema = json.loads(monitor_schema_file)
    get_api_items = dict()
    assert('directory' in monitor_schema)
    for api_item in monitor_schema['directory']:
        assert('request' in api_item)
        assert('http_method' in api_item['request'])
        if api_item['request']['http_method'] != 'GET':
            continue
        path = api_item['path']
        name = api_item['name']
        action = api_item['action']
        key = '%s/%s' % (path, name)
        if action != 'select':
            key = '%s/%s' % (key, action)
        assert(key not in get_api_items)
        get_api_items[key] = api_item
    schemas = dict()
    for api_item_key in get_api_items:
        api_item = get_api_items[api_item_key]
        selector = api_item_key.replace('/', '_')
        assert(selector not in schemas)
        schemas[selector] = dict()
        schemas[selector]['url'] = api_item_key
        schemas[selector]['params'] = dict()
        assert(api_item['request']['http_method'] == 'GET')
        if 'parameters' in api_item['request']:
            for param in api_item['request']['parameters']:
                param_name = param['name']
                param_type = param['type']
                param_desc = param['summary'] if 'summary' in param else ''
                schemas[selector]['params'][param_name] = dict()
                schemas[selector]['params'][param_name]['type'] = param_type
                schemas[selector]['params'][param_name]['description'] = param_desc
                schemas[selector]['description'] = api_item['summary'] if 'summary' in api_item else ''
    file_loader = FileSystemLoader('ansible_templates')
    env = Environment(loader=file_loader,
                      lstrip_blocks=False, trim_blocks=False)

    # Render module code
    template = env.get_template('monitor_fact.j2')
    data = template.render(selectors=schemas)
    output_path = 'output/' + version + '/fortios_monitor_fact.py'
    with open(output_path, 'w') as f:
        f.write(data)
        f.flush()
    # Render Sphinx doc
    template = env.get_template('monitor_fact.rst.j2')
    data = template.render(selectors=schemas)
    output_path = 'output/' + version + '/fortios_monitor_fact.rst'
    with open(output_path, 'w') as f:
        f.write(data)
        f.flush()


def monitor_schema_to_module_spec(monitor_params):
    rdata = dict()
    for param in monitor_params:
        key = param['name']
        rdata[key] = dict()
        if param['type'] == 'string':
            rdata[key]['type'] = 'str'
        elif param['type'] == 'Integer':
            rdata[key]['type'] = 'int'
        elif param['type'] == 'int':
            rdata[key]['type'] = 'int'
        elif param['type'] == 'array':
            rdata[key]['type'] = 'list'
        elif param['type'] == 'boolean':
            rdata[key]['type'] = 'boolean'
        else:
            raise Exception("Data type is not supported " + param['type'])

        rdata[key]['description'] = param['summary'] if param['summary'] else ''
        rdata[key]['required'] = param['required'] if 'required' in param else False

    return rdata


def generate_monitor_modules(version):
    # Init template to generate a single module
    file_loader = FileSystemLoader('ansible_templates')
    env = Environment(loader=file_loader,
                      lstrip_blocks=False, trim_blocks=False)
    template = env.get_template('monitor_config.j2')

    monitor_schema_file = open('monitor_schema.json').read()
    monitor_schema = json.loads(monitor_schema_file)
    get_api_items = dict()
    assert('directory' in monitor_schema)
    for api_item in monitor_schema['directory']:
        assert('request' in api_item)
        assert('http_method' in api_item['request'])
        if api_item['request']['http_method'] != 'POST':
            continue
        path = api_item['path']
        original_name = api_item['name']
        name = original_name.replace('-', '_')
        original_action = api_item['action']
        action = original_action.replace('-', '_')
        key = '%s_%s_%s' % (path, name, action)
        print('Generate module for ' + key)

        monitor_params = monitor_schema_to_module_spec(api_item['request']['parameters']) if 'parameters' in api_item['request'] else {}
        #assert(key not in get_api_items)
        #get_api_items[key] = api_item


        data = template.render(**locals())
        output_path = 'output/' + version + '/fortios_monitor_' + key + '.py'
        with open(output_path, 'w') as f:
            f.write(data)
            f.flush()


    print('api_item:', get_api_items)

if __name__ == '__main__':
    #generate_cofiguration_fact_rst()
    #generate_monitor_fact('v6.0.0')
    generate_monitor_modules('v6.4.0')
