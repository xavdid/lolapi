import tornado.web
import pymongo
from tornado.web import HTTPError
from dictshield.document import Document
from dictshield.fields import (StringField, DictField)
from dictshield.fields.compound import ListField
from functions import *
import random
import copy


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
        self.ablist = {}
        attach(self,cd)

    def showStats(self,full=False):#will change for command line- doesn't need handler, can just take print
        if full:
            slist = ['level','hp','mana','energy','hp_regen','mana_regen','ad','ap','as','armor','mr','crit_chance','lifesteal','spellvamp','cdr','on_enemy_hit','on_self_hit','bonus_stats']
        else:
            slist = ['hp','mana','energy','ad','ap','as','armor','mr']
        alist = ['q','w','e','r']
        for s in slist:
            try:
                st = self.cur_stats[s]
                if s == 'hp' or s == 'mana' or s == 'energy':
                    print reverseNamer(s).title()+': %0.1f/%s'%(st,str(self.cur_stats[s+'_max']))
                elif s == 'ad' or s == 'ap' or s == 'armor' or s == 'mr':
                    func = getattr(self, s, None)
                    f = func()
                    print reverseNamer(s).title()+': %.1f'%f
                else:
                    try:
                        print reverseNamer(s).title()+': %0.2f' %st
                    except:
                        print reverseNamer(s).title()+':',st
            except KeyError:
                pass

        print 'Cooldowns:'
        for a in alist:
            print a+':',self.cur_stats['cooldowns'][a]
        print 'Status:'
        if len(self.cur_stats['status']) == 0:
            print None
        else:
            for st in self.cur_stats['status']:
                print st.title(),self.cur_stats['status'][st]

    def showItems(self):
        k = getChamp('items')
        x = 0
        for i in self.items:
            print str(x)+':',k['items'][i]['name']
            x+=1

    def setBase(self):
        # self.cur_stats 
        self.cur_stats = {'level':0,'hp':0,'hp_max':0,'mana_max':0,'hp_regen':0,'mana':0,'mana_regen':0,'ad':0,'ap':0,'ms':0,'as':0,'armor':0,
            'mr':0,'crit_chance':0,'lifesteal':0,'spellvamp':0,'flat_armor_pen':0,'flat_magic_pen':0,'perc_armor_pen':0,'perc_magic_pen':0,
                'cdr':0,'damage_block':0,'on_enemy_hit':[],'on_self_hit':[],'status':{},'cooldowns':{'p':0,'q':0,'w':0,'e':0,'r':0},
                'ability_rank':{'q':0,'w':0,'e':0,'r':0},'bonus_stats':{'ad':0,'ap':0,'hp':0,'mana':0,'armor':0,'mr':0,'ms':0,'as':0}}
        #for debugging so that all the abilities are maxed: 
        for a in self.cur_stats['ability_rank']:
            if a == 'r':
                self.cur_stats['ability_rank'][a] = 3
            else:
                self.cur_stats['ability_rank'][a] = 5

    def resetStats(self):
        for s in self.cur_stats:
            if isinstance(self.cur_stats[s],float) or isinstance(self.cur_stats[s],int):
                self.cur_stats[s] = statMult(self.c['stats'],s,18) #hardcoded for 18, will change to champ level later

    def doItems(self):
        self.resetStats()
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
        if self.ninja:
            self.cur_stats['energy'] = 200
        else:
            self.cur_stats['mana'] = self.cur_stats['mana_max']

    def getAbility(self, ability):
        response = {}
        ab = getattr(self, ability, None)
        if callable(ab):
            response = ab()
            response['dtype'] = ab(True)
        elif 'damage' in self.moves[ability]:
            response['damage'] = moveMult(self.moves[ability]['damage'], self.cur_stats['ability_rank'][ability],
                self.cur_stats[self.moves[ability]['damage_ratio_type']], self.moves[ability]['damage_ratio'])
            response['dtype'] = self.moves[ability]['damage_type']
        if 'scaling' in self.moves[ability]:
            response['scaling'] = self.moves[ability]['scaling'] #that is, what it scales on
        response['name'] = self.moves[ability]['name']

        return response
#these functions return the base+bonus for their given stat
    def ad(self):
        return self.cur_stats['ad']+self.cur_stats['bonus_stats']['ad']
    def ap(self):
        return self.cur_stats['ap']+self.cur_stats['bonus_stats']['ap']
    def hp(self,val=0):
        if (val):
            self.cur_stats['hp'] += val
            if self.cur_stats['hp'] > self.cur_stats['hp_max']+self.cur_stats['bonus_stats']['hp']:
                self.cur_stats['hp'] = self.cur_stats['hp_max']+self.cur_stats['bonus_stats']['hp']
            elif self.cur_stats['hp'] < 0:
                self.cur_stats['hp'] = 0
        else:
            return self.cur_stats['hp']
    def mana(self,val=0):
        if (val):
            self.cur_stats['mana'] += val
            if self.cur_stats['mana'] > self.cur_stats['mana_max']+self.cur_stats['bonus_stats']['mana']:
                self.cur_stats['mana'] = self.cur_stats['mana_max']+self.cur_stats['bonus_stats']['mana']
            elif self.cur_stats['mana'] < 0:
                self.cur_stats['mana'] = 0
        else:
            return self.cur_stats['mana']
    def armor(self):
        return self.cur_stats['armor']+self.cur_stats['bonus_stats']['armor']
    def mr(self):
        return self.cur_stats['mr']+self.cur_stats['bonus_stats']['mr']
    def ats(self): #as is reserved in python, bummer
        return self.cur_stats['as']*(1+self.cur_stats['bonus_stats']['as'])

#these take care of maitenence stuff (cooldowns, bs, etc)
    def tick(self):
        self.hpRegen()
        self.secondaryRegen()
        self.cooldowns()
        self.statusTimers()
        self.checkStats()

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
    def statusTimers(self):
        # print 'checking!'
        poplist = []
        for b in self.cur_stats['status']:
            if self.cur_stats['status'][b] == 0:
                pass
            elif 'duration' in self.cur_stats['status'][b]:
                self.cur_stats['status'][b]['duration'] -= 1
                if self.cur_stats['status'][b]['duration'] <= 0:
                    poplist.append(b)
        for d in poplist:
            for e in self.cur_stats['status'][d]['effect']:
                if e == 'on_self_hit' or e == 'on_enemy_hit':
                    self.cur_stats[e].remove(self.cur_stats['status'][d]['effect'][e])
            self.cur_stats['status'].pop(d)
        self.checkStats()
    def setCooldowns(self,ability):
        self.cur_stats['cooldowns'][ability] = self.moves[ability]['cooldown'][self.cur_stats['ability_rank'][ability]]
    def canCast(self,ability):
        if (self.moves[ability]['cost'][self.cur_stats['ability_rank'][ability]] < self.cur_stats[self.moves[ability]['cost_type']] 
            and self.cur_stats['cooldowns'][ability] <= 0 and 'taunt' not in self.cur_stats['status'] and 'stun' not in self.cur_stats['status'] 
            and 'taunt' not in self.cur_stats['status']):
                # print 'true'
                return True
        else:
            if 'on' in self.moves[ability]:
                self.moves[ability]['on'] = False
                print 'Toggling off'
            return False

    def useAbility(self,ability,targlist=[],toggle=False):
        if self.canCast(ability):#if you can cast
            if self.ninja: #spend energy if ninja
                self.energy(-(self.moves[ability]['cost'][self.cur_stats['ability_rank'][ability]]))
            else: #spend mana
                self.mana(-(self.moves[ability]['cost'][self.cur_stats['ability_rank'][ability]]))

            #whether it's being switched or just used for damage
            if 'on' in self.moves[ability]: #decides whether or not the ability is a toggle one
                if toggle:
                    if self.moves[ability]['on'] == True: #toggling off
                        self.moves[ability]['on'] = False
                        self.setCooldowns(ability)
                        print 'Toggling off'
                        return 0
                    elif self.moves[ability]['on'] == False: #toggling on || technically some abilities have a cooldown when you turn them on but i wont sweat that now
                        self.moves[ability]['on'] = True
                        self.cur_stats['status'].update({self.moves[ability]['name']:0})
                        print 'Toggling on'
            else:
                self.setCooldowns(ability)

            abi = self.getAbility(ability) #gets the dictionary of the ability (any combination of damage, cc, steriod, etc)
            for k in abi:
                if k == 'damage' or k == 'scaling_damage':
                    for targ in targlist:
                        d = damageCalc(self,targ,abi)
                        targ.hp(-d)
                        print targ.name.title(),'took %0.2f damage from'%d,abi['name'].title()+'!'
                        # print 'hit her for %s' %d
                elif k == 'stun' or k == 'taunt':
                    for targ in targlist:
                        self.applyStaticAbility(k,targ)
                elif k == 'effect':
                    for targ in targlist:
                        self.applyStaticAbility(abi[k],targ)
                elif k == 'heal':
                    self.hp(abi['heal'])
                    print 'Healed self for',abi['heal']
                elif k == 'stats':
                    for st in k:
                        self.cur_stats[st] += abi[k][st]
            return 1
        else:
            print 'Can\'t cast now'
            return 0
                        
    def autoAttack(self,targ):
        abi = {'damage':self.ad(),'dtype':'physical'}
        d = damageCalc(self,targ,abi)
        #scale for attack speed
        d *= self.cur_stats['as']
        #check for crit
        if self.cur_stats['crit_chance'] > 0:
            cr = random.randint(1,100)
            if cr/100.0 <= self.cur_stats['crit_chance']:
                print 'crit!'
                d *= 2
        #check for damage block
        if self.cur_stats['damage_block'] > 0:
            d -= self.cur_stats['damage_block']
        #deal damage
        targ.hp(-d)
        print targ.name.title(),'was hit for %0.3f!' %d
        #apply abilities
        for oh in self.cur_stats['on_enemy_hit']:
            self.applyStaticAbility(oh,targ)
        for a in targ.cur_stats['on_self_hit']:
            targ.applyStaticAbility(a,self) 

    def applyStaticAbility(self, ability, targ=None): #applying these will assume full level of whomever's hitting them;  I can change it later. also hardcoded
        if ability not in self.ablist:
            try:
                self.customStatic(ability,targ)
            except:
                self.customStatic(ability)
        else:
            ab = copy.deepcopy(self.ablist[ability])
            ab['stacks'] = 0
            for ef in ab['effect']:
                # print 'ef',targ.cur_stats[ef],'other',ablist[ability]['effect'][ef]
                if ef == 'on_enemy_hit':
                    self.cur_stats['on_enemy_hit'].append(ab['effect'][ef])
                elif ef == 'on_self_hit':
                    self.cur_stats['on_self_hit'].append(ab['effect'][ef])
                #check if it's an ability that goes on enemy or self and increment appropreately.
                elif ab['target'] == 'enemy':
                    if ability not in targ.cur_stats['status']:
                        ab['stacks'] = 1
                        targ.cur_stats['status'][ability] = ab
                    if ability in targ.cur_stats['status']:
                        targ.cur_stats['status'][ability]['duration'] = ab['duration']
                    elif targ.cur_stats['status'][ability]['stacks'] < targ.cur_stats['status'][ability]['max_stacks']:
                            targ.cur_stats['status'][ability]['stacks'] += 1
                elif ab['target'] == 'self':
                    if ability not in self.cur_stats['status']:
                        ab['stacks'] = 1
                        self.cur_stats['status'].update({ability:ab})
                    elif self.cur_stats['status'][ability]['stacks'] < self.cur_stats['status'][ability]['max_stacks']:
                            self.cur_stats['status'][ability]['stacks'] += 1
    
    def resetBonuses(self):
        for s in self.cur_stats['bonus_stats']:
            self.cur_stats['bonus_stats'][s] = 0
    def checkStats(self):
        self.resetBonuses()
        for b in self.cur_stats['status']:
            if self.cur_stats['status'][b] == 0:
                pass
            else:
                for e in self.cur_stats['status'][b]['effect']:
                    if e != 'on_enemy_hit' and e != 'on_self_hit':
                        self.cur_stats['bonus_stats'][e] += (self.cur_stats['status'][b]['effect'][e]*self.cur_stats['status'][b]['stacks'])
            # except:
                # pass

    def fullRestore(self):
        self.cur_stats['hp'] = self.cur_stats['bonus_stats']['hp']+self.cur_stats['hp_max']
        if self.ninja:
            self.cur_stats['energy'] = 200
        else:
            self.cur_stats['mana'] = self.cur_stats['bonus_stats']['mana']+self.cur_stats['mana_max']

class Ninja(Champion):
    def __init__(self,cd):
        super(Ninja, self).__init__(cd)
        self.ninja = True
        self.cur_stats.pop('mana')
        self.cur_stats.pop('mana_max')
        self.cur_stats.pop('mana_regen')
        self.cur_stats['energy'] = 200.0
        self.cur_stats['energy_max'] = 200.0

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

    def q(self, dypte = False):
        response = {}
        if (dtype):
            response['dtype'] = self.moves['q']['damage_type']
        else:
            response['damage'] = moveMult(self.moves['q']['damage'],self.cur_stats['ability_rank']['q'],
                self.cur_stats[self.moves['q']['damage_ratio_type']],self.moves['q']['damage_ratio'])
            response['damage2'] = moveMult(self.moves['q']['damage_2'],self.cur_stats['ability_rank']['q'],
                self.cur_stats[self.moves['q']['damage_ratio_type']],self.moves['q']['damage_2_ratio'])
        return response

class Akali(Ninja):
    def __init__(self,cd):
        super(Akali, self).__init__(cd)
        self.cur_stats['essence_of_shadow'] = 3

    def e(self, dtype = False):
        response = {}
        if (dtype):
            return self.moves['e']['damage_type']
        else:
            response['damage'] = moveMult(self.moves['e']['damage'],self.cur_stats['ability_rank']['e'],self.cur_stats[self.moves['e']['damage_ratio_type']],
                self.moves['e']['damage_ratio'],self.cur_stats[self.moves['e']['damage_ratio_type_b']],self.moves['e']['damage_ratio_b'])
            return response

class Alistar(Champion):
    def __init__(self,cd):
        super(Alistar, self).__init__(cd)
        self.ablist = {'stun':{'effect':{},'duration':self.moves['q']['effect']['stun'][self.cur_stats['ability_rank']['q']]}}

    def e(self, dtype = False):
        response = {}
        if (dtype):
            pass
        else:
            response['heal'] = moveMult(self.moves['e']['self_heal_val'],self.cur_stats['ability_rank']['e'],
                self.cur_stats[self.moves['e']['heal_ratio_type']],self.moves['e']['self_heal_ratio'])
            # response['ally_heal'] = moveMult(self.moves['e']['ally_heal_val'],self.cur_stats['ability_rank']['e'],
                # self.cur_stats[self.moves['e']['ally_heal_ratio_type']],self.moves['e']['ally_heal_ratio'])
            return response

class Amumu(Champion):
    def __init__(self,cd):
        super(Amumu, self).__init__(cd)
        self.cur_stats['damage_block'] = self.moves['e']['passive']['damage_block'][self.cur_stats['ability_rank']['e']] #this (and other similar abilities) will need to be reallocated on levelup
        self.cur_stats['on_self_hit'].append('tantrum')
        self.cur_stats['on_enemy_hit'].append('cursed_touch')
        self.ablist = {
        'stun':{'effect':{},'duration':self.moves['q']['effect']['stun'][self.cur_stats['ability_rank']['q']]},
        'cursed_touch':{'effect':{'mr':self.moves['p']['on_enemy_hit']['mr'][2]},'duration':self.moves['p']['on_enemy_hit']['duration'][2],
            'max_stacks':self.moves['p']['on_enemy_hit']['max_stacks'][2],'target':'enemy'}
            }

    def w(self, dtype = False):
        response = {}
        if (dtype):
            return self.moves['w']['damage_type']
        else:
            response['scaling_damage'] = moveMult(self.moves['w']['damage_b'],self.cur_stats['ability_rank']['w'],
                self.cur_stats[self.moves['w']['damage_ratio_type_b']],self.moves['w']['damage_ratio_b'])
            response['base_damage'] = self.moves['w']['damage'][self.cur_stats['ability_rank']['w']]
            return response

    def tick(self, targ = None):
        self.hpRegen()
        self.secondaryRegen()
        if (self.moves['w']['on']):
            self.useAbility('w', [targ])
        self.cooldowns()
        self.statusTimers()
        self.checkStats()

    def customStatic(self, ability):
        if ability == 'tantrum':
            if self.cur_stats['cooldowns']['e'] > 0:
                self.cur_stats['cooldowns']['e'] -=1

class Anivia(Champion):
    def __init__(self,cd):
        super(Anivia, self).__init__(cd)
        self.ablist = {
        'chill':{'effect':{'as':-0.2,'ms':-0.2},'duration':3,'max_stacks':1,'target':'enemy'},
        'stun':{'effect':{},'duration':self.moves['q']['effect']['stun'][self.cur_stats['ability_rank']['q']]}
        }

    def tick(self, targ = None):
        self.hpRegen()
        self.secondaryRegen()
        if (self.moves['r']['on']):
            self.useAbility('r', [targ])
        self.cooldowns()
        self.statusTimers()
        self.checkStats()

class Annie(Champion):
    def __init__(self,cd):
        super(Annie, self).__init__(cd)
        self.ablist = {
        'stun':{'effect':{},'duration':1.75},
        'molten_shield':{'effect':{'armor':self.moves['e']['effect']['armor'][self.cur_stats['ability_rank']['e']],'mr':self.moves['e']['effect']['mr'][self.cur_stats['ability_rank']['e']],'on_self_hit':'burn'},'duration':5,"max_stacks":1,'target':'self'}
        }

    def customStatic(self, ability, targ):
        if ability == 'burn':
            abi = {}
            abi['damage'] = self.moves['e']['effect']['burn'][self.cur_stats['ability_rank']['e']]
            abi['dtype'] = 'magic'
            d = damageCalc(self,targ,abi)
            targ.hp(-d)
            print targ.name.title(),'took',d,'from Molten Shield'

    def e(self, dtype = False):
        response = {}
        if (dtype):
            return self.moves['e']['damage_type']
        else:
            response['damage'] = 0
            response['effect'] = 'molten_shield'
            return response




