import os
import yaml
import json

CWD = os.getcwd()

class Manifest():
    """ All about manifest """
    def __init__(self, yaml_dir, mapping_file_dir):
        self.yaml = dict()
        self.mapping = dict()
        self.vals = []
        self.saver = dict()
        
        self.read_yaml(yaml_dir)
        self.read_mapping(mapping_file_dir)
    
    def read_yaml(self, yaml_dir):
        """ read yaml file """
        yaml_files = [pos_json for pos_json in os.listdir(yaml_dir) if pos_json.endswith('.yaml')]
        temp = ""
        # print(yaml_files)

        for file in yaml_files:
            try:
                with open(os.path.join(yaml_dir, file)) as yaml_file:
                    temp = yaml.load(yaml_file, Loader=yaml.FullLoader)
            except IOError:
                print('Could not read yaml file:{}'.format(yaml))
            
            self.yaml[temp["metadata"]["name"]] = temp

    def read_mapping(self, mapping_file_dir):
        """ read corresponding mapping file """
        json_files = [pos_json for pos_json in os.listdir(mapping_file_dir) if pos_json.endswith('.json')]

        for file in json_files:
            try:
                with open(os.path.join(mapping_file_dir, file)) as yaml_file:
                    temp = json.load(yaml_file)
            except IOError:
                print('Could not read json file')
            
            self.mapping.update(temp)

    def find_vals(self, key, temp_json):
        """ insert all matching json key-vals in array """
        for k, v in temp_json.items():
            if k == key:
                self.vals.append(v)
                return True

            if isinstance(v, dict):
                found = self.find_vals(key, v)
                if found:
                    return True

            if isinstance(v, list):
                for _, val in enumerate(v):
                    if isinstance(val, str):
                        continue
                    found = self.find_vals(key, val)
                    if found:
                        return True
        return False
    
    
    def find_val(self, role, context, key):
        """ find val in manifest """

        # 1. find corresponding manifest context & key
        # code here
        key = role + "-" + context + "-" + key
        
        try:
            return self.saver[key]
        except:
            # log that the key does not exist in the saver dict.
            pass

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
        

    