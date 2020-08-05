#!/usr/bin/env python

# pylint: disable=line-too-long, invalid-name, missing-module-docstring

""" validation code """

import os
import json
import logging
import argparse
import sys
import datetime
from validation.manifest import Manifest
from validation.hardware import HardwareValidation
from validation.info import InfoValidation
from validation.platform import PlatformValidation
from validation.software import SoftwareValidation
from validation.network import NetworkValidation
from validation.storage import StorageValidation

CWD = os.getcwd()

class Validate():
    """ Validation class """
    def __init__(self, yaml_dir, mapping_file_type, json_fn):
        self.correct = 0
        self.wrong = 0
        self.total = 0
        self.json = dict()
        self.logger = ""
        self.result = ""

        self.start_logger()
        self.read_json(json_fn)
        self.manifest = Manifest(yaml_dir=yaml_dir, mapping_file_dir=os.path.join(CWD, "mapping", mapping_file_type), self.logger)

    def read_json(self, json_fn):
        """ read json file """
        try:
            with open(os.path.join(CWD, json_fn)) as json_file:
                self.json = json.loads(json_file.read())
        except IOError:
            self.logger.critical("Unable to read the pdf file:%s", json_fn)
            self.logger.info("Exiting process")
            sys.exit()

    def start_logger(self):
        """ starting logging process """
        logging.basicConfig(filename='validation.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

        self.logger = logging.getLogger('validation')
        self.logger.info("Starting validation program")

    def validate(self):
        """ description about validation """
        # validate info
        correct, wrong, total, result = InfoValidation('norole', self.json, self.manifest, self.logger).get_values()
        self.correct += correct
        self.wrong += wrong
        self.total += total
        string = ("The number of correct :{} wrong:{} and total:{} in info profile\n\n".format(self.correct, self.wrong, self.total))
        self.result += result + string

        # iterate through the roles: have a class for each for each of the roles
        for _, value in enumerate(self.json["roles"]):
            role = value["name"]
            # print(role,value["hardware_profile"])
            correct, wrong, total, result = HardwareValidation(role, self.json, value["hardware_profile"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = ("The number of correct :{} wrong:{} and total:{} in hardware profile\n\n".format(correct, wrong, total))
            self.result += result + string

            correct, wrong, total, string = StorageValidation(role, self.json, value["storage_mapping"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = ("The number of correct :{} wrong:{} and total:{} in storage profile\n\n".format(correct, wrong, total))
            self.result += result + string

            correct, wrong, total, string = PlatformValidation(role, self.json, value["platform_profile"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = ("The number of correct :{} wrong:{} and total:{} in platform profile\n\n".format(correct, wrong, total))
            self.result += result + string

            correct, wrong, total, string = NetworkValidation(role, self.json, value["interface_mapping"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = ("The number of correct :{} wrong:{} and total:{} in network profile\n\n".format(correct, wrong, total))
            self.result += result + string

        self.result += "Timestamp:{}\n".format(datetime.datetime.now())
        self.result += "correct:{} wrong:{} total:{}\n".format(self.correct, self.wrong, self.total)
        self.result += "percentage of correct:{:.2f} wrong:{:.2f}\n".format(self.correct / (self.correct + self.wrong), self.wrong / (self.correct + self.wrong))
        # print the final report
        self.logger.info("Validation complete!")
        return self.result

if __name__ == "__main__":
    # Initiate the parser
    parser = argparse.ArgumentParser(description="validation program")

    # Add long and short argument for test
    parser.add_argument("--test", help="test the code", action="store_true")

    # Add long and short argument for manifest dir
    parser.add_argument("--mani_dir", help="get manifest dir")

    # Add long and short argument for mapping dir
    parser.add_argument("--map_dir", help="get mapping dir")

    # Add long and short argument for pdf file
    parser.add_argument("--pdf", help="get pdf")

    # Read arguments from the command line
    args = parser.parse_args()

    if args.test:
        Validate(args.mani_dir, args.map_dir, args.pdf)
