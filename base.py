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
    
    # def cur():
        # return cur_stats

class Item(Document):
    price = IntField()

class ChampBase(object):
    def __init__(self, ch):
        self.c = ch
        self.cur_stats = ch['stats']
        self.cur_stats['ap'] = 0

'''this doesn't reattach to the dictfields because it's not needed in the accessing'''
class Ahri(ChampBase):

    # can't hardcode that 500
    # also may want to change this response from an int to json?
    def q(self):
        return movemult(self.c['moves']['q']['damage'],5,self.cur_stats['ap'],self.c['moves']['q']['damage_ratio']) 
    def q2(self):
        return movemult(self.c['moves']['q']['damage_2'],5,self.cur_stats['ap'],self.c['moves']['q']['damage_2_ratio'])
    def w(self):
        return movemult(self.c['moves']['w']['damage'],5,self.cur_stats['ap'],self.c['moves']['w']['damage_ratio'])
    def e(self):
        return movemult(self.c['moves']['e']['damage'],5,self.cur_stats['ap'],self.c['moves']['e']['damage_ratio'])
    def r(self):
        return movemult(self.c['moves']['r']['damage'],3,self.cur_stats['ap'],self.c['moves']['r']['damage_ratio'])

'''This is for storing dictionaries that are new champs'''
def attach(c,ch):
    ch.name = c['name']
    ch.title = c['title']
    ch.stats = c['stats']
    ch.moves = c['moves']
