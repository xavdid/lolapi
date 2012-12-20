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
from functions import *
# from functions import moveMult, statMult, attach, getChamp, itemMult
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
        self.cur_stats = {'hp':0,'hp_max':0,'mana_max':0,'hpreg':0,'mana':0,'manareg':0,'ad':0,'ap':0,'ms':0,'as':0,'armor':0,
            'mr':0,'crit':0,'lifesteal':0,'spellvamp':0,'flat_armor_pen':0,'flat_magic_pen':0,'perc_armor_pen':0,'perc_magic_pen':0,
                'cdr':0,'damage_block':0,'onhit':{}}

    def resetStats(self):
        for s in self.cur_stats:
            self.cur_stats[s] = statMult(self.c['stats'],s,18)

    def doItems(self):
        i = getChamp('items')
        # pprint(i)
        for e in self.items:
            for s in i['items'][e]['effect']:
                if (s == 'armor_pen' or s == 'magic_pen'):
                    if (i['items'][e]['effect'][s]['type'] == 'flat'):
                        self.cur_stats['flat_'+s] += i['items'][e]['effect'][s]['val']
                    else:
                        self.cur_stats['perc_'+s] += i['items'][e]['effect'][s]['val']
                else:
                    self.cur_stats[s] += i['items'][e]['effect'][s]

    def q(self, dtype = False):
        if (dtype):
            return self.c['moves']['q']['damage_type']
        else: return moveMult(self.c['moves']['q']['damage'],5,self.cur_stats[self.c['moves']['q']['damage_ratio_type']],self.c['moves']['q']['damage_ratio']) 
    def w(self, dtype = False):
        if (dtype):
            return self.c['moves']['w']['damage_type']
        else: return moveMult(self.c['moves']['w']['damage'],5,self.cur_stats[self.c['moves']['w']['damage_ratio_type']],self.c['moves']['w']['damage_ratio']) 
    def e(self, dtype = False):
        if (dtype):
            return self.c['moves']['e']['damage_type']
        else: return moveMult(self.c['moves']['e']['damage'],5,self.cur_stats[self.c['moves']['e']['damage_ratio_type']],self.c['moves']['e']['damage_ratio']) 
    def r(self, dtype = False):
        if (dtype):
            return self.c['moves']['r']['damage_type']
        else: return moveMult(self.c['moves']['r']['damage'],3,self.cur_stats[self.c['moves']['r']['damage_ratio_type']],self.c['moves']['r']['damage_ratio'])
    def ad(self):
        return self.cur_stats['ad']
    def ap(self):
        return self.cur_stats['ap']
    def hp(self, val=0):
        if (val):
            self.cur_stats['hp'] += val
            if self.cur_stats['hp'] > self.cur_stats['hp_max']:
                self.cur_stats['hp'] = self.cur_stats['hp_max']
        else:
            return self.cur_stats['hp']
    def mana(self, val=0):
        if (val):
            self.cur_stats['mana'] += val
            if self.cur_stats['mana'] > self.cur_stats['mana_max']:
                self.cur_stats['mana'] = self.cur_stats['mana_max']
        else:
            return self.cur_stats['mana']
    def armor(self):
        return self.cur_stats['armor']
    def mr(self):
        return self.cur_stats['mr']
    def regen(self):
        self.hpRegen()
        self.secRegen()
    def hpRegen(self):
        if self.cur_stats['hp'] < self.cur_stats['hp_max']:
            self.hp(self.cur_stats['hpreg']/5)
    def secRegen(self):
        if self.cur_stats['mana'] < self.cur_stats['mana_max']:
            self.hp(self.cur_stats['manareg']/5)

class Ninja(Champion):
    def __init__(self,cd):
        super(Ninja, self).__init__(cd)

    def setBase(self):
        # self.cur_stats 
        self.cur_stats = {'hp':0,'hp_max':0,'hpreg':0,'energy':0,'ad':0,'ap':0,'ms':0,'as':0,'armor':0,'mr':0,'crit':0,
            'lifesteal':0,'spellvamp':0,'flat_armor_pen':0,'flat_magic_pen':0,'perc_armor_pen':0,'perc_magic_pen':0,
                'cdr':0,'damage_block':0,'onhit':{}}

    def energy(self, val=0):
        if val:
            self.cur_stats['energy']+=val
        else: 
            return self.cur_stats['energy']

    def secRegen(self):
        if self.cur_stats['energy'] < 200:
            self.energy(5)

# this doesn't reattach to the dictfields because it's not needed in the accessing
class Ahri(Champion):
    def __init__(self,cd):
        super(Ahri, self).__init__(cd)

    # also may want to change this response from an int to json?
    def q2(self):
        return moveMult(self.c['moves']['q']['damage_2'],5,self.cur_stats[self.c['moves']['q']['damage_ratio_type']],self.c['moves']['q']['damage_2_ratio'])
    

class Akali(Ninja):
    def __init__(self,cd):
        super(Akali, self).__init__(cd)

    def w(self):
        return 0

    def e(self):
        return moveMult(self.c['moves']['e']['damage'],5,self.cur_stats[self.c['moves']['e']['damage_ratio_type']],self.c['moves']['e']['damage_ratio'],self.cur_stats[self.c['moves']['e']['damage_ratio_type_b']],self.c['moves']['e']['damage_ratio_b'])

class Alistar(Champion):
    def __init__(self,cd):
        super(Alistar, self).__init__(cd)

    def e(self):
        return moveMult(self.c['moves']['e']['self_heal_val'],5,self.cur_stats[self.c['moves']['e']['heal_ratio_type']],self.c['moves']['e']['self_heal_ratio']) 
