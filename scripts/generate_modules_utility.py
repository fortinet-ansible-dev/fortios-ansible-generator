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

if __name__ == '__main__':
    generate_cofiguration_fact_rst()
