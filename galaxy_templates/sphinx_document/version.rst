FortiOS Galaxy Versioning
====================================

FortiOS Galaxy versions
~~~~~~~~~~~~~~~~~~~~~~~

From ``v2.0.0`` on, FortiOS galaxy collections are unified, there is only one sequential collection at any moment. users who install these collections
are expected to find the version compatibility information for each module and its parameters.

+---------------+---------------------+----------------+-----------------------------------------------------------------+
| FOS version   | Galaxy Version      | Release date   | Path to Install                                                 |
+===============+=====================+================+=================================================================+
| unified       | 2.0.0 ``latest``    | 2021/4/6      | ``ansible-galaxy collection install fortinet.fortios:2.0.0``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+

Legacy FortiOS Galaxy Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prior to FortiOS collection ``v2.0.0``, FortiOS Galaxy collections were built over three FOS major versions, i.e. ``v6.0``, ``v6.2`` and ``v6.4``, thus, users are expected to install
the collection according to the following table to avoid potential compatibility issues.


+---------------+---------------------+----------------+-----------------------------------------------------------------+
| FOS version   | Galaxy Version      | Release date   | Path to Install                                                 |
+===============+=====================+================+=================================================================+
| 6.0.0         | 1.0.13              | 2020/5/26      | ``ansible-galaxy collection install fortinet.fortios:1.0.13``   |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.0.0         | 1.1.2               | 2020/12/4      | ``ansible-galaxy collection install fortinet.fortios:1.1.2``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.0.0         | 1.1.5               | 2020/12/7      | ``ansible-galaxy collection install fortinet.fortios:1.1.5``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.0.0         | 1.1.8               | 2020/12/21     | ``ansible-galaxy collection install fortinet.fortios:1.1.8``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.0.0         | 1.1.9               | 2020/3/1       | ``ansible-galaxy collection install fortinet.fortios:1.1.9``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.2.0         | 1.0.10              | 2020/5/6       | ``ansible-galaxy collection install fortinet.fortios:1.0.10``   |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.2.0         | 1.1.0               | 2020/12/4      | ``ansible-galaxy collection install fortinet.fortios:1.1.0``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.2.0         | 1.1.3               | 2020/12/7      | ``ansible-galaxy collection install fortinet.fortios:1.1.3``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.2.0         | 1.1.6               | 2020/12/21     | ``ansible-galaxy collection install fortinet.fortios:1.1.6``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.4.0         | 1.0.11              | 2020/5/11      | ``ansible-galaxy collection install fortinet.fortios:1.0.11``   |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.4.0         | 1.1.1               | 2020/12/4      | ``ansible-galaxy collection install fortinet.fortios:1.1.1``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.4.0         | 1.1.4               | 2020/12/7      | ``ansible-galaxy collection install fortinet.fortios:1.1.4``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+
| 6.4.0         | 1.1.7               | 2020/12/21     | ``ansible-galaxy collection install fortinet.fortios:1.1.7``    |
+---------------+---------------------+----------------+-----------------------------------------------------------------+

**Note**: Use ``-f`` option (i.e.
``ansible-galaxy collection install -f fortinet.fortios:x.x.x``) to
renew your existing local installation.
