# TODO:
# Completeness check - What is the correct path?
# Should we check if the parameter exists before checking the value?
# startswith

import grp
import pwd
import os
import configparser

from stat import S_IROTH,S_IWGRP,S_IWOTH,S_IXGRP,S_IXUSR, S_IXOTH

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
    if(not config['DEFAULT']['auth_strategy'] != 'keystone'):
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

def check_horizon_hardening():
    config = configparser.ConfigParser()
    config.read('/var/lib/config-data/puppet-generated/horizon/openstack-dashboard/local_settings.py')
    file_name = 'local_settings.py'
    stat_info = os.stat('/var/lib/config-data/puppet-generated/horizon/openstack-dashboard/local_settings.py')
    if (pwd.getpwuid(stat_info.st_uid)[0] != 'root'):
        print('The user of File {} is not root'.format(file_name))
        return False
    if (grp.getgrgid(stat_info.st_gid)[0] != 'horizon'):
        print('The group ownership of file {} is not horizon'.format(file_name))
        return False
    try:
        fl = open('/var/lib/config-data/puppet-generated/horizon/openstack-dashboard/local_settings.py', 'r')
        config.read_string(fl.read())
        if (not config['DISALLOW_IFRAME_EMBED']):
            print("Dashboard can be embedded within a iframe")
            return False
        if (not config['CSRF_COOKIE_SECURE']):
            print("CSRF exploit can be executed in the dashboard")
            return False
        if (not config['SESSION_COOKIE_SECURE']):
            print("Cookie sessions can be used to exploit the dashboard")
            return False
        if (not config['SESSION_COOKIE_HTTPONLY']):
            print("DOM exploits can be executed in the dashboard")
            return False
        if (config['PASSWORD_AUTOCOMPLETE']):
            print("Password autocomplete is harmful for the dashboard")
            return False
        if (not config['DISABLE_PASSWORD_REVEAL']):
            print("Password fields can be revealed in the dashboard")
            return False
        if (not config['ENFORCE_PASSWORD_CHECK']):
            print("Password can be changed without admin permission")
            return False
        if (not config['PASSWORD_VALIDATOR']):
            print("Password complexity can't be validated")
            return False
        if (not config['SECURE_PROXY_SSL_HEADER'] != 'HTTP_X_FORWARDED_PROTO' or not config['SECURE_PROXY_SSL_HEADER'] != 'https'):
            print("Consider deploying dashboard behind a proxy")
            return False
        fl.close()
    except:
        return False
    return True

def check_nova_hardening():
    config = configparser.ConfigParser()
    config.read('/var/lib/config-data/puppet-generated/nova/etc/nova/nova.conf')
    filenames = [
        '/var/lib/config-data/puppet-generated/nova/etc/nova/nova.conf',
        '/var/lib/config-data/puppet-generated/nova/etc/nova/api-paste.ini',
        '/var/lib/config-data/puppet-generated/nova/etc/nova/policy.json',
        '/var/lib/config-data/puppet-generated/nova/etc/nova/rootwrap.conf',
        '/var/lib/config-data/puppet-generated/nova/etc/nova']
    for file in filenames:    
        stat_info = os.stat(file)
        if (pwd.getpwuid(stat_info.st_uid)[0] != 'root'):
            print('The user of File {} is not root'.format(file))
            return False
        if (grp.getgrgid(stat_info.st_gid)[0] != 'nova'):
            print('The group ownership of file {} is not nova'.format(file))
            return False
    if(not config['DEFAULT']['auth_strategy'] != 'keystone'):
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
    if (config['DEFAULT']['insecure_debug']):
        print("Sending responses in http is not disabled during debug")
        return False
    if (not config['token']['provider'] != 'fernet' and config['token']['provider'] == 'uuid'):
        print("Insecure token provider configured, use fernet")
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
                 '/var/lib/config-data/puppet-generated/nova/etc/nova/rootwrap.conf',
                 '/var/lib/config-data/puppet-generated/horizon/etc/openstack-dashboard/local_settings.py']
    for file in filenames:
        stat_info = os.stat(file)
        if (bool(stat_info.st_mode & S_IXUSR(stat_info.st_mode)) or
            bool(stat_info.st_mode & S_IWGRP(stat_info.st_mode)) or
            bool(stat_info.st_mode & S_IXGRP(stat_info.st_mode)) or
            bool(stat_info.st_mode & S_IROTH(stat_info.st_mode)) or
            bool(stat_info.st_mode & S_IWOTH(stat_info.st_mode)) or
            bool(stat_info.st_mode & S_IXOTH(stat_info.st_mode))):
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
        if (grp.getgrgid(stat_info.st_gid)[0] != 'keystone'):
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
        if (grp.getgrgid(stat_info.st_gid)[0] != 'nova'):
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
        if (grp.getgrgid(stat_info.st_gid)[0] != 'neutron'):
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
        if (grp.getgrgid(stat_info.st_gid)[0] != 'cinder'):
            print('The group ownership of file {} is not cinder'.format(file))
            return False
    return True

def main():
    if check_ug_root_cinder():
        print('UG-ROOT-CINDER PASSED')
    else:
        print('UG-ROOT-CINDER FAILED')

    if check_ug_root_neutron():
        print('UG-ROOT-NEUTRON PASSED')
    else:
        print('UG-ROOT-NEUTRON FAILED')

    if check_ug_root_nova():
        print('UG-ROOT-NOVA PASSED')
    else:
        print('UG-ROOT-NOVA FAILED')

    if check_sixfourzero_filepermission():
        print('ALL FILE PERMISSIONS ARE STRICT')
    else:
        print('SOME FILE PERMISSIONS ARE NOT STRICT')

    if check_horizon_hardening():
        print('UG-ROOT-HORIZON PASSED')
    else:
        print('UG-ROOT-HORIZON FAILED')
    if check_keystone_hardening():
        print('Keystone checklist PASSED')
    else:
        print('Keystone checklist FAILED')
    if check_cinder_hardening():
        print('Cinder checklist PASSED')
    else:
        print('Cinder checklist FAILED')
    if check_neutron_hardening:
        print('Neutron checklist PASSED')
    else:
        print('Neutron checklist FAILED')
    if check_nova_hardening():
        print('Nova checklist PASSED')
    else:
        print('Nova checklist FAILED')


if __name__ == '__main__':
    main()