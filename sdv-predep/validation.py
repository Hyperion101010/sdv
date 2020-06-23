#!/usr/bin/env python

# pylint: disable=line-too-long, invalid-name, missing-module-docstring

import os
import json
import yaml

CWD = os.getcwd()

class Validate():
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
        """ read json file """
        try:
            with open(os.path.join(CWD, mapping_fn)) as json_file:
                self.mapping = json.loads(json_file.read())
        except IOError:
            print('Could not read mapping file')

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
        string = ""
        present = self.find_json_vals(key, self.json)

        if present:
            # Check mapping file
            if key in self.mapping.keys():
                key = self.mapping[key]

            match = self.find_match(key, self.yaml)

            if match:
                string += 'The pdf key vals are:{} and installer key vals are:{}\n'.format(self.json_vals, self.yaml_vals)
                string += "key-value pairs of pdf and installer match!\n"
            else:
                string += 'The pdf key vals are:{} and installer key vals are:{}\n'.format(self.json_vals, self.yaml_vals)
                string += "key-value pairs of pdf and installer do not match\n"
        else:
            string += 'key not present in pdf'
        
        return string
