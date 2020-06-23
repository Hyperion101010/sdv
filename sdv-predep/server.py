#!/usr/bin/env python

# pylint: disable=line-too-long, invalid-name, missing-module-docstring

from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
import logging
import tornado.concurrent
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.options
import tornado.web
import tornado.log

from extrapolation import Extrapolate
from validation import Validate

class ValidateJson(RequestHandler):

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def post(self):
        data = json.loads(self.request.body.decode())
        pdf_fn, inst_fn, map_fn = data["pdf_fn"], data["inst_fn"], data["map_fn"]
        key = data["key"]

        result = Validate(pdf_fn, inst_fn, map_fn).check_match(key)

        self.write({"result": result})


class ExtrapolateJson(RequestHandler):

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def post(self):
        data = json.loads(self.request.body.decode())
        pdf_fd = data["pdf_fn"]

        try:
            Extrapolate(pdf_fd).extrapolate()
            self.write({"message": "success! New pdf file:pd_new.json"})
        except Exception as e:
            self.write({"message": "failure:"+str(e)})

def make_app():
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