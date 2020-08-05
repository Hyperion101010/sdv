#!/usr/bin/env python

# pylint: disable= line-too-long, invalid-name, broad-except, too-many-instance-attributes, too-many-arguments, too-many-branches

""" program which validates software profile """

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
        """ return set of right wrong and total """
        return self.right, self.wrong, self.total

    def comparison(self, key, profile, pdf_val, man_val):
        """ do comparison and print results"""
        self.total += 1

        if pdf_val == "":
            print("No value exists for pdf-key:{} of profile:{} and role:{}".format(key, profile, self.role))
        elif man_val == []:
            print("No value exists for manifest-key:{} of profile:{} and role:{}".format(key, profile, self.role))
        elif pdf_val not in man_val:
            print("The pdf and manifest values do not match for key:{} profile:{} role:{}".format(key, profile, self.role))
            print("the pdf val:{} and manifest val:{}".format(pdf_val, man_val))
            self.wrong += 1
        else:
            print("The pdf and manifest values do match for key:{} profile:{} role:{}".format(key, profile, self.role))
            self.right += 1

    def validate(self, value):
        """ validate software profile """
        val = ""
        profile = 'software_set'
        # keys = ["none"]

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key["profile_name"]
                break

        self.validate_undercloud(val["undercloud_profile"])
        self.validate_infrastructure(val["infrasw_profile"])
        self.validate_openstack(val["openstack_profile"])

    def validate_undercloud(self, value):
        """ validate undercloud sw """
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

    def validate_infrastructure(self, value):
        """ validate infra sw """
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

    def validate_openstack(self, value):
        """ validate openstack sw """
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
