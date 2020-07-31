#!/usr/bin/env python

# pylint: disable=line-too-long, invalid-name, missing-module-docstring

import os
import json
from time import time
from manifest import Manifest
from hardware import HardwareValidation
from info import InfoValidation
from platform import PlatformValidation
from software import SoftwareValidation
from storage import StorageValidation

CWD = os.getcwd()

class Validate():
    def __init__(self, yaml_dir, mapping_file_dir, json_fn):
        self.correct = 0
        self.wrong = 0
        self.total = 0
        self.json = dict()

        self.read_json(json_fn)
        self.manifest = Manifest(yaml_dir=yaml_dir, mapping_file_dir=mapping_file_dir)
        self.validate(self.json)
    
    def read_json(self, json_fn):
        """ read json file """
        try:
            with open(os.path.join(CWD, json_fn)) as json_file:
                self.json = json.loads(json_file.read())
        except IOError:
            print('Could not read json file')
    
    def validate(self, json):
        """ description about validation """
        # iterate through the roles: have a class for each for each of the roles
        for index, value in enumerate(json["roles"]):
            role = value["name"]
            # print(role,value["hardware_profile"])
            self.correct, self.wrong, self.total =  HardwareValidation(role, json, value["hardware_profile"], self.manifest).get_values()
            print("The number of correct :{} wrong:{} and total:{}".format(self.correct,self.wrong, self.total))
            print()
            print()
            self.correct, self.wrong, self.total =  StorageValidation(role, json, value["storage_mapping"], self.manifest).get_values()
            print("The number of correct :{} wrong:{} and total:{}".format(self.correct,self.wrong, self.total))
            print()
            print()
            self.correct, self.wrong, self.total =  PlatformValidation(role, json, value["platform_profile"], self.manifest).get_values()
            print("The number of correct :{} wrong:{} and total:{}".format(self.correct,self.wrong, self.total))
            print()
            print()
        
        # print the final report
        print()
        print()



if __name__ == "__main__":
    Validate('/home/ashwin/github/sdv/sdv-predep/data', '/home/ashwin/github/sdv/sdv-predep/mapping-files/airship', '/home/ashwin/github/sdv/sdv-predep/data/platform_description_16July2020.json')