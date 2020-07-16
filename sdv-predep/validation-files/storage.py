class SoftwareValidation():
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
    
    def validate_storage(self, value):
        """ validate storage profile """
        val = ""
        profile = 'storage_profile'
        keys = ['bootdrive']

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break
    
        for key in keys:
            temp1 = val[key]
            temp2 = find_val_manifest(self.role, profile , key)
            self.comparison(key, profile, temp1, temp2)
        
        # redefining keys for bd_partitions
        keys = ["name", "size", "bootable"]
        for val in val["bd_partitons"]:
            for _, key in enumerate(keys):
                temp1 = val[key]
                temp2 = find_manifest_val(self.role, profile + '.bd_partitions', key)
                self.comparison(key, profile, temp1, temp2)

        # redefining keys for bd_partitions.filesystem
        keys = ["name", "size", "bootable"]
        for val in val["bd_partitons"]:
            for _, key in enumerate(keys):
                temp1 = val["filesystem"][key]
                temp2 = find_manifest_val(self.role, profile + '.bd_partitions.filesystem', key)
                self.comparison(key, profile, temp1, temp2)
        
        # redefining keys for data_devices
        keys = ["name"]
        for val in val["data_devices"]:
            for _, key in enumerate(keys):
                temp1 = val[key]
                temp2 = find_manifest_val(self.role, profile + '.data_devices', key)
                self.comparison(key, profile, temp1, temp2)

        # redefining keys for journal_devices
        keys = ["name"]
        for val in val["journal_devices"]:
            for _, key in enumerate(keys):
                temp1 = val[key]
                temp2 = find_manifest_val(self.role, profile + '.journal_devices', key)
                self.comparison(key, profile, temp1, temp2)
    