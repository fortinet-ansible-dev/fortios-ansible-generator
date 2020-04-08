#! /usr/bin/python3
import os
import sys
import json
import yaml
import importlib

def absolute_path(path):
    cwd = os.getcwd()
    cpath = path.strip(' ')
    if cpath[0] == '/':
        return cpath
    return "%s/%s" % (cwd, cpath)

def array_to_string(arr):
    data = ''
    first = True
    for item in arr:
        if not first:
            data += ', '
        data += str(item)
        first = False
    return data

def generate_parameters(params, layer):
    ddata = ''
    for key in params:
        param = params[key]
        assert('type' in param)
        key_desc = param['description'][0] if 'description' in param else 'no description'
        key_type = param['type']
        if key_type in ['str', 'bool', 'int'] or (key_type == 'list' and 'choices' in param):
            ddata += ' ' * layer * 4 + '<li>'
            ddata += ' <span class="li-head">' + key + '</span>'
            ddata += ' - %s' % (key_desc)
            ddata += ' <span class="li-normal">type: %s</span>' % (key_type)
            if 'required' in param:
                ddata += ' <span class="li-required">required: %s</span>' % (param['required'])
            if 'default' in param:
                ddata += ' <span class="li-normal">default: %s</span>' % (param['default'])
            if 'choices' in param:
                ddata += ' <span class="li-normal">choices: %s</span>' % (array_to_string(param['choices']))
            ddata += '</li>\n'
        elif key_type == 'dict' or (key_type == 'list' and 'suboptions' in param):
            ddata += ' ' * layer * 4 + '<li>'
            ddata += ' <span class="li-head">' + key + '</span>'
            ddata += ' - %s' % (key_desc)
            ddata += ' <span class="li-normal">type: %s</span>' % (key_type)
            ddata += '</li>\n'
            ddata += ' ' * (layer + 1) * 4 + '<ul class="ul-self">\n'
            assert('suboptions' in param)
            ddata += generate_parameters(param['suboptions'], layer + 1)
            ddata += ' ' * (layer + 1) * 4 + '</ul>\n'
        else:
            
            print('incomplete schema: key:%s key_type:%s' % (key, key_type))
           #assert(False)
    return ddata

def format_example(example):
    ddata = ''
    for line in example.splitlines():
        ddata += '    ' + line + '\n'
    return ddata
def generate_return(doc_ret):
    ddata = ''
    for key in doc_ret:
        item = doc_ret[key]
        key_type = item['type']
        key_desc = item['description'] if 'description' in item else 'No decription'
        ddata += '    <li>'
        ddata += ' <span class="li-return">%s</span>' % (key)
        ddata += ' - %s' % (key_desc)
        if 'returned' in item:
            ddata += ' <span class="li-normal">returned: %s</span>' % (item['returned'])
        ddata += ' <span class="li-normal">type: %s</span>' % (key_type)
        if 'sample' in item:
            ddata += ' <span class="li-normal">sample: %s</span>' % (item['sample'])
        ddata += '</li>\n'
    return ddata

def generate_document(mod, dst):
    ddata = ''
    mod_doc = yaml.load(mod.DOCUMENTATION)
    mod_name = mod_doc['module']
    mod_sht_desc = mod_doc['short_description']

    ddata += ':source: %s.py\n\n'  % (mod_name)
    ddata += ':orphan:\n\n'
    ddata += '.. %s:\n\n' %(mod_name)
    
    short_desc = '%s -- %s' % (mod_name, mod_sht_desc)
    ddata += short_desc + '\n'
    ddata += '+' * len(short_desc) + '\n\n'

    ddata += '.. versionadded:: %s\n\n' % (mod_doc['version_added'])

    ddata += '.. contents::\n'
    ddata += '   :local:\n'
    ddata += '   :depth: 1\n\n\n'

    ddata += 'Synopsis\n'
    ddata += '--------\n'

    for item in mod_doc['description']:
        ddata += '- %s\n' % (item)
    ddata += '\n\n\n'

    ddata += 'Requirements\n'
    ddata += '------------\n'
    ddata += 'The below requirements are needed on the host that executes this module.\n\n'
    
    for item in mod_doc['requirements']:
        ddata += '- %s\n' % (item)
    ddata += '\n\n'

    ddata += 'Parameters\n'
    ddata += '----------\n\n\n'
    ddata += '.. raw:: html\n\n'
    ddata += '    <ul>\n'
    ddata += generate_parameters(mod_doc['options'], 1)
    ddata += '    </ul>\n\n\n'

    ddata += 'Notes\n'
    ddata += '-----\n\n'
    ddata += '.. note::\n\n'
    for item in mod_doc['notes']:
        ddata += '   - %s\n\n' % (item)
    ddata += '\n\n'
   
    ddata += 'Examples\n'
    ddata += '--------\n\n'
    ddata += '.. code-block:: yaml+jinja\n'
    ddata += format_example(mod.EXAMPLES)

    ddata += '\n\n'
    ddata += 'Return Values\n'
    ddata += '-------------\n'
    ddata += 'Common return values are documented: https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values, the following are the fields unique to this module:\n\n'
    ddata += '.. raw:: html\n\n'

    mod_ret = yaml.load(mod.RETURN)
    ddata += '    ' + '<ul>\n\n'
    ddata += generate_return(mod_ret)
    ddata += '    ' + '</ul>\n\n'

    ddata += 'Status\n'
    ddata += '------\n\n'
    ddata += '- This module is not guaranteed to have a backwards compatible interface.\n\n\n'

    ddata += 'Authors\n'
    ddata += '-------\n\n'

    for item in mod_doc['author']:
        ddata += '- %s\n' % (item)
    ddata += '\n\n'

    ddata += '.. hint::\n'
    ddata += '    If you notice any issues in this documentation, you can create a pull request to improve it.\n'

    with open(dst, 'w') as f:
        f.write(ddata)


def main():
    if len(sys.argv) != 3:
        print('incomplete arguments list')
        sys.exit(-1)
    src = absolute_path(sys.argv[1])
    dst = absolute_path(sys.argv[2])
    if not os.path.isfile(src):
        raise Exception('source file not given')
    dirname = os.path.dirname(src)
    sys.path.append(dirname)
    basename = os.path.basename(src)

    if not basename.endswith('.py'):
        raise Exception('source file is not a Python file')
    modname = basename[:-3]
    mod = importlib.import_module(modname)
    generate_document(mod, dst)
    
if __name__ == '__main__':
    main()
