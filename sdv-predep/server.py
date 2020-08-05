#!/usr/bin/env python

# pylint: disable=line-too-long, invalid-name, missing-module-docstring, broad-except

""" server code """

import os
import json
import logging
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import tornado.concurrent
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.options
import tornado.web
import tornado.log

from validation.validation import Validate
from extrapolation.extrapolation import Extrapolate


class ValidateJson(RequestHandler):
    "rest api class for validation "
    def set_default_headers(self):
        """ set default headers"""
        self.set_header('Content-Type', 'application/json')

    def post(self):
        """ consume post request """
        failures = 0

        # decode the body
        data = json.loads(self.request.body.decode())

        # check for keys
        try:
            data["pdf_file"]
        except Exception:
            app_log.error("pdf_file key does not exist")
            self.write("provide pdf_file key\n ")
            failures += 1

        try:
            data["inst_dir"]
        except Exception:
            app_log.error("inst_dir key does not exist")
            self.write("provide inst_dir key\n")
            failures += 1

        try:
            data["inst_type"]
        except Exception:
            app_log.error("inst_type key does not exist")
            self.write("provide inst_type key\n")
            failures += 1

        if failures == 0:
            pdf_file, inst_dir, inst_type = data["pdf_file"], data["inst_dir"], data["inst_type"]

            # check if the paths are relative or not
            if not os.path.isabs(pdf_file):
                app_log.critical("path provided for pdf is not an absolute path")
                self.write("provide absolute path for pdf\n ")
                failures += 1

            if not os.path.isabs(inst_dir):
                app_log.critical("path provided for inst_dir is not an absolute path")
                self.write("provide absolute path for inst_dir\n ")
                failures += 1

            if inst_type not in ["airship", "tripleo"]:
                app_log.error("only airship and tripleo are supported")
                self.write("only airship and tripleo are supported, for now.\n")
                failures += 1

            if failures == 0:
                # Validate('/home/ashwin/github/sdv/sdv-predep/data', '/home/ashwin/github/sdv/sdv-predep/mapping/airship', '/home/ashwin/github/sdv/sdv-predep/data/platform_description_16July2020.json').validate()
                result = Validate(inst_dir, inst_type, pdf_file).validate()
                self.write(result)


class ExtrapolateJson(RequestHandler):
    """rest api class for extrapolation"""
    def set_default_headers(self):
        """ set default header"""
        self.set_header('Content-Type', 'application/json')

    def post(self):
        """consume post request"""
        failures = 0

        data = json.loads(self.request.body.decode())

        # check for keys
        try:
            data["pdf_fn"]
        except Exception:
            app_log.error("pdf_fn key does not exist")
            self.write("provide pdf_file key\n ")
            failures += 1

        try:
            data["store_at"]
        except Exception:
            app_log.error("store-at key does not exist")
            self.write("provide store_at key\n ")
            failures += 1

        if failures == 0:
            pdf_fd = data["pdf_fn"]
            store_at = data["store_at"]

            # check if the paths are relative or not
            if not os.path.isabs(pdf_fd):
                app_log.critical("path provided for pdf is not an absolute path")
                self.write("provide absolute path for pdf\n ")
                failures += 1

            if not os.path.isabs(store_at):
                app_log.critical("path provided for store_at is not an absolute path")
                self.write("provide absolute path for store_at\n ")
                failures += 1

            if failures == 0:
                try:
                    Extrapolate(pdf_fd, store_at)
                    self.write({"message": "success! New pdf file:pd_new.json"})
                except Exception as e:
                    self.write({"message": "failure:"+str(e)})

def make_app():
    """url mapping to class """
    urls = [
        ("/validate", ValidateJson),
        ("/extrapolate", ExtrapolateJson)
    ]
    return Application(urls, debug=True)

if __name__ == '__main__':
    # app config
    app = make_app()

    # Cli Config
    tornado.options.define("port", default=8888, help="run on the given port", type=int)
    tornado.options.parse_command_line()

    # Server Config
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)

    # Tornado's event loop handles it from here
    print("Starting Tornado server.....")

    # Logging
    log_file_filename = "tornado.log"
    handler = logging.FileHandler(log_file_filename)
    app_log = logging.getLogger("tornado.general")
    tornado.log.enable_pretty_logging()
    app_log.addHandler(handler)

    # Start Loop
    tornado.ioloop.IOLoop.current().start()

    # start
    IOLoop.instance().start()
