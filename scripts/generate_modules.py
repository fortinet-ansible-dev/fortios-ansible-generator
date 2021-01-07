#!/usr/bin/python
from jinja2 import Template, Environment, FileSystemLoader
import json
import autopep8
import os
import re
import sys

def replaceSpecialChars(str):
    return str.replace('-', '_').replace('.', '_').replace('+', 'plus')


def getModuleName(path, name):
    return replaceSpecialChars(path.lower()) + "_" + replaceSpecialChars(name.lower())


def searchProperBreakableChar(line, startingPosition):
    breakableChars = " :.,;"
    for i in reversed(range(0, startingPosition)):
        if line[i] in breakableChars:
            return i
    return startingPosition


def numberOfInitialSpaces(line):
    return len(line) - len(line.lstrip()) + 2


def splitLargeLines(output):
    output = output.splitlines()
    for i in range(0, len(output)):
        line = output[i]
        if len(line) > 159:
            position = searchProperBreakableChar(line, 159)
            initialSpaces = " " * numberOfInitialSpaces(output[i])
            output.insert(i + 1, initialSpaces + line[position:])
            output[i] = output[i][:position]
    output = '\n'.join(output)
    return output


def calculateFullPath(parent_attrs, attribute_name):
    return attribute_name if not parent_attrs else parent_attrs + ',' + attribute_name


def hyphenToUnderscore(data):
    if isinstance(data, list):
        for elem in data:
            elem = hyphenToUnderscore(elem)
        return data
    elif isinstance(data, dict):
        for k, v in data.items():
            if not (len(data) == 2 and 'name' in data and 'help' in data) and \
                k != 'help':
                # Only change hyphens for names and complex types.
                # Simple types (enums) only contain name and help
                # Also, avoid changing hyphens in 'help' attributes
                data[k] = hyphenToUnderscore(v)
        return data
    elif isinstance(data, str):
        return data.replace('-', '_')
    elif isinstance(data, unicode):
        return data.encode('utf-8').replace('-', '_')
    else:
        return data

def invalid_attr_to_valid_attr(data, valid_identifiers):
    if (valid_identifiers.has_key(data)):
        return valid_identifiers[data]
    return data

def invalid_attr_to_valid_attrs(data, valid_identifiers, valid_identifiers_module):
    if isinstance(data, list):
        for elem in data:
            elem = invalid_attr_to_valid_attrs(elem, valid_identifiers, valid_identifiers_module)
        return data
    elif isinstance(data, dict):
        for k, v in data.items():
            if not (len(data) == 2 and 'name' in data and 'help' in data) and \
                k != 'help':
                data[k] = invalid_attr_to_valid_attrs(v, valid_identifiers, valid_identifiers_module)
        return data
    elif isinstance(data, str):
        data1 = invalid_attr_to_valid_attr(data, valid_identifiers)
        if data1 != data:
            valid_identifiers_module[data] = valid_identifiers[data]
        return data1
    elif isinstance(data, unicode):
        data1 = invalid_attr_to_valid_attr(data.encode('utf-8'), valid_identifiers)
        if data1 != data:
            valid_identifiers_module[data] = valid_identifiers[data]
        return data1
    else:
        return data

def removeDefaultCommentsInFGTDoc(str):
    regex = r"(-.*\(.*?)(, ){0,1}([D|d]efault[ |:|=\n]+.*)(\))"
    str = re.sub(regex, r"\g<1>\g<4>", str)

    regex = r"(-.*)\(\)"
    str = re.sub(regex, r"\g<1>", str)
    return str

def renderModule(schema, version, special_attributes, valid_identifiers, version_added, supports_check_mode, movable=False):

    # Generate module
    versioned_schema = json.dumps(generate_versioned_fields(schema['schema']), indent=4).replace('": false', '": False').replace('": true', '": True')
    file_loader = FileSystemLoader('ansible_templates')
    env = Environment(loader=file_loader,
                      lstrip_blocks=False, trim_blocks=False)
    if 'children' not in schema['schema']:
        print('warning: not a valid schema, skip.')
        return

    schema['schema'] = hyphenToUnderscore(schema['schema'])

    valid_identifiers_module = {}
    schema['schema']['children'] = invalid_attr_to_valid_attrs(schema['schema']['children'], valid_identifiers, valid_identifiers_module)

    short_description = schema['schema']['help'][:-1] + " in Fortinet's FortiOS and FortiGate."
    description = ""
    original_path = schema['path']
    original_name = schema['name']
    path = replaceSpecialChars(original_path).lower()
    name = replaceSpecialChars(original_name).lower()
    module_name = "fortios_" + path + "_" + name
    if module_name in version_added:
        module_version_added = version_added[module_name]
    else:
        module_version_added = '2.10'
    #try:
    #    module_version_added = version_added[module_name]
    #except KeyError:
    #    print("cannot find", module_name)
    #    return

    mkeyname = None
    if 'mkey' in schema['schema']:
        mkeyname = schema['schema']['mkey']

    special_attributes_flattened = [','.join(x for x in elem) for elem in special_attributes]

    template = env.get_template('doc.j2')
    output = template.render(calculateFullPath=calculateFullPath, **locals())

    template = env.get_template('examples.j2')
    output += template.render(**locals())

    template = env.get_template('return.j2')
    output += template.render(**locals())

    template = env.get_template('code.j2')
    output += template.render(calculateFullPath=calculateFullPath, vi=valid_identifiers_module, **locals())

    dir = 'output/' + version + '/' + path
    if not os.path.exists(dir):
        os.makedirs(dir)

    file = open('output/' + version + '/' + path + '/fortios_' + path + '_' + name + '.py', 'w')
    output = removeDefaultCommentsInFGTDoc(output)
    output = splitLargeLines(output)
    file.write(output)
    file.close()

    # Generate example
    file_example = open('output/' + version + '/' + path + '/fortios_' + path +
                        '_' + name + '_example.yml', 'w')
    template = env.get_template('examples.j2')
    output = template.render(**locals())
    lines = output.splitlines(True)
    file_example.writelines(lines[2:-1])
    file_example.close()

    # Generate test
    file_example = open('output/' + version + '/' + path + '/test_fortios_' + path +
                        '_' + name + '.py', 'w')
    template = env.get_template('tests.j2')
    output = template.render(**locals())
    lines = output.splitlines(True)
    file_example.writelines(lines)
    file_example.close()

    print("\033[0mFile generated: " + 'output/' + version + '/\033[37mfortios_' + path + '_' + name + '.py')
    print("\033[0mFile generated: " + 'output/' + version + '/\033[37mfortios_' + path + '_' + name + '_example.yml')
    print("\033[0mFile generated: " + 'output/' + version + '/\033[37mtest_fortios_' + path + '_' + name + '.py')

def convert_mkey_type(mkey_type):
    if mkey_type is None:
        return None
    if mkey_type == 'integer':
        return 'int'
    return 'str'

def renderFactModule(schema_results, version):
    # Generate module
    file_loader = FileSystemLoader('ansible_templates')
    env = Environment(loader=file_loader,
                      lstrip_blocks=False, trim_blocks=False)

    template = env.get_template('fact.j2')

    selector_definitions = {
            schema_result['path'] + "_" + schema_result['name']: {
                'mkey': schema_result['schema'].get('mkey', None),
                'mkey_type': convert_mkey_type(schema_result['schema'].get('mkey_type', None)),
            }
            for schema_result in schema_results
            if 'diagnose' not in schema_result['path'] and 'execute' not in schema_result['path']
        }

    output = template.render(**locals())

    output_path = 'output/' + version + '/fortios_configuration_fact.py'
    file = open(output_path, 'w')
    output = splitLargeLines(output)
    file.write(output)
    file.close()

    print('generated config fact in ' + output_path)
    return output_path


def generate_versioned_fields(schema):
    rdata = dict()
    assert('category' in schema)
    assert('revisions' in schema)
    category = schema['category']
    if category == 'table':
        # payload as a list
        assert('children' in schema)
        rdata['type'] = 'list'
        rdata['children'] = dict()
        rdata['revisions'] = schema['revisions']
        for child in schema['children']:
            child_value = schema['children'][child]
            rdata['children'][child] = generate_versioned_fields(child_value)
    elif category == 'unitary':
        assert('type' in schema)
        rdata['revisions'] = schema['revisions']
        if schema['type'] in ['string', 'var-string', 'mac-address', 'user',
                              'ipv4-classnet-any', 'password', 'ipv4-address-any',
                              'ipv6-prefix', 'ipv4-address', 'ipv4-classnet-host',
                              'datetime', 'ipv4-classnet', 'password-2', 'ipv6-address',
                              'ipv4-netmask', 'ipv4-address-multicast', 'ipv4-netmask-any',
                              'uuid', 'ipv6-network', 'password-3', 'time', 'varlen_password']:
            rdata['type'] = 'string'
        elif schema['type'] == 'integer':
            rdata['type'] = 'integer'
        elif schema['type'] == 'option':
            assert('options' in schema)
            if not len(schema['options']):
                rdata['type'] = 'string' # default as string
            elif type(schema['options'][0]['name']) is int:
                rdata['type'] = 'integer'
            elif type(schema['options'][0]['name']) in [str, unicode]:
                rdata['type'] = 'string'
            else:
                assert(False)
            options = list()
            for option in schema['options']:
                options.append({'value': option['name'], 'revisions': option['revisions']})
            if len(options):
                rdata['options'] = options
        else:
            assert(False)
    elif category == 'complex':
        # payload as one unique item
        if 'children' in schema:
            assert('children' in schema)
            assert('revisions' in schema)
            rdata['revisions'] = schema['revisions']
            rdata['type'] = 'dict'
            rdata['children'] = dict()
            for child in schema['children']:
                child_value = schema['children'][child]
                rdata['children'][child] = generate_versioned_fields(child_value)
    else:
        assert(False)
    return rdata


def jinjaExecutor(number=None):

    fgt_schema_file = open('fgt_schema.json').read()
    fgt_schema = json.loads(fgt_schema_file)
    fgt_sch_results = fgt_schema['results']

    special_attributes_file = open('special_attributes.lst').read()
    special_attributes = json.loads(special_attributes_file)

    valid_identifiers_file = open('valid_identifiers.lst').read()
    valid_identifiers = json.loads(valid_identifiers_file)
    version_added_file = open('version_added.json').read()
    version_added_json = json.loads(version_added_file)
    check_mode_support_file = open('check_mode_support.txt').read()
    check_mode_support_set = set(check_mode_support_file.split('\n'))

    movable_modules_file = open('movable_modules.lst').read()
    movable_modules = json.loads(movable_modules_file)

    autopep_files = './output/' + fgt_schema['version']

    if not number:
        real_counter = 0
        for i, pn in enumerate(fgt_sch_results):
            if 'diagnose_' not in pn['path'] and 'execute_' not in pn['path'] and 'test' != pn['path']:
                module_name = getModuleName(pn['path'], pn['name'])
                print('\n\033[0mParsing schema:')
                print('\033[0mModule name: \033[92m' + module_name)
                print('\033[0mIteration:\033[93m' + str(real_counter) + "\033[0m, Schema position: \033[93m" + str(i))
                renderModule(fgt_sch_results[i],
                             fgt_schema['version'],
                             special_attributes[module_name] if module_name in special_attributes else [],
                             valid_identifiers,
                             version_added_json,
                             module_name in check_mode_support_set,
                             module_name in movable_modules)
                real_counter += 1
    else:
        module_name = getModuleName(fgt_sch_results[number]['path'], fgt_sch_results[number]['name'])
        renderModule(fgt_sch_results[number],
                     fgt_schema['version'],
                     special_attributes[module_name] if module_name in special_attributes else [],
                     valid_identifiers,
                     version_added_json,
                     module_name in check_mode_support_set)

        autopep_files = './output/' + \
                fgt_schema['version'] + '/' + \
                replaceSpecialChars(fgt_sch_results[number]['path']) + \
                '/fortios_' + replaceSpecialChars(fgt_sch_results[number]['path']) + '_' + replaceSpecialChars(fgt_sch_results[number]['name']) + '.py'

        autopep_files += ' ./output/' + \
                fgt_schema['version'] + '/' + \
                replaceSpecialChars(fgt_sch_results[number]['path']) + \
                '/test_fortios_' + replaceSpecialChars(fgt_sch_results[number]['path']) + '_' + replaceSpecialChars(fgt_sch_results[number]['name']) + '.py'


    autopep_files += ' ' + renderFactModule(fgt_sch_results, fgt_schema['version'])

    # there is an escape letter in fortios_vpn_ssl_settings.py, replace it.
    os.popen("sed -i 's/Encode \\\\2F sequence/Encode 2F sequence/g' ./output/" + fgt_schema['version'] + "/vpn_ssl/fortios_vpn_ssl_settings.py")

    # copy licence modules
    licence_output_folder = './output/' + fgt_schema['version'] + '/licence'
    os.popen('mkdir -p ' + licence_output_folder)
    os.popen('cp ./galaxy_templates/licence_modules/* ' + licence_output_folder)

    from generate_modules_utility import generate_cofiguration_fact_rst
    generate_cofiguration_fact_rst(fgt_sch_results, fgt_schema['version'])

    print("\n\n\033[0mExecuting autopep8 ....")
    # Note this is done with popen and not with autopep8.fix_code in order to get the multiprocessig optimization, only available from CLI
    os.popen('autopep8 --aggressive --max-line-length 160 --jobs 8 --ignore E402 --in-place --recursive ' + autopep_files)
    # Avoid this check since it conflicts with Ansible guidelines:
    # E402 - Fix module level import not at top of file

    # Fix exceptional issues due to bugs in autopep
    # Using os.popen for quick edit and modification. Should be replaced by proper Python calls
    print("\n\n\033[0mFinal fixes ....")
    os.popen("sed -i 's/filtered_data =/filtered_data = \\\/' ./output/" + fgt_schema['version'] + "/wireless_controller_hotspot20/fortios_wireless_controller_hotspot20_anqp_ip_address_type.py")
    os.popen("sed -i 's/filtered_data =/filtered_data = \\\/' ./output/" + fgt_schema['version'] + "/wireless_controller_hotspot20/fortios_wireless_controller_hotspot20_anqp_network_auth_type.py")
    os.popen("sed -i 's/filtered_data =/filtered_data = \\\/' ./output/" + fgt_schema['version'] + "/wireless_controller_hotspot20/fortios_wireless_controller_hotspot20_anqp_roaming_consortium.py")
    os.popen("sed -i 's/filtered_data =/filtered_data = \\\/' ./output/" + fgt_schema['version'] + "/wireless_controller_hotspot20/fortios_wireless_controller_hotspot20_h2qp_conn_capability.py")
    os.popen("sed -i 's/    underscore_to_hyphen/        underscore_to_hyphen/' ./output/" + fgt_schema['version'] + "/wireless_controller_hotspot20/fortios_wireless_controller_hotspot20_anqp_ip_address_type.py")
    os.popen("sed -i 's/    underscore_to_hyphen/        underscore_to_hyphen/' ./output/" + fgt_schema['version'] + "/wireless_controller_hotspot20/fortios_wireless_controller_hotspot20_anqp_network_auth_type.py")
    os.popen("sed -i 's/    underscore_to_hyphen/        underscore_to_hyphen/' ./output/" + fgt_schema['version'] + "/wireless_controller_hotspot20/fortios_wireless_controller_hotspot20_anqp_roaming_consortium.py")
    os.popen("sed -i 's/    underscore_to_hyphen/        underscore_to_hyphen/' ./output/" + fgt_schema['version'] + "/wireless_controller_hotspot20/fortios_wireless_controller_hotspot20_h2qp_conn_capability.py")
    os.popen("find . -name 'test_fortios_router_bfd*.py' -exec rm {} \\;")

if __name__ == "__main__":
    print("args " + str(sys.argv))
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else None
    jinjaExecutor(arg)
