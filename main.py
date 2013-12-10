# import tornado.options 
import tornado.web
import tornado.httpserver 
import tornado.ioloop
import pymongo
import tornado.httpclient
# import asyncmongo
import base
import routes
import sys

class Application(tornado.web.Application): 
	def __init__(self):

		settings = {'static_path': 'static', 'debug': "True"}
		tornado.web.Application.__init__(self,base.route.get_routes(), **settings)

def main():
	try:
		port = int(sys.argv[1])
	except:
		port = 8888
	# tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application()) 
	http_server.listen(port) 
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()