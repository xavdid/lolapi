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
from functions import moveMult, statMult, attach, getChamp, itemMult
from pprint import pprint

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

class ChampBase(Document):
    name = StringField(required = True)
    title = StringField()
    stats = DictField()
    moves = DictField()
    
class ItemBase(Document):
    items = DictField()
    name = StringField(required = True)

class Champion(object):
    def __init__(self, cd):
        self.c = cd
        self.cur_stats = {}
        self.setBase()
        self.resetStats()
        self.items = []
        attach(self,cd)

    def setBase(self):
        # self.cur_stats 
        self.cur_stats = {'hp':0,'hpreg':0,'mana':0,'manareg':0,'ad':0,'ap':0,'ms':0,'as':0,'armor':0,'mr':0,'crit':0,
            'lifesteal':0,'spellvamp':0}

    def resetStats(self):
        for s in self.cur_stats:
            self.cur_stats[s] = statMult(self.c['stats'],s,18)

    def doItems(self):
        i = getChamp('items')
        # pprint(i)
        for e in self.items:
            for s in i['items'][e]['effect']:
                self.cur_stats[s] += i['items'][e]['effect'][s]

# this doesn't reattach to the dictfields because it's not needed in the accessing
class Ahri(Champion):
    def __init__(self,cd):
        # print dir(self)
        super(Ahri, self).__init__(cd)
        # self.poop = {}
        # ChampBase.setBase(self.poop)
        # self.c = cd
        # self.cur_stats = 

    # also may want to change this response from an int to json?
    def q(self):
        return moveMult(self.c['moves']['q']['damage'],5,self.cur_stats['ap'],self.c['moves']['q']['damage_ratio']) 
    def q2(self):
        return moveMult(self.c['moves']['q']['damage_2'],5,self.cur_stats['ap'],self.c['moves']['q']['damage_2_ratio'])
    def w(self):
        return moveMult(self.c['moves']['w']['damage'],5,self.cur_stats['ap'],self.c['moves']['w']['damage_ratio'])
    def e(self):
        return moveMult(self.c['moves']['e']['damage'],5,self.cur_stats['ap'],self.c['moves']['e']['damage_ratio'])
    def r(self):
        return moveMult(self.c['moves']['r']['damage'],3,self.cur_stats['ap'],self.c['moves']['r']['damage_ratio'])

class Akali(Champion):
    def __init__(self,cd):
        super(Akali, self).__init__(cd)

    def setBase(self):
        # self.cur_stats 
        self.cur_stats = {'hp':0,'hpreg':0,'energy':0,'ad':0,'ap':0,'ms':0,'as':0,'armor':0,'mr':0,'crit':0,
            'lifesteal':0,'spellvamp':0}

# This is for storing dictionaries that are new champs




# def doItems(ch,i):
