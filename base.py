import tornado.web
import tornado.httpserver 
import tornado.ioloop
import pymongo
import tornado.httpclient
from tornado.web import HTTPError
import asyncmongo
from tornado.options import define, options
from dictshield.document import Document
from dictshield.fields import (StringField, DictField, BooleanField, IntField, FloatField)
from dictshield.fields.compound import ListField
from functions import movemult, statmult

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

class Champion(Document):
    name = StringField(required = True)
    title = StringField()
    stats = DictField()
    moves = DictField()
    items = ListField(IntField())

class Ahri(Champion):
    def __init__(self, ch):
        self.c = ch

    # can't hardcode that 500
    def q(self):
        return(movemult(self.c['moves']['q']['damage'],5,500,self.c['moves']['q']['damage_ratio']))



