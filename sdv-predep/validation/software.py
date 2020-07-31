class SoftwareValidation():
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
    
    def validate_software(self, value):
        """ validate platform profile """
        val = ""
        profile = 'software_set'
        keys = []

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        self.validate_undercloud(value)
        self.validate_infrastructure(value)
        self.validate_openstack(value)
    
    def validate_undercloud(self,value):
        val = ""
        profile = 'undercloud_sw_profiles'
        keys = ["name", "version"]

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        for val in val["sw_list"]:
            for _, key in enumerate(keys):
                temp1 = val[key]
                temp2 = self.manifest.find_val(self.role, profile, key)
                self.comparison(key, profile, temp1, temp2)
    
    def validate_infrastructure(self,value):
        val = ""
        profile = 'infrastructure_sw_profiles'
        keys = ["name", "version"]

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        for val in val["sw_list"]:
            for _, key in enumerate(keys):
                temp1 = val[key]
                temp2 = self.manifest.find_val(self.role, profile, key)
                self.comparison(key, profile, temp1, temp2)
    
    def validate_openstack(self,value):
        val = ""
        profile = 'openstack_sw_profiles'
        keys = ["name", "version"]

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
        
        for val in val["sw_list"]:
            for _, key in enumerate(keys):
                temp1 = val[key]
                temp2 = self.manifest.find_val(self.role, profile, key)
                self.comparison(key, profile, temp1, temp2)

