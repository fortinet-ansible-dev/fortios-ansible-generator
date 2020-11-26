
Run Your First Playbook
==============================

This document explains how to run your first FortiOS Ansible playbook.

--------------

With FortiOS Galaxy collection, you are always recommended to run
FortiOS module in ``httpapi`` manner. The first step is to prepare your
host inventory with which you can use ``ansible-vault`` to encrypt or
decrypt your secrets for the sake of confidentiality.

Prepare host inventory
~~~~~~~~~~~~~~~~~~~~~~

in our case we create a file named ``hosts``:

::

   [fortigates]
   fortigate01 ansible_host=192.168.190.130 ansible_user="admin" ansible_password="password"
   fortigate02 ansible_host=192.168.190.131 ansible_user="admin" ansible_password="password"
   fortigate03 ansible_host=192.168.190.132 fortios_access_token=<your access token>

   [fortigates:vars]
   ansible_network_os=fortinet.fortios.fortios

FortiOS supports two ways to authenticate Ansible: ``ansible_user`` and ``ansible_password`` pair based; ``fortios_access_token`` access token based.
Access token based way is prefered as it is safer without any password explosure and access token guarantees request source location is wanted. 


for how to generate an API token, visit page `FortiOS API Spec`_.


Write the playbook
~~~~~~~~~~~~~~~~~~

in the example: ``test.yml`` we are going to modify the fortigate
device’s hostname:

::

   - hosts: fortigate03
     connection: httpapi
     collections:
     - fortinet.fortios
     vars:
      vdom: "root"
      ansible_httpapi_use_ssl: yes
      ansible_httpapi_validate_certs: no
      ansible_httpapi_port: 443
     tasks:
      - name: Configure global attributes.
        fortios_system_global:
           vdom:  "{{ vdom }}"
           access_token: "{{ fortios_access_token }}" #if you prefer access token based authentication, add this line.
           system_global:
               hostname: 'CustomHostName'

there are several options which might need you special care:

-  **connection** : ``httpapi`` is preferred.
-  **collections** : The namespace must be ``fortinet.fortios``
-  **ansible_httpapi_use_ssl** and **ansible_httpapi_port**: by
   default when your fortiOS device is licensed, the https is enabled.
   there is one exception: module ``fortios_system_vmlicense`` allows
   you to upload the licence with http, in this case, you should set
   ``ansible_httpapi_use_ssl: no`` and ``ansible_httpapi_port: 80``

Run the playbook
~~~~~~~~~~~~~~~~

::

   ansible-playbook -i hosts test.yml

you can also observe the verbose output by adding option at the tail:
``-vvv``.

.. _FortiOS API Spec: https://fndn.fortinet.net/index.php?/fortiapi/1-fortios/92/
