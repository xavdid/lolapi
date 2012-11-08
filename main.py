import tornado.options 
import tornado.web
import tornado.httpserver 
import tornado.ioloop
import pymongo
import tornado.httpclient
import asyncmongo
import base
import routes
from tornado.options import define, options

class Application(tornado.web.Application): 
	def __init__(self):

		settings = {'static_path': 'static', 'debug': "True"}

		c = pymongo.Connection()
		self.db = c.loldbase #so, there's one database, "blog_database", here called loldbase.
		tornado.web.Application.__init__(self,base.route.get_routes(), **settings)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application()) 
	http_server.listen(options.port) 
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()