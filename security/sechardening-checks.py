# TODO:
# Completeness check - What is the correct path?
# Should we check if the parameter exists before checking the value?
# startswith

import grp
import pwd
import os
import configparser

['DEFAULT']

def check_neutron_hardening():
    '''
    Section:Parameter:Expected-Value
    keystone_authtoken:auth_protocol:https
    keystone_authtoken:identity_uri:https://....
    :use_ssl:True
    :auth_strategy:keystone
    '''
    config = configparser.ConfigParser()
    config.read('/var/lib/config-data/puppet-generated/neutron/etc/neutron/neutron.conf')
    if (config['keystone_authtoken']['auth_protocol'] != 'https' and
        not config['keystone_authtoken']['identity_uri'].startswith('https')):
        print('Authentication token is not secured')
        return False
    if (not config['DEFAULT']['use_ssl']):
        print('SSL is not used')
        return False
    if(not config['DEFAULT']['auth_strategy'] != 'keystone')
        print('Authentication strategy should be keystone')
        return False


def check_cinder_hardening():
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
    config.read('/var/lib/config-data/puppet-generated/cinder/etc/cinder/cinder.conf')
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
    if(!config['DEFAULT']['auth_strategy'] != 'keystone')
        print('Authentication strategy should be keystone')
        return False
    if (config['DEFAULT']['glance_api_insecure']):
        print('Cinder-Glance API is insecure')
        return False
    if (config['DEFAULT']['osapi_max_request_body_size'] != 114688 or
        config['oslo_middleware']['max_request_body_size'] != 114688)
        print('MAX Request Body Size is not 114688')
        return False

def check_horizon_hardening():


def check_nova_hardening():
    config = configparser.ConfigParser()
    config.read('/var/lib/config-data/puppet-generated/nova/etc/nova/nova.conf')
    if(not config['DEFAULT']['auth_strategy'] != 'keystone')
        print('Authentication strategy should be keystone')
        return False
    if (config['keystone_authtoken']['auth_protocol'] != 'https' and
        not config['keystone_authtoken']['identity_uri'].startswith('https')):
        print('Authentication token is not secured')
    if (config['DEFAULT']['glance_api_insecure']):
        print('Glance-Nova API is insecure')
        return False


def check_keystone_hardening():
    '''
    https://static.open-scap.org/ssg-guides/ssg-rhosp13-guide-stig.html
    /etc/keystone/keystone.conf
    Section:Parameter:Expected-Value
    token:hash_algorithm:SHA256
    ssl:enable:True
    NA:max_request_body_size:default/114688/some-value
    security_compliance:disable_user_account_days_inactive:some-value
    security_compliance:lockout_failure_attempts:some-value
    security_compliance:lockout_duration:some-value
    DEFAULT:admin_token:disabled
    *** If lockout_failure_attempts is enabled and lockout_duration is left undefined,
    users will be locked out indefinitely until the user is explicitly re-enabled ***
    [/etc/keystone/keystone-paste.ini]
    filter:admin_token_auth:AdminTokenAuthMiddleware:not-exist
    '''
    config = configparser.ConfigParser()
    config.read('/var/lib/config-data/puppet-generated/keystone/etc/keystone/keystone.conf')
    if config['token']['hash_algorithm'] != 'SHA256':
        print('Hash Algorithm is NOT SHA256')
        return False
    if not config['ssl']['enable']:
        print('SSL is not enabled')
        return False
    if not config['DEFAULT']['max_request_body_size']:
        print('MAX request Body Size is not specified')
        return False
    if (not config['security_compliance']['disable_user_account_days_inactive'] and
        not config['security_compliance']['lockout_failure_attempts'] and
        not config['security_compliance']['lockout_duration']):
        print("Security Compliance configurations are not correct")
        return False
    if config['DEFAULT']['admin_token'] != 'disabled':
        print("Admin Token is not disabled")
        return False



def check_sixfourzero_filepermission():
    # https://stackoverflow.com/questions/1861836/checking-file-permissions-in-linux-with-python
    filenames = ['/var/lib/config-data/puppet-generated/cinder/etc/cinder/cinder.conf',
                 '/var/lib/config-data/puppet-generated/cinder/etc/cinder/api-paste.ini',
                 '/var/lib/config-data/puppet-generated/cinder/etc/cinder/policy.json',
                 '/var/lib/config-data/puppet-generated/cinder/etc/cinder/rootwrap.conf',
                 '/var/lib/config-data/puppet-generated/neutron/etc/neutron/neutron.conf',
                 '/var/lib/config-data/puppet-generated/neutron/etc/neutron/api-paste.ini',
                 '/var/lib/config-data/puppet-generated/neutron/etc/neutron/policy.json',
                 '/var/lib/config-data/puppet-generated/neutron/etc/neutron/rootwrap.conf',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/keystone.conf',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/keystone-paste.ini',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/policy.json',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/logging.conf',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/ssl/certs/signing_cert.pem',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/ssl/private/signing_key.pem',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/ssl/certs/ca.pem',
                 '/var/lib/config-data/puppet-generated/nova/etc/nova/nova.conf',
                 '/var/lib/config-data/puppet-generated/nova/etc/nova/api-paste.ini',
                 '/var/lib/config-data/puppet-generated/nova/etc/nova/policy.json',
                 '/var/lib/config-data/puppet-generated/nova/etc/nova/rootwrap.conf']
    for file in filenames:
        stat_info = os.stat(file)
        if (bool(stat_info.st_mode & stat.IXUSR) or
            bool(stat_info.st_mode & stat.IWGRP) or
            bool(stat_info.st_mode & stat.IXGRP) or
            bool(stat_info.st_mode & stat.IROTH) or
            bool(stat_info.st_mode & stat.IWOTH) or
            bool(stat_info.st_mode & stat.IXOTH)):
            print('The File {} has wrong permission - FIX IT'.format(file))
            return False
    return True

def check_ug_keystone():
    filenames = ['/var/lib/config-data/puppet-generated/keystone/etc/keystone/keystone.conf',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/keystone-paste.ini',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/policy.json',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/logging.conf',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/ssl/certs/signing_cert.pem',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/ssl/private/signing_key.pem',
                 '/var/lib/config-data/puppet-generated/keystone/etc/keystone/ssl/certs/ca.pem']
    for file in filenames:
        stat_info = os.stat(file)
        if (pwd.getpwuid(stat_info.st_uid)[0] != 'keystone'):
            print('The user of File {} is not root'.format(file))
            return False
        if (pwd.getgrpid(stat_info.st_gid)[0] != 'keystone'):
            print('The group ownership of file {} is not keystone'.format(file))
            return False
    return True


def check_ug_root_nova():

    filenames = ['/var/lib/config-data/puppet-generated/nova/etc/nova/nova.conf',
                 '/var/lib/config-data/puppet-generated/nova/etc/nova/api-paste.ini',
                 '/var/lib/config-data/puppet-generated/nova/etc/nova/policy.json',
                 '/var/lib/config-data/puppet-generated/nova/etc/nova/rootwrap.conf']
        for file in filenames:
        stat_info = os.stat(file)
        if (pwd.getpwuid(stat_info.st_uid)[0] != 'root'):
            print('The user of File {} is not root'.format(file))
            return False
        if (pwd.getgrpid(stat_info.st_gid)[0] != 'nova'):
            print('The group ownership of file {} is not nova'.format(file))
            return False
    return True

def check_ug_root_neutron():
    # https://stackoverflow.com/questions/927866/how-to-get-the-owner-and-group-of-a-folder-with-python-on-a-linux-machine
    filenames = ['/var/lib/config-data/puppet-generated/neutron/etc/neutron/neutron.con',
                 '/var/lib/config-data/puppet-generated/neutron/etc/neutron/api-paste.ini',
                 '/var/lib/config-data/puppet-generated/neutron/etc/neutron/policy.json',
                 '/var/lib/config-data/puppet-generated/neutron/etc/neutron/rootwrap.conf']
    for file in filenames:
        stat_info = os.stat(file)
        if (pwd.getpwuid(stat_info.st_uid)[0] != 'root'):
            print('The user of File {} is not root'.format(file))
            return False
        if (pwd.getgrpid(stat_info.st_gid)[0] != 'neutron'):
            print('The group ownership of file {} is not neutron'.format(file))
            return False
    return True

def check_ug_root_cinder():
    # https://stackoverflow.com/questions/927866/how-to-get-the-owner-and-group-of-a-folder-with-python-on-a-linux-machine
    filenames = ['/var/lib/config-data/puppet-generated/cinder/etc/cinder/cinder.conf',
                 '/var/lib/config-data/puppet-generated/cinder/etc/cinder/api-paste.ini',
                 '/var/lib/config-data/puppet-generated/cinder/etc/cinder/policy.json',
                 '/var/lib/config-data/puppet-generated/cinder/etc/cinder/rootwrap.conf']
    for file in filenames:
        stat_info = os.stat(file)
        if (pwd.getpwuid(stat_info.st_uid)[0] != 'root'):
            print('The user of File {} is not root'.format(file))
            return False
        if (pwd.getgrpid(stat_info.st_gid)[0] != 'cinder'):
            print('The group ownership of file {} is not cinder'.format(file))
            return False
    return True

def main():
    if check_ug_root_cinder():
        print('UG-ROOT-CINDER PASSED')
    else:
        print('UG-ROOT-CINDER FAILED')

    if check_ug_root_cinder():
        print('UG-ROOT-NEUTRON PASSED')
    else:
        print('UG-ROOT-NEUTRON FAILED')
    if check_sixfourzero_filepermission():
        print('ALL FILE PERMISSIONS ARE STRICT')
    else:
        print('SOME FILE PERMISSIONS ARE NOT STRICT')


if __name__ == '__main__':
    main()
