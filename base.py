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
from pprint import pprint

define("port", default=8888, help="run on the given port", type=int)

class route(object):
    _routes = []

    def __init__(self,uri,name=None):
        self._uri = uri
        self.name = name

    def __call__(self,_handler):
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
    def __init__(self,cd):
        self.c = cd
        self.cur_stats = {}
        self.setBase()
        self.resetStats()
        self.items = []  
        self.ninja = False
        attach(self,cd)

    def setBase(self):
        # self.cur_stats 
        self.cur_stats = {'level':0,'hp':0,'hp_max':0,'mana_max':0,'hp_regen':0,'mana':0,'mana_regen':0,'ad':0,'ap':0,'ms':0,'as':0,'armor':0,
            'mr':0,'crit':0,'lifesteal':0,'spellvamp':0,'flat_armor_pen':0,'flat_magic_pen':0,'perc_armor_pen':0,'perc_magic_pen':0,
                'cdr':0,'damage_block':0,'on_hit':{},'on_self_hit':{},'status':{},'cooldowns':{'i':0,'q':0,'w':0,'e':0,'r':0},'ability_rank':{'q':0,'w':0,'e':0,'r':0}}
        #for debugging so that all the abilities are up: 
        for a in self.cur_stats['ability_rank']:
            if a == 'r':
                self.cur_stats['ability_rank'][a] = 3
            else:
                self.cur_stats['ability_rank'][a] = 5

    def resetStats(self):
        for s in self.cur_stats:
            if isinstance(self.cur_stats[s],int):
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
                    try:
                        self.cur_stats[s] += i['items'][e]['effect'][s]
                    except KeyError:
                        continue
        self.cur_stats['hp'] = self.cur_stats['hp_max']
        # self.cur_stats['mana'] = self.cur_stats['mana_max'] #FIX FOR NINJA

    def getAbility(self, ability):
        response = {}
        if 'damage' in self.c['moves'][ability]:
            response['damage'] = moveMult(self.c['moves'][ability]['damage'],self.cur_stats['ability_rank'][ability],
                self.cur_stats[self.c['moves'][ability]['damage_ratio_type']],self.c['moves'][ability]['damage_ratio'])
            response['dtype'] = self.c['moves'][ability]['damage_type']
        elif 'effect' in self.c['moves'][ability]:
            for k in self.c['moves']['w']['effect']:
                response[k] = self.c['moves'][ability]['effect'][k][self.cur_stats['ability_rank'][ability]]
        return response

    def ad(self):
        return self.cur_stats['ad']
    def ap(self):
        return self.cur_stats['ap']
    def hp(self,val=0):
        if (val):
            self.cur_stats['hp'] += val
            if self.cur_stats['hp'] > self.cur_stats['hp_max']:
                self.cur_stats['hp'] = self.cur_stats['hp_max']
            elif self.cur_stats['hp'] < 0:
                self.cur_stats['hp'] = 0
        else:
            return self.cur_stats['hp']
    def mana(self,val=0):
        if (val):
            self.cur_stats['mana'] += val
            if self.cur_stats['mana'] > self.cur_stats['mana_max']:
                self.cur_stats['mana'] = self.cur_stats['mana_max']
            elif self.cur_stats['mana'] < 0:
                self.cur_stats['mana'] = 0
        else:
            return self.cur_stats['mana']
    def armor(self):
        return self.cur_stats['armor']
    def mr(self):
        return self.cur_stats['mr']
    def tick(self):
        self.hpRegen()
        self.secondaryRegen()
        self.cooldowns()
    def hpRegen(self):
        if self.cur_stats['hp'] < self.cur_stats['hp_max']:
            self.hp(self.cur_stats['hp_regen']/5.0)
    def secondaryRegen(self): #this is named as such as to account for fury and energy so I don't always need to redefine tick()
        if self.cur_stats['mana'] < self.cur_stats['mana_max']:
            self.mana(self.cur_stats['mana_regen']/5.0)
    def cooldowns(self):
        for a in self.cur_stats['cooldowns']:
            if self.cur_stats['cooldowns'][a] > 0:
               self.cur_stats['cooldowns'][a] -= 1
    def setCooldowns(self,ability):
        self.cur_stats['cooldowns'][ability] = self.c['moves'][ability]['cd'][self.cur_stats['ability_rank'][ability]]
    def canCast(self,ability): #this will at some point need to account for being silenced
        if (self.c['moves'][ability]['cost_val'][self.cur_stats['ability_rank'][ability]] < self.cur_stats[self.c['moves'][ability]['cost_type']] 
            and self.cur_stats['cooldowns'][ability] == 0):
                return True
        else:
            if 'on' in self.c['moves'][ability]:
                self.c['moves'][ability]['on'] = False
            return False

    def useAbility(self,ability,handler,*args): #REMOVE HANDLER LATER, IT'S JUST FOR TESTING I THINK
        if self.canCast(ability):#if you can cast
            if self.ninja: #spend energy if ninja
                self.energy(-(self.c['moves'][ability]['cost_val'][self.cur_stats['ability_rank'][ability]]))
            else: #spend mana
                self.mana(-(self.c['moves'][ability]['cost_val'][self.cur_stats['ability_rank'][ability]]))

            if 'on' in self.c['moves'][ability]: #decides whether or not the ability is a toggle one
                if self.c['moves'][ability]['on'] == True: #toggling off
                    self.c['moves'][ability]['on'] = False
                    self.setCooldowns(ability)
                elif self.c['moves'][ability]['on'] == False: #toggling on|| technically some abilities have a cooldown when you turn them on but i wont sweat that now
                    self.c['moves'][ability]['on'] = True
            else: 
                self.setCooldowns(ability)

            abi = self.getAbility(ability) #gets the dictionary of the ability (any combination of damage, cc, steriod, etc)
            for k in abi:
                if k == 'damage':
                    for targ in args:
                        d = damageCalc(self,targ,abi)
                        targ.hp(-d)
        else:
            # print 'can\'t cast now, sorry'
            handler.write(' ||can\'t cast now, sorry|| ')

class Ninja(Champion):
    def __init__(self,cd):
        super(Ninja, self).__init__(cd)
        self.ninja = True

    def setBase(self):
        # self.cur_stats 
        self.cur_stats = {'level':0,'hp':0,'hp_max':0,'hp_regen':0,'energy':0,'ad':0,'ap':0,'ms':0,'as':0,'armor':0,'mr':0,'crit':0,
            'lifesteal':0,'spellvamp':0,'flat_armor_pen':0,'flat_magic_pen':0,'perc_armor_pen':0,'perc_magic_pen':0,
                'cdr':0,'damage_block':0,'on_hit':{},'on_self_hit':{},'status':{},'cooldowns':{'i':0,'q':0,'w':0,'e':0,'r':0},'ability_rank':{'q':0,'w':0,'e':0,'r':0}}
        for a in self.cur_stats['ability_rank']:
            if a == 'r':
                self.cur_stats['ability_rank'][a] = 3
            else:
                self.cur_stats['ability_rank'][a] = 5

    def energy(self, val=0):
        if val:
            self.cur_stats['energy']+=val
            if self.cur_stats['energy'] > 200:
                self.cur_stats['energy'] = 200
            elif self.cur_stats['energy'] < 0:
                self.cur_stats['energy'] = 0
        else: 
            return self.cur_stats['energy']

    def secondaryRegen(self):
        if self.cur_stats['energy'] < 200:
            self.energy(5)

# this doesn't reattach to the dictfields because it's not needed in the accessing
class Ahri(Champion):
    def __init__(self,cd):
        super(Ahri, self).__init__(cd)

    # also may want to change this response from an int to json?
    def q(self, dypte = False):
        response = {}
        if (dtype):
            response['dtype'] = self.c['moves']['q']['damage_type']
        else:
            response['damage'] = moveMult(self.c['moves']['q']['damage'],self.cur_stats['ability_rank']['q'],
                self.cur_stats[self.c['moves']['q']['damage_ratio_type']],self.c['moves']['q']['damage_ratio'])
            response['damage2'] = moveMult(self.c['moves']['q']['damage_2'],self.cur_stats['ability_rank']['q'],
                self.cur_stats[self.c['moves']['q']['damage_ratio_type']],self.c['moves']['q']['damage_2_ratio'])
        return response

class Akali(Ninja):
    def __init__(self,cd):
        super(Akali, self).__init__(cd)

    def e(self, dtype = False):
        if (dtype):
            return self.c['moves']['e']['damage_type']
        else:
            return moveMult(self.c['moves']['e']['damage'],self.cur_stats['ability_rank']['e'],self.cur_stats[self.c['moves']['e']['damage_ratio_type']],
                self.c['moves']['e']['damage_ratio'],self.cur_stats[self.c['moves']['e']['damage_ratio_type_b']],self.c['moves']['e']['damage_ratio_b'])

class Alistar(Champion):
    def __init__(self,cd):
        super(Alistar, self).__init__(cd)

    def e(self, dtype = False):
        response = {}
        if (dtype):
            pass
        else:
            response['self_heal'] = moveMult(self.c['moves']['e']['self_heal_val'],self.cur_stats['ability_rank']['e'],
                self.cur_stats[self.c['moves']['e']['heal_ratio_type']],self.c['moves']['e']['self_heal_ratio'])
            response['ally_heal'] = moveMult(self.c['moves']['e']['ally_heal_val'],self.cur_stats['ability_rank']['e'],
                self.cur_stats[self.c['moves']['e']['ally_heal_ratio_type']],self.c['moves']['e']['ally_heal_ratio'])
            return response

class Amumu(Champion):
    def __init__(self,cd):
        super(Amumu, self).__init__(cd)

    def w(self, dtype = False):
        if (dtype):
            return self.c['moves']['w']['damage_type']
        else:
            return (moveMult(self.c['moves']['w']['damage_b'],self.cur_stats['ability_rank']['w'],
                self.cur_stats[self.c['moves']['w']['damage_ratio_type_b']],self.c['moves']['w']['damage_ratio_b']) 
                + self.c['moves']['w']['damage'][self.cur_stats['ability_rank']['w']])

    def tick(self):
        self.hpRegen()
        self.secondaryRegen()
        if (self.c['moves']['w']['on']):
            self.mana(-8)
        self.cooldowns()


