class PlatformValidation():
    """ perform hardware validation """
    def __init__(self, role, json, value, manifest):
        self.role = role
        self.json = json
        self.value = value

        self.right = 0
        self.wrong = 0
        self.total = 0
        
        self.manifest = manifest

        self.validate()
    
    def get_values(self):
        return self.right, self.wrong, self.total
    
    def comparison(self, key, profile, pdf_val, man_val):

        self.total += 1

        if pdf_val == "":
            print("No value exists for pdf-key:{} of profile:{} and role:{}".format(key, profile, self.role))
        elif man_val == "" or man_val == None:
            print("No value exists for manifest-key:{} of profile:{} and role:{}".format(key, profile, self.role))
        elif pdf_val not in man_val:
            print("The pdf and manifest values do not match for key:{} profile:{} role:{}".format(key, profile, self.role))
            print("the pdf val:{} and manifest val:{}".format(pdf_val, man_val))
            self.wrong += 1
        else:
            print("The pdf and manifest values do match for key:{} profile:{} role:{}".format(key, profile, self.role))
            self.right += 1
    
    def validate(self):
        """ validate platform profile """
        val = ""
        profile = 'platform_profiles'
        keys = ['os', 'rt_kvm', 'kernel_version', 'kernel_parameters', 'isolated_cpus', 
                'vnf_cores',
                'iommu', 'vswitch_daemon_cores', 'vswitch_type', 'vswitch_uio_driver', 
                'vswitch_mem_channels', 'vswitch_socket_memory', 'vswitch_pmd_cores', 
                'vswitch_dpdk_lcores', 'vswitch_dpdk_rxqs', 'vswitch_options']

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break
        
        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        key = ["hugepage_count", "hugepage_size"]
        
        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
