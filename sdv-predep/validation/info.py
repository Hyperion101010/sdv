class InfoValidation():
    """ perform hardware validation """
    def __init__(self, role, json, value, manifest):
        self.role = role
        self.json = json

        self.right = 0
        self.wrong = 0
        self.total = 0

        self.manifest = manifest

        self.validate(value)
    
    def get_values(self):
        return self.right, self.wrong, self.total
    
    def comparison(self, key, profile, pdf_val, man_val):

        self.total += 1

        if pdf_val == "":
            print("No value exists for pdf-key:{} of profile:{} and role:{}".format(key, profile, self.role))
        elif man_val == "" or man_val == None:
            print("No value exists for manifest-key:{} of profile:{} and role:{}".format(key, profile, self.role))
        elif pdf_val != man_val:
            print("The pdf and manifest values do not match for key:{} profile:{} role;{}".format(key, profile, self.role))
            self.right += 1
        else:
            print("The pdf and manifest values do not match for key:{} profile:{} role;{}".format(key, profile, self.role))
            self.wrong += 1
    
    def validate(self, value):
        """ validate all infos """

        val = ""
        profile = 'management_info'
        keys = ['owner', 'area_name', 'area_center_name', 'room_id', 'city', 'resource_pool_name']
        
        val = value[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        val = ""
        profile = 'ntp_info'
        keys = ['primary_ip', 'primary_zone', 'secondary_ip', 'secondary_zone']
        
        val = value[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

        val = ""
        profile = 'syslog_info'
        keys = ["server_ip", "transport"]
        
        val = value[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        val = ""
        profile = 'ldap_info'
        keys = ["base_url", "url", "auth_path", "common_name", "subdomain", "domain"]
        
        val = value[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        val = ""
        profile = 'proxy_info'
        keys = ["address", "port", "user", "password"]
        
        val = value[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        val = ""
        profile = 'vim_info'
        keys = ["vim_name", "vim_id", "vendor", "version", "installer", "deployment_style", "container_orchestrator", "storage_type"]
        
        val = value[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        val = ""
        profile = 'demployment_info'
        keys = ["high_availability", "introspection", "deployment_type", "installer_used", "workload_vnf", "workload_cnf", "sdn_controller", "sdn_controller_version", "sdn_controller_nbapps", "vnfm", "vnfm_version", "data_plane_used", "ironic_deploy_interface", "external_stroage_cluster", "bl_str_connect_method", "cpu_allocation_ratio"]
        
        val = value[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        val = ""
        profile = 'jumphost_info'
        keys = ["ip", "name"]
        
        val = value[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        val = ""
        profile = 'rack_info.rack_details'
        keys = ["rack_name","rack_description", "raack_az"]
        
        val = value[profile.split('.')[0]][profile.split('.')[1]]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        val = ""
        profile = 'storage_cluster_info'
        keys = ["name", "cluster_type", "cluster_id", "auth_type", "username", "password", "certificate_location", "client_key", "public_cidr", "cluster_cidr"]
        
        val = value[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        
        