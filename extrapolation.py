#!/usr/bin/env python

# pylint: disable=line-too-long, invalid-name, missing-module-docstring, no-self-use

import os
import json

CWD = os.getcwd()

class Extrapolate():
    """Perform extrapolation"""
    def __init__(self, pd_fn):
        self.pd = dict()

        self.read_pd(pd_fn)

    def read_pd(self, json_fn):
        """ read platform descritpion file """
        try:
            with open(os.path.join(CWD, json_fn)) as json_file:
                self.pd = json.loads(json_file.read())
        except IOError:
            print('Could not read pd file')

    def save_pd(self):
        """ save the pd file """
        try:
            with open('pd_new.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.pd, json_file, indent=2)
        except IOError:
            print('Could not save pd file')

    def get_hardware_profile(self, val):
        """get hardware profile """
        # perform operations. As of now none exists

        return val

    def get_interface_mapping_profile(self, val):
        """get interface mapping profile """
        # perform operations. As of now none exists

        return val

    def get_storage_profile(self, val):
        """get storage profile """
        # perform operations. As of now none exists

        return val

    def get_platform_profile(self, val):
        """get hardware profile """
        # perform operations. As of now none exists

        return val

    def get_rack_name(self):
        """get rack name """
        # perform operations. As of now none exists

        return "rack"

    def get_device_name(self, val):
        """get device name """
        # perform operations. As of now none exists

        return val

    def get_az_name(self):
        """get az name """
        # perform operations. As of now none exists

        return "az_name"

    def get_ha_name(self):
        """get ha name """
        # perform operations. As of now none exists

        return "ha_name"

    def get_ipmi_info(self):
        """get hardware profile """
        # perform operations. As of now none exists
        temp = dict()
        temp["ip"] = "192.xxx.xxx.xxx"
        temp["user"] = self.pd["extrapolation_info"]["ilo_password"]
        temp["password"] = self.pd["extrapolation_info"]["ilo_user"]

        return temp

    def extrapolate(self):
        """ Perform Extrapolation """
        list_servers = []

        for val in self.pd["roles"]:
            n = int(val["count"]) # Number of servers in the particular role.

            for _ in range(n):
                temp = dict()
                temp["rack"] = self.get_rack_name()
                temp["device_name"] = self.get_device_name(val["name"])
                temp["az_name"] = self.get_az_name()
                temp["ha_name"] = self.get_ha_name()
                temp["ipmi_info"] = self.get_ipmi_info()

                list_servers.append(temp)

        # save the pd file
        self.pd["servers"] = list_servers
        self.save_pd()



if __name__ == "__main__":
    obj = Extrapolate('platform_description_12May2020.json')
    obj.extrapolate()
