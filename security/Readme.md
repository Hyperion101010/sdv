# Security Hardening.
There are 3 aspects:
1. Hardening using Ansible: Using Openstack's Ansible-Hardening. https://docs.openstack.org/ansible-hardening/latest/
2. Checking File Permissions: Use the sechardening-checks.py file.
3. Testing: Using the tools 'Syntribos' (https://github.com/openstack-archive/syntribos) 'cypherscan' (https://github.com/mozilla/cipherscan) and 'AIDE' (https://aide.github.io/) to perform the testing.

These 3 many not fully cover the guidelines mentioned in:
https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html-single/security_and_hardening_guide/index
