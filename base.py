import tornado.web
import tornado.httpserver 
import tornado.ioloop
import pymongo
import tornado.httpclient
from tornado.web import HTTPError
import asyncmongo
from tornado.options import define, options
from dictshield.document import Document
# from dictshield.fields.mongo import ObjectIdField 
from dictshield.fields import StringField, DictField, BooleanField, IntField, FloatField

define("port", default=8888, help="run on the given port", type=int)

class route(object):
    _routes = []

    def __init__(self, uri, name=None):
        self._uri = uri
        self.name = name

    def __call__(self, _handler):
        name = self.name and self.name or _handler.__name__
        self._routes.append(tornado.web.url(self._uri, _handler, name=name))
        return _handler

    @classmethod
    def get_routes(self):
        return self._routes

class BaseAPIHandler(tornado.web.RequestHandler):
    pass
'''
class Champion(object):
	name = ''
	hp_base = 0
	hp_ratio = 0
	hpreg_base = 0
	hpreg_ratio = 0
	mana_base = 0
	mana_ratio = 0
	manareg_base = 0
	manareg_ratio = 0
	arange = 0
	ad_base = 0
	ad_ratio = 0
	armor_base = 0
	armor_ratio = 0
	mr_base = 0
	move = 0
	statsvars = [name,hp_base,hp_ratio,hpreg_base,hpreg_ratio,mana_base,mana_ratio,manareg_base,manareg_ratio,
	arange,ad_base,ad_ratio,armor_base,armor_ratio,mr_base,move]
	def disp():
		x=0
		for stat in statsvars:
			print statsname[1]+": "+stat+"\n"
'''
class Champion(Document):
	name = StringField(required = True)
	stats = DictField()




