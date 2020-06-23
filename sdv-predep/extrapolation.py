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

    def get_ipmi_info(self, ipmi, count, inc):
        """get hardware profile """
        # perform operations. As of now none exists
        temp = dict()
        print('.'.join(ipmi.split('.')[:3]),)
        temp["ip"] = str('.'.join(ipmi.split('.')[:3])) + '.' + str(int(ipmi.split('.')[-1]) + count*int(inc))
        temp["user"] = self.pd["extrapolation_info"]["ilo_user"]
        temp["password"] = self.pd["management_info"]["city"]+self.pd["management_info"]["area_name"]\
            +self.pd["management_info"]["room_id"]+str(count)

        return temp

    def extrapolate(self):
        """ Perform Extrapolation """
        list_servers = []

        # get ipmi info
        count = 1
        ipmi = ""
        for val in self.pd["networks"]:
            if val["name"] == 'ipmi':
                ipmi = val["vip"].split('/')[0] # currently we will only take /24

        for val in self.pd["roles"]:
            n = int(val["count"]) # Number of servers in the particular role.


            for _ in range(n):
                temp = dict()
                temp["rack"] = self.get_rack_name()
                temp["device_name"] = self.get_device_name(val["name"])
                temp["az_name"] = self.get_az_name()
                temp["ha_name"] = self.get_ha_name()

                temp["ipmi_info"] = self.get_ipmi_info(ipmi, count, self.pd["extrapolation_info"]["ip_increment"])
                count += 1

                list_servers.append(temp)

        # save the pd file
        self.pd["servers"] = list_servers
        self.save_pd()

