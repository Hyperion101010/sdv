class StorageValidation():
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
        """ validate storage profile """
        val = ""
        profile = 'storage_profile'
        keys = ['bootdrive']

        for key in self.json[profile]:
            if key["name"] == self.value:
                val = key
                break
    
        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)
        
        # redefining keys for bd_partitions
        keys = ["name", "size", "bootable"]
        # print(val)
        for valx in val["bd_partitions"]:
            for _, key in enumerate(keys):
                temp1 = valx[key]
                temp2 = self.manifest.find_val(self.role, profile + '.bd_partitions', key)
                self.comparison(key, profile, temp1, temp2)

        # redefining keys for bd_comparisonpartitions.filesystem
        keys = ["mountpoint", "fstype", "mount_options"]
        # print(val)
        for valx in val["bd_partitions"]:
            for _, key in enumerate(keys):
                temp1 = valx["filesystem"][key]
                temp2 = self.manifest.find_val(self.role, profile + '.bd_partitions.filesystem', key)
                self.comparison(key, profile, temp1, temp2)
        
        # redefining keys for data_devices
        keys_1 = ["name", "size"]
        keys_2 = ["mountpoint", "fstype", "mount_options"]

        for val1 in val["data_devices"]:
            for val2 in val1["partitions"]:
                for _, key in enumerate(keys_1):
                    temp1 = val2[key]
                    temp2 = self.manifest.find_val(self.role, profile + '.data_devices', key)
                    self.comparison(key, profile, temp1, temp2)
                for _, key in enumerate(keys_2):
                    temp1 = val2["filesystem"][key]
                    temp2 = self.manifest.find_val(self.role, profile + '.data_devices', key)
                    self.comparison(key, profile, temp1, temp2)

        # redefining keys for journal_devices
        keys = ["name"]
        for valx in val["journal_devices"]:
            for _, key in enumerate(keys):
                temp1 = valx[key]
                temp2 = self.manifest.find_val(self.role, profile + '.journal_devices', key)
                self.comparison(key, profile, temp1, temp2)
    