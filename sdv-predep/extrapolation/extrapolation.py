#!/usr/bin/env python

# pylint: disable=line-too-long, invalid-name

""" program to perform extrapolation """

import os
import json
import logging
import sys
import argparse
from netaddr import IPNetwork

class Extrapolate():
    """Perform extrapolation"""
    def __init__(self, pdf_fn, store_at):
        self.store_at = store_at

        self.pdf = dict()
        self.ip_list = []

        self.start_logger()
        self.read_pdf(pdf_fn)
        self.get_ip("192.168.10.0/24") # temp value!
        self.extrapolate()

    def start_logger(self):
        """ starting logging process """
        logging.basicConfig(filename='extrapolation.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

        self.logger = logging.getLogger('extrapolation')
        self.logger.info("Starting extrapolation program")

    def read_pdf(self, json_fn):
        """ read platform descritpion file """
        try:
            with open(os.path.join(json_fn)) as json_file:
                self.logger.info("Reading the pdf file:%s", json_fn)
                self.pdf = json.loads(json_file.read())
        except IOError as e:
            self.logger.critical("Error while reading the pdf file: %s", str(e))
            sys.exit()

    def save_pdf(self):
        """ save the pdf file """
        try:
            with open(os.path.join(self.store_at, 'pdf_new.json'), 'w', encoding='utf-8') as json_file:
                self.logger.info("Saving the extrapolated pdf file")
                json.dump(self.pdf, json_file, indent=2)
        except IOError as e:
            self.logger.error("Could not save the logger file: %s", str(e))

    def get_ip(self, value):
        """ get list of valid ip's"""
        self.logger.info("getting list of ip's from %s", value)
        for ip in IPNetwork(value):
            if str(ip).split('.')[-1] != '0' and str(ip).split('.')[-1] != '255':
                self.ip_list.append(str(ip))

    def get_ipmi_info(self, count):
        """get ipmi info """
        temp = dict()
        if count > len(self.ip_list):
            self.logger.error("No ip's avaialble!")
        elif not self.pdf["extrapolation_info"]["ip_increment"].isdigit():
            self.logger.error("ip increment value is not an integer")
        else:
            temp["ip"] = self.ip_list[count * int(self.pdf["extrapolation_info"]["ip_increment"])]
            temp["user"] = self.pdf["extrapolation_info"]["ilo_user"]
            temp["password"] = self.pdf["management_info"]["city"]+self.pdf["management_info"]["area_name"]\
                +self.pdf["management_info"]["room_id"]+str(count + 1)

        return temp

    def extrapolate(self):
        """ Perform Extrapolation """
        self.logger.info("starting extrapolation")

        list_servers = []

        # get ipmi info
        count = 0

        for val in self.pdf["roles"]:
            n = int(val["count"]) # Number of servers in the particular role.
            role = val["name"]


            for _ in range(n):
                temp = dict()
                temp["role_name"] = role
                temp["device_name"] = role + str(count + 1)
                temp["az_name"] = str(count + 1)
                temp["ha_name"] = str(count + 1)

                temp["ilo_info"] = self.get_ipmi_info(count)
                count += 1

                list_servers.append(temp)

        # save the pdf file
        self.pdf["servers"] = list_servers
        self.save_pdf()

        self.logger.info("Extrapolation completed!")

if __name__ == "__main__":
    # main class is for testing purposes
    # Initiate the parser
    parser = argparse.ArgumentParser(description="Extrapolation program")

    # Add long and short argument for test
    parser.add_argument("--test", help="test the code", action="store_true")

    # Add long and short argument for pdf file
    parser.add_argument("--file", help="get pdf file name")

    # Read arguments from the command line
    args = parser.parse_args()

    if args.test:
        Extrapolate(args.file)
