
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
   fortigate01 ansible_host=192.168.190.131 ansible_user="admin" ansible_password="password"

   [fortigates:vars]
   ansible_network_os=fortinet.fortios.fortios

Write the playbook
~~~~~~~~~~~~~~~~~~

in the example: ``test.yml`` we are going to modify the fortigate
device’s hostname:

::

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
      - name: Configure global attributes.
        fortios_system_global:
           vdom:  "{{ vdom }}"
           system_global:
               hostname: 'CustomHostName'

there are several options which might need you special care:

-  **``connection``** : ``httpapi`` is preferred.
-  **``collections``** : The namespace must be ``fortinet.fortios``
-  **``ansible_httpapi_use_ssl``** and **``ansible_httpapi_port``**: by
   default when your fortiOS device is licensed, the https is enabled.
   there is one exception: module ``fortios_system_vmlicense`` allows
   you to upload the licence with http, in this case, you should set
   ``ansible_httpapi_use_ssl: no`` and ``ansible_httpapi_port: 80``
-  Don’t specify ``host``, ``username``, ``password``, ``https`` or
   ``ssl_verify`` under second level options(``fortios_system_global``
   in the above example)

Run the playbook
~~~~~~~~~~~~~~~~

::

   ansible-playbook -i hosts test.yml

you can also observe the verbose output by adding option at the tail:
``-vvv``.
