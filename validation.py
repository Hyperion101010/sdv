#!/usr/bin/env python

# pylint: disable=line-too-long, invalid-name, missing-module-docstring

import os
import json
import yaml

CWD = os.getcwd()

class FindKey():
    """Find Key Class"""
    def __init__(self, json_fn, yaml_fn, mapping_fn):
        self.yaml = dict()
        self.json = dict()
        self.mapping = dict()

        self.read_yaml(yaml_fn)
        self.read_json(json_fn)
        self.read_mapping(mapping_fn)

        self.json_vals = []
        self.yaml_vals = []

    def read_yaml(self, yaml_fn):
        """ read yaml file """
        try:
            with open(os.path.join(CWD, yaml_fn)) as yaml_file:
                self.yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
        except IOError:
            print('Could not read yaml file')

    def read_json(self, json_fn):
        """ read json file """
        try:
            with open(os.path.join(CWD, json_fn)) as json_file:
                self.json = json.loads(json_file.read())
        except IOError:
            print('Could not read json file')

    def read_mapping(self, mapping_fn):
        """ read yaml file """
        try:
            with open(os.path.join(CWD, mapping_fn)) as mapping_file:
                temp = mapping_file.read()
        except IOError:
            print('Could not read mapping file')

        # insert file contents into dict
        temp = temp.split('\n')

        for val in temp:
            val = val.split(':')
            self.mapping[val[0].strip()] = val[1].strip()

    def find_json_vals(self, key, temp_json):
        """ insert all matching json key-vals in array """
        for k, v in temp_json.items():
            if k == key:
                self.json_vals.append(v)
                return True

            if isinstance(v, dict):
                found = self.find_json_vals(key, v)
                if found:
                    return True

            if isinstance(v, list):
                for _, val in enumerate(v):
                    found = self.find_json_vals(key, val)
                    if found:
                        return True
        return False

    def find_match(self, key, yaml_temp):
        """ find if yaml key-val matches with json """
        for k, v in yaml_temp.items():
            if k == key:
                self.yaml_vals.append(v)
                if v in self.json_vals:
                    return True

            elif isinstance(v, dict):
                found = self.find_match(key, v)
                if found:
                    return True

            elif isinstance(v, list):
                for _, val in enumerate(v):
                    found = self.find_match(key, val)
                    if found:
                        return True
        return False

    def check_match(self, key):
        """ check if keys of json and yaml match """
        self.json_vals = []
        self.yaml_vals = []
        present = self.find_json_vals(key, self.json)

        if present:
            # Check mapping file
            if key in self.mapping.keys():
                key = self.mapping[key]

            match = self.find_match(key, self.yaml)

            if match:
                print('The json vals are:{} and yaml vals are:{}'.format(self.json_vals, self.yaml_vals))
                print("key-value pairs of json and yaml match!")
            else:
                print('The json vals are:{} and yaml vals are:{}'.format(self.json_vals, self.yaml_vals))
                print("key-value pairs of json and yaml do not match")
        else:
            print('key not present in json')


if __name__ == "__main__":
    obj = FindKey('platform_description_18March2020.json', 'intel-pod10.yaml', 'mapping.txt')
    obj.check_match('qemu')