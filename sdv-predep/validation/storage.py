#!/usr/bin/env python

# pylint: disable= line-too-long, invalid-name, broad-except, too-many-statements, too-many-arguments, too-many-branches, too-many-instance-attributes

""" program which validates software profile """

class StorageValidation():
    """ perform hardware validation """
    def __init__(self, role, json, value, manifest, logger):
        self.role = role
        self.json = json
        self.value = value
        self.logger = logger

        self.right = 0
        self.wrong = 0
        self.total = 0
        self.result = ""

        self.manifest = manifest

        self.validate()

    def get_values(self):
        """ return set of right wrong and total """
        return self.right, self.wrong, self.total, self.result

    def comparison(self, key, profile, pdf_val, man_val):
        """ do comparison and print results"""
        self.total += 1

        if pdf_val == "":
            self.result += ("No value exists for pdf-key:{} of profile:{} and role:{}\n".format(key, profile, self.role))
        elif man_val == []:
            self.result += ("No value exists for manifest-key:{} of profile:{} and role:{}\n".format(key, profile, self.role))
        elif pdf_val not in man_val:
            self.result += ("The pdf and manifest values do not match for key:{} profile:{} role:{}\n".format(key, profile, self.role))
            self.result += ("the pdf val:{} and manifest val:{}\n".format(pdf_val, man_val))
            self.wrong += 1
        else:
            self.result += ("The pdf and manifest values do match for key:{} profile:{} role:{}\n".format(key, profile, self.role))
            self.right += 1

    def validate(self):
        """ validate storage profile """
        val = ""
        profile = 'storage_profile'
        keys = ['bootdrive']

        self.logger.info("Starting with the validation of storage profile: %s", self.value)

        for key in self.json[profile]:
            if key["name"] == self.value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find storage profile name: %s", self.value)
        else:
            for key in keys:
                try:
                    temp1 = val[key]
                    temp2 = self.manifest.find_val(self.role, profile, key)
                    self.comparison(key, profile, temp1, temp2)
                except Exception:
                    self.logger.error("Not able to find key: %s in storage profile: %s", key, self.value)

            # redefining keys for bd_partitions
            keys = ["name", "size", "bootable"]
            # print(val)
            for valx in val["bd_partitions"]:
                for _, key in enumerate(keys):
                    try:
                        temp1 = valx[key]
                        temp2 = self.manifest.find_val(self.role, profile + '.bd_partitions', key)
                        self.comparison(key, profile, temp1, temp2)
                    except Exception:
                        self.logger.error("Not able to find key: %s in storage profile-bd_partitions: %s", key, self.value)

            # redefining keys for bd_comparisonpartitions.filesystem
            keys = ["mountpoint", "fstype", "mount_options"]
            # print(val)
            for valx in val["bd_partitions"]:
                for _, key in enumerate(keys):
                    try:
                        temp1 = valx["filesystem"][key]
                        temp2 = self.manifest.find_val(self.role, profile + '.bd_partitions.filesystem', key)
                        self.comparison(key, profile, temp1, temp2)
                    except Exception:
                        self.logger.error("Not able to find key: %s in storage profile-filesystem: %s", key, self.value)

            # redefining keys for data_devices
            keys_1 = ["name", "size"]
            keys_2 = ["mountpoint", "fstype", "mount_options"]

            for val1 in val["data_devices"]:
                for val2 in val1["partitions"]:
                    for _, key in enumerate(keys_1):
                        try:
                            temp1 = val2[key]
                            temp2 = self.manifest.find_val(self.role, profile + '.data_devices', key)
                            self.comparison(key, profile, temp1, temp2)
                        except Exception:
                            self.logger.error("Not able to find key: %s in storage profile-data_devices: %s", key, self.value)
                    for _, key in enumerate(keys_2):
                        try:
                            temp1 = val2["filesystem"][key]
                            temp2 = self.manifest.find_val(self.role, profile + '.data_devices', key)
                            self.comparison(key, profile, temp1, temp2)
                        except Exception:
                            self.logger.error("Not able to find key: %s in storage profile-data_devices: %s", key, self.value)

            # redefining keys for journal_devices
            keys = ["name"]
            for valx in val["journal_devices"]:
                for _, key in enumerate(keys):
                    try:
                        temp1 = valx[key]
                        temp2 = self.manifest.find_val(self.role, profile + '.journal_devices', key)
                        self.comparison(key, profile, temp1, temp2)
                    except Exception:
                        self.logger.error("Not able to find key: %s in storage profile-journal_devices: %s", key, self.value)
        