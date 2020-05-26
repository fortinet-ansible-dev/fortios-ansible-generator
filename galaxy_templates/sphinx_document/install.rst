
Install FortiOS Ansible Galaxy
==============================

This document explains how to install the FortiOS Ansible Galaxy
Collection.

--------------

Install Python3
~~~~~~~~~~~~~~~

-  Follow steps in https://www.python.org/ to install Python3 on your
   host.

Install Ansible Core
~~~~~~~~~~~~~~~~~~~~

-  Follow instructions in
   https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
   to install Ansible
-  The Ansible core version requirement: >= 2.9.0

Install FortiOS Galaxy Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The FortiOS Ansible Galaxy supports multilple FortiOS major releases,
you can install the latest collection by default via command
``ansible-galaxy collection install fortinet.fortios``. you can also
choose another galaxy version to match your FortiOS device.

Please see the `versionig notes`_ for more recently released collections
and install the ones which are marked ``latest`` for your devices.

.. _versionig notes: version.html

