class PlatformValidation():
    """ perform hardware validation """
    def __init__(self, role, json):
        self.role = role
        self.json = json
    
    def comparison(self, key, profile, pdf_val, man_val):
        if pdf_val == "":
            print("No value exists for pdf-key:{} of profile:{} and role:{}".format(key, profile, self.role))
        elif man_val == "" or man_val == None:
            print("No value exists for manifest-key:{} of profile:{} and role:{}".format(key, profile, self.role))
        elif pdf_val != man_val:
            print("The pdf and manifest values do not match for key:{} profile:{} role;{}".format(key, profile, self.role))
        else:
            print("The pdf and manifest values do not match for key:{} profile:{} role;{}".format(key, profile, self.role))
    
    def validate_platform(self, value):
        """ validate platform profile """
        val = ""
        profile = 'platform_profiles'
        keys = ['os', 'rt_kvm', 'kernel_version', 'kernel_parameters', 'isolated_cpus', 
                'vnf_cores', 'os_reserved_cores', 'hugepage_count', 'hugepage_size', 
                'iommu', 'vswitch_daemon_cores', 'vswitch_type', 'vswitch_uio_driver', 
                'vswitch_mem_channels', 'vswitch_socket_memory', 'vswitch_pmd_cores', 
                'vswitch_dpdk_lcores', 'vswitch_dpdk_rxqs', 'vswitch_options']

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        for key in keys:
            temp1 = val[key]
            temp2 = find_val_manifest(self.role, profile , key)
            self.comparison(key, profile, temp1, temp2)