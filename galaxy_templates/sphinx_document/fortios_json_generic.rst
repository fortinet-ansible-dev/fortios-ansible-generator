:source: fortios_json_generic.py

:orphan:

.. :

.. _fortios_json_generic:

fortios_json_generic -- Configure Fortinet's FortiOS and FortiGate with json generic method.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 1


Synopsis
--------
This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the user to set any category supported by FortiAPI with raw json. All parameters and values included in examples need to be adjusted to datasources before usage. 


Requirements
-------------
The below requirements are needed on the host that executes this module.

- install galaxy collection ``fortinet.fortios`` >= 2.0.0


Parameters
----------

.. raw:: html

    <ul>

    <li><span class="li-head">vdom</span> - Virtual domain, among those defined previously. A vdom is a virtual instance of the FortiGate that can be configured and used as a different unit. <span class="li-normal">type: str</span> <span class="li-normal">default: root</span></li>
    <li> <span class="li-head">access_token</span> - Token-based authentication. Generated from GUI of Fortigate. <span class="li-normal">type: str</span> <span class="li-required">required: False</span> </li>
    <li><span class="li-head">json_generic</span> - json generic <span class="li-normal">default: null</span> <span class="li-normal">type: dict</span></li>
            <ul class="ul-self">
            <li><span class="li-head">dictbody</span> - Body with YAML list of key/value format <span class="li-normal">type: dict</span></li>
            <li><span class="li-head">jsonbody</span> - Body with JSON string format, will always give priority to jsonbody <span class="li-normal">type: str</span></li>
            <li><span class="li-head">method</span> - HTTP methods <span class="li-normal">type: str</span> <span class="li-normal">choices: GET,  PUT,  POST,  DELETE</span></li>
            <li><span class="li-head">path</span> - URL path, e.g./api/v2/cmdb/firewall/address <span class="li-normal">type: str</span></li>
            <li><span class="li-head">specialparams</span> - Extra URL parameters, e.g.start=1&count=10 <span class="li-normal">type: str</span>
            </ul>

    </ul>




Examples
--------

**host**

.. code-block:: yaml+jinja

    [fortigates]
    fortigate01 ansible_host=192.168.52.177 ansible_user="admin" ansible_password="admin"

    [fortigates:vars]
    ansible_network_os=fortios


**sample1.yml**

.. code-block:: yaml+jinja

    ---
    - hosts: fortigates
      connection: httpapi
      collections:
        - fortinet.fortios
      vars:
       vdom: "root"
       ansible_httpapi_use_ssl: yes
       ansible_httpapi_validate_certs: no
       ansible_httpapi_port: 443

      tasks:
      - name: test add with string
        fortios_json_generic:
          vdom:  "{{ vdom }}"
          json_generic:
            method: "POST"
            path: "/api/v2/cmdb/firewall/address"
            jsonbody: |
              {
              "name": "111",
              "type": "geography",
              "fqdn": "",
              "country": "AL",
              "comment": "ccc",
              "visibility": "enable",
              "associated-interface": "port1",
              "allow-routing": "disable"
              }
        register: info
        
      - name: display vars
        debug: msg="{{info}}" 
        
**sample2.yml**

.. code-block:: yaml+jinja

    ---
    - hosts: fortigates
      connection: httpapi
      collections:
        - fortinet.fortios
      vars:
       vdom: "root"
       ansible_httpapi_use_ssl: yes
       ansible_httpapi_validate_certs: no
       ansible_httpapi_port: 443

      tasks:
      - name: test delete
        fortios_json_generic:
          vdom:  "{{ vdom }}"
          json_generic:
            method: "DELETE"
            path: "/api/v2/cmdb/firewall/address/111"
            specialparams: "testpara1=1&testpara2=2"
        register: info
        
      - name: display vars
        debug: msg="{{info}}"

      - name: test add with dict
        fortios_json_generic:
          vdom:  "{{ vdom }}"
          json_generic:
            method: "POST"
            path: "/api/v2/cmdb/firewall/address"
            dictbody:
              name: "111"
              type: "geography"
              fqdn: ""
              country: "AL"
              comment: "ccc"
              visibility: "enable"
              associated-interface: "port1"
              allow-routing: "disable"
        register: info
        
      - name: display vars
        debug: msg="{{info}}"    
        
      - name: test delete
        fortios_json_generic:
          vdom:  "{{ vdom }}"
          json_generic:
            method: "DELETE"
            path: "/api/v2/cmdb/firewall/address/111"
        register: info
        
      - name: display vars
        debug: msg="{{info}}"

      - name: test add with string
        fortios_json_generic:
          vdom:  "{{ vdom }}"
          json_generic:
            method: "POST"
            path: "/api/v2/cmdb/firewall/address"
            jsonbody: |
              {
              "name": "111",
              "type": "geography",
              "fqdn": "",
              "country": "AL",
              "comment": "ccc",
              "visibility": "enable",
              "associated-interface": "port1",
              "allow-routing": "disable"
              }
        register: info
        
      - name: display vars
        debug: msg="{{info}}" 
        

**sample3.yml**

.. code-block:: yaml+jinja

    ---
    - hosts: fortigates
      collections:
        - fortinet.fortios
      connection: httpapi
      vars:
       vdom: "root"
       ansible_httpapi_use_ssl: yes
       ansible_httpapi_validate_certs: no
       ansible_httpapi_port: 443

      tasks:
      - name: test firewall policy order modification
    	fortios_json_generic:
    	  vdom:  "{{ vdom }}"
    	  json_generic:
    		method: "PUT"
    		path: "/api/v2/cmdb/firewall/policy/1"
    		specialparams: "action=move&after=2"
    	register: info
    	
      - name: display vars
    	debug: msg="{{info}}"
    



Return Values
-------------
Common return values are documented: https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values, the following are the fields unique to this module:

.. raw:: html

    <ul>

    <li><span class="li-return">build</span> - Build number of the fortigate image <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: '1547'</span></li>
    <li><span class="li-return">http_method</span> - Last method used to provision the content into FortiGate <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: 'PUT'</span></li>
    <li><span class="li-return">http_status</span> - Last result given by FortiGate on last operation applied <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: 200</span></li>
    <li><span class="li-return">mkey</span> - Master key (id) used in the last call to FortiGate <span class="li-normal">returned: success</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: id</span></li>
    <li><span class="li-return">name</span> - Name of the table used to fulfill the request <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: urlfilter</span></li>
    <li><span class="li-return">path</span> - Path of the table used to fulfill the request <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: webfilter</span></li>
    <li><span class="li-return">revision</span> - Internal revision number <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: 17.0.2.10658</span></li>
    <li><span class="li-return">serial</span> - Serial number of the unit <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: FGVMEVYYQT3AB5352</span></li>
    <li><span class="li-return">status</span> - Indication of the operation's result <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: success</span></li>
    <li><span class="li-return">vdom</span> - Virtual domain used <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: root</span></li>
    <li><span class="li-return">version</span> - Version of the FortiGate <span class="li-normal">returned: always</span> <span class="li-normal">type: str</span> <span class="li-normal">sample: v5.6.3</span></li>
    </ul>



Status
------

- This module is ported from https://github.com/fortinet/ansible-fortios-generic


Authors
-------
- Link Zheng (@chillancezen)
- Jie Xue (@JieX19)
- Frank Shen (@fshen01)
- Hongbin Lu (@fgtdev-hblu)




Warning
-------
It's preferred to use ``FortiOS Ansible Collection Included Modules`` unless some features are not available there.
