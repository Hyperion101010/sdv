import time

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

import grp
import pwd
import os
import configparser

class client_runner:
    def __init__(self, pod_name):
        self.pod_name = pod_name
        config.load_kube_config('kubepod15')
        c = Configuration()
        c.assert_hostname = False
        Configuration.set_default(c)
        self.api_instance = core_v1_api.CoreV1Api()
        print('initiated')

    def interact(self):
        exec_command = ['/bin/sh']
        self.kbclient = stream(self.api_instance.connect_get_namespaced_pod_exec,
                  self.pod_name,
                  'openstack',
                  command=exec_command,
                  stderr=True, stdin=True,
                  stdout=True, tty=False,
                  _preload_content=False)
        print('interacted', self.kbclient.is_open())

    def execute_com(self, command_name, file_name):
        if not self.kbclient.is_open():
            print('re-open the stream', self.kbclient.is_open())
            self.interact()

        if 'cat' in command_name:
            self.kbclient.write_stdin(command_name+' ' + file_name + '\n')
            self.op = self.kbclient.read_stdout(timeout=3)
            if self.op is '':
                self.op = self.kbclient.read_stdout(timeout=3)
        elif 'stat' in command_name:
            self.kbclient.write_stdin(command_name+ ' ' + file_name + '\n')
            self.op = self.kbclient.read_stdout(timeout=3)
        elif 'ownership' in command_name:
            command_name = 'stat --format "%G"'
            self.kbclient.write_stdin(command_name+ ' ' + file_name + '\n')
            self.op = self.kbclient.read_stdout(timeout=3)
        elif 'group-ownership' in command_name:
            command_name = 'stat --format "%U"'
            self.kbclient.write_stdin(command_name+ ' ' + file_name + '\n')
            self.op = self.kbclient.read_stdout(timeout=3)
        elif 'ls' in command_name:
            self.kbclient.write_stdin(command_name+ ' ' + file_name + '\n')
            self.op = self.kbclient.read_stdout(timeout=3)
            if self.op is '':
                self.op = self.kbclient.read_stdout(timeout=3)
        else:
            print('unrecognised command\n')

    def get_op(self):
        return self.op

    def close(self):
        self.kbclient.close()

def cinder_checks(clrn):
    '''
    Section:Parameter:Expected-Value
    keystone_authtoken:auth_protocol:https
    keystone_authtoken:identity_uri:https://....
    :nova_api_insecure:False
    :glance_api_insecure:False
    :nas_secure_file_permissions:auto
    :nas_secure_file_operations:auto
    :auth_strategy:keystone
    :osapi_max_request_body_size:114688 OR
    oslo_middleware:max_request_body_size:114688
    '''
    config = configparser.ConfigParser()
    clrn.execute_com('cat', '/etc/cinder/cinder.conf')
    config.read_string(clrn.get_op())
    if (config['keystone_authtoken']['auth_protocol'] != 'https' and
        not config['keystone_authtoken']['identity_uri'].startswith('https')):
        print('Authentication token is not secured')
        return False
    if (config['DEFAULT']['nova_api_insecure']):
        print('Cinder-Nova API is insecure')
        return False
    if(config['DEFAULT']['nas_secure_file_operations'] != 'auto'):
        print('NAS Secure File is False')
        return False
    if(config['DEFAULT']['nas_secure_file_permissions'] != 'auto'):
        print('NAS secure file permissions')
        return False
    if(config['DEFAULT']['auth_strategy'] != 'keystone'):
        print('Authentication strategy should be keystone')
        return False
    if (config['DEFAULT']['glance_api_insecure']):
        print('Cinder-Glance API is insecure')
        return False
    if (config['DEFAULT']['osapi_max_request_body_size'] != 114688 or
        config['oslo_middleware']['max_request_body_size'] != 114688):
        print('MAX Request Body Size is not 114688')
        return False
    filenames = ['/etc/cinder/cinder.conf',
                 '/etc/cinder/api-paste.ini',
                 '/etc/cinder/policy.json',
                 '/etc/cinder/rootwrap.conf']
    for fl_name in filenames:
        clrn.execute_com('ownership', fl_name)
        user_name = clrn.get_op()
        clrn.execute_com('group-ownership', fl_name)
        group_name = clrn.get_op()
        if user_name != 'root' and group_name != 'cinder':
            return False
        else:
            pass

def main():
    clrn = client_runner('cinder-api-b9c88f9b9-4x4px')
    clrn.interact()
    cinder_checks(clrn)

if __name__== '__main__':
    main()