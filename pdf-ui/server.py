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

import pygit2
from github import Github

class Authentication(RequestHandler):
    """ github application """

    def get(self):
        self.write({"session_id":443211})


class WriteJson(RequestHandler):
    """ write json to github """
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
    
    def write_to_github(self, data):
        # using username and password establish connection to github
        g = Github(userName, password)

        #Clone the newly created repo
        repoClone = pygit2.clone_repository(git_url, '/path/to/clone/to')

        #put the files in the repository here

        #Commit it
        repoClone.remotes.set_url("origin", git_url)
        index = repoClone.index
        index.add_all()
        index.write()
        author = pygit2.Signature("your name", "your email")
        commiter = pygit2.Signature("your name", "your email")
        tree = index.write_tree()
        oid = repoClone.create_commit('refs/heads/master', author, commiter, "init commit",tree,[repoClone.head.get_object().hex])
        remote = repoClone.remotes["origin"]
        credentials = pygit2.UserPass(userName, password)
        remote.credentials = credentials

        callbacks=pygit2.RemoteCallbacks(credentials=credentials)

        remote.push(['refs/heads/master'],callbacks=callbacks)

        # delete the cloned file

        return None
    
    def post(self):
        data = json.loads(self.request.body.decode())

        try:
            self.write_to_github(data)
            self.write({"message":"sucess"})
        except Exception as e:
            self.write({"message":"failure due to" + str(e)})

class ReadJson(RequestHandler):
    """ read json from github """
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
    
    def read_from_github(self, data):
        # using username and password establish connection to github
        g = Github(userName, password)

        #Clone the newly created repo
        repoClone = pygit2.clone_repository(git_url, '/path/to/clone/to')

        # read the file

        # delete the cloned file

        return None
    
    def post(self):
        data = json.loads(self.request.body.decode())

        try:
            self.read_from_github(data)
            self.write({"message":"sucess"})
        except Exception as e:
            self.write({"message":"failure due to" + str(e)})

class ListSite(RequestHandler):
    """ get list of sites """
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def get_list_site(self):
        g = github.Github("USERNAME", "PASSWORD")
        repo = g.get_user().get_repo( "REPO_NAME" )
        return  list(repo.get_dir_contents(""))
    
    def get(self):
        data = self.get_list_site()
        self.write(data)

class NewSite(RequestHandler):
    """ create a new site """
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def write_to_github(self, data):
        # using username and password establish connection to github
        g = Github(userName, password)

        #Clone the newly created repo
        repoClone = pygit2.clone_repository(git_url, '/path/to/clone/to')

        #create a new file in the repository here

        #Commit it
        repoClone.remotes.set_url("origin", git_url)
        index = repoClone.index
        index.add_all()
        index.write()
        author = pygit2.Signature("your name", "your email")
        commiter = pygit2.Signature("your name", "your email")
        tree = index.write_tree()
        oid = repoClone.create_commit('refs/heads/master', author, commiter, "init commit",tree,[repoClone.head.get_object().hex])
        remote = repoClone.remotes["origin"]
        credentials = pygit2.UserPass(userName, password)
        remote.credentials = credentials

        callbacks=pygit2.RemoteCallbacks(credentials=credentials)

        remote.push(['refs/heads/master'],callbacks=callbacks)

        # delete the cloned file

        return None        
    
    def get(self):
        data = self.get_argument('sitename', None)

        try:
            self.write_to_github(data)
            self.write({"message":"sucess"})
        except Exception as e:
            self.write({"message":"failure due to" + str(e)})

def make_app():
    urls = [
        ("/authentication", Authentication),
        ("/write-json", WriteJson),
        ("/read-json", ReadJson),
        ("/list-site", ListSite),
        ("/new-site", NewSite)
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