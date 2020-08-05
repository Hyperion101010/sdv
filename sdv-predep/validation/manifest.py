#!/usr/bin/env python

# pylint: disable=line-too-long, invalid-name, missing-module-docstring, broad-except

""" manifest code """

import os
import json
import yaml

CWD = os.getcwd()

class Manifest():
    """ All about manifest """
    def __init__(self, yaml_dir, mapping_file_dir, logger):
        self.yaml = dict()
        self.mapping = dict()
        self.vals = []
        self.saver = dict()
        self.logger = logger

        self.read_yaml(yaml_dir)
        self.read_mapping(mapping_file_dir)

    def read_yaml(self, yaml_dir):
        """ read yaml file """
        yaml_files = [pos_json for pos_json in os.listdir(yaml_dir) if pos_json.endswith('.yaml')]
        temp = ""

        for file in yaml_files:
            try:
                with open(os.path.join(yaml_dir, file)) as yaml_file:
                    temp = yaml.load(yaml_file, Loader=yaml.FullLoader)
            except Exception as e:
                self.logger.exception("could not read the manifest files:%s", str(e))

            self.yaml[temp["metadata"]["name"]] = temp

    def read_mapping(self, mapping_file_dir):
        """ read corresponding mapping file """
        json_files = [pos_json for pos_json in os.listdir(mapping_file_dir) if pos_json.endswith('.json')]

        for file in json_files:
            try:
                with open(os.path.join(mapping_file_dir, file)) as yaml_file:
                    temp = json.load(yaml_file)
            except Exception as e:
                self.logger.exception("could not read the json file:%s", str(e))

            self.mapping.update(temp)

    def find_vals(self, key, temp_json):
        """ insert all matching json key-vals in array """
        for k, v in temp_json.items():
            if k == key:
                if isinstance(v, list):
                    for val in v:
                        self.vals.append(val)
                else:
                    self.vals.append(v)

            if isinstance(v, dict):
                found = self.find_vals(key, v)
                if found:
                    return True

            if isinstance(v, list):
                for _, val in enumerate(v):
                    if isinstance(val, str):
                        # print(v, k, val, key)
                        continue
                    found = self.find_vals(key, val)
                    if found:
                        return True
        return False

    def find_val(self, role, context, skey):
        """ find val in manifest """

        # 1. find corresponding manifest context & key
        # code here
        key = role + "-" + context + "-" + skey

        try:
            return self.saver[key]
        except Exception:
            # log that the key does not exist in the saver dict.
            self.logger.info("key: %s doesnt exist in the saved keys, searching manifest")

        man_con = self.mapping[key]["manifest_context"]
        man_key = self.mapping[key]["manifest_key"]

        if man_con == '':
            self.saver[key] = []
            return []

        # 2. find values corresponding to the key( by recursing through shortened dict )
        # code here
        self.vals = []
        temp = self.yaml[man_con]
        # print(man_key,temp)
        self.find_vals(man_key, temp)

        # 3. return the value
        self.saver[key] = self.vals
        return self.vals
