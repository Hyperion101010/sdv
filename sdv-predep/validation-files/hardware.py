class HardwareValidation():
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

    def validate_bios_profile(self, value):
        """ validate bios profile """
        val = ""
        profile = 'bios_profiles'
        keys = ['bios_version', 'bios_mode', 'bootstrap_proto', 'hyperthreading_enabled', 'bios_setting']

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        for key in keys:
            temp1 = val[key]
            temp2 = find_val_manifest(self.role, profile , key)
            self.comparison(key, profile, temp1, temp2)
    
    def validate_processor_profile(self, value):
        """ validate processor profile """
        val = ""
        profile = 'processor_profiles'
        keys = ['numa_id', 'cpus', 'cpu_cflags', 'speed', 'cache_size', 'model', 'architecture']

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        val = val["profile_info"]

        for key in keys:
            temp1 = val[key]
            temp2 = find_val_manifest(self.role, profile , key)
            self.comparison(key, profile, temp1, temp2)

    def validate_disks_profile(self, value):
        """ validate disks profile """
        val = ""
        profile = 'disks_profiles'
        keys = ['alias', 'address', 'dev_type', 'rotation', 'bus']

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        val = val["profile_info"]

        for key in keys:
            temp1 = val[key]
            temp2 = find_val_manifest(self.role, profile , key)
            self.comparison(key, profile, temp1, temp2)

    def validate_nic_profile(self, value):
        """ validate nic profile """
        val = ""
        profile = 'processor_profiles'
        keys = ['alias', 'address', 'dev_type', 'bus', 'sriov_capable', 'numa_id']

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        val = val["profile_info"]

        for key in keys:
            temp1 = val[key]
            temp2 = find_val_manifest(self.role, profile , key)
            self.comparison(key, profile, temp1, temp2)

    def validate(self, value):
        """ validate hardware """
        # find hardware profile with given key
        val = ""
        profile = 'hardware_profiles'
        keys = ['manufaturer', 'model', 'generation', 'memory']

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        val = val["profile_info"]

        for key in keys:
            temp1 = val[key]
            temp2 = find_val_manifest(self.role, profile , key)
            self.comparison(key, profile, temp1, temp2)

        self.validate_bios_profile(val["bios_profile"])
        self.validate_processor_profile(val["processor_profile"])
        self.validate_disks_profile(val["disks_profile"])
        self.validate_nics_profile(val["nics_profile"])
    
