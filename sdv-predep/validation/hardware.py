class HardwareValidation():
    """ perform hardware validation """
    def __init__(self, role, json, value, manifest):
        self.role = role
        self.json = json
        self.value = value

        self.right = 0
        self.wrong = 0
        self.total = 0

        self.manifest = manifest

        self.validate_hardware()
    
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

    def validate_bios_profile(self, value):
        """ validate bios profile """
        val = ""
        profile = 'bios_profile'
        keys = ['bios_version', 'bios_mode', 'bootstrap_proto', 'hyperthreading_enabled', 'bios_setting']

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key
                break
        
        # print(val)
        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
    
    def validate_processor_profile(self, value):
        """ validate processor profile """
        val = ""
        profile = 'processor_profiles'
        keys = ['speed', 'model', 'architecture']

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break
        
        # print(val)
        val = val["profile_info"]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

    def validate_disks_profile(self, value):
        """ validate disks profile """
        val = ""
        profile = 'disks_profiles'
        keys = ['address', 'dev_type', 'rotation', 'bus']

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break
        
        # print(val)
        val = val["profile_info"]

        for vals in val:
            for key in keys:
                temp1 = vals[key]
                temp2 = self.manifest.find_val(self.role, profile, key)
                self.comparison(key, profile, temp1, temp2)

    def validate_nic_profile(self, value):
        """ validate nic profile """
        val = ""
        profile = 'nic_profiles'
        keys = ['address', 'dev_type', 'bus', 'sriov_capable', 'numa_id']

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break
        
        val = val["profile_info"]

        for vals in val:
            for key in keys:
                temp1 = vals[key]
                temp2 = self.manifest.find_val(self.role, profile, key)
                self.comparison(key, profile, temp1, temp2)

    def validate_hardware(self):
        """ validate hardware """
        # find hardware profile with given key
        val = ""
        profile = 'hardware_profiles'
        keys = ['manufacturer', 'model', 'generation', 'memory']

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break
        
        # print(val)
        val = val["profile_info"]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

        # print(val["bios_profile"])
        self.validate_bios_profile(val["bios_profile"])
        self.validate_processor_profile(val["processor_profile"])
        self.validate_disks_profile(val["disks_profile"])
        self.validate_nic_profile(val["nics_profile"])
    
