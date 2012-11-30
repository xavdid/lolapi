from functions import *
import pymongo
# from base import route, Champion, Ahri, ItemBase, ChampBase, Akali
from base import *
import simplejson as json
import asyncmongo
import tornado.web
from tornado.web import asynchronous
from tornado.gen import engine, Task
from pprint import pprint

@route('/champions/add')
class ChampAdd(tornado.web.RequestHandler):
    def get(self):
    	c = pymongo.Connection()
        db = c.loldb
        champ = ChampBase()
        # asdf = ItemBase()
        # asdf.items = {"ruby":{"name":"Ruby Crystal","effect":{"hp":180},"cost":475,"tag":"ruby"},
            # "amp_tome":{"name":"Amplification Tome","effect":{"ap":20},"cost":435,"tag":"amp_tome"}}
        # asdf.name = 'items'
        champ.name = 'alistar'
        champ.title = 'the Minotaur'
        st = {}
        st['hp_base'] = 442.0
        st['hp_ratio'] = 102.0
        st['hpreg_base'] = 7.25
        st['hpreg_ratio'] = 0.85
        # st['energy'] = 200
        st['mana_base'] = 215.0
        st['mana_ratio'] = 38.0
        st['manareg_base'] = 6.45
        st['manareg_ratio'] = .45
        st['arange'] = 125.0
        st['ad_base'] = 55.03
        st['ad_ratio'] = 3.62
        st['as_base'] = 0.625
        st['as_ratio'] = 2.13
        st['armor_base'] = 14.5
        st['armor_ratio'] = 3.5
        st['mr_base'] = 30.0
        st['mr_ratio'] = 1.25
        st['move'] = 300.0
        champ.stats = st
        
        i = {}
        i['name'] = 'Trample'
        i['desc'] = 'Each time Alistar casts a spell, he gains the ability to move through units and will deal damage to nearby enemy units and structures for about 3 seconds. Trample deals double damage to minions and monsters. '
        i['damage'] = 6
        i['damage_ratio'] = 1
        i['damage ratio type'] = 'level'
        i['damage_ratio_b'] = .1
        i['damage_ratio_type_b'] = 'ap'
        champ.moves['i'] = i
        
        q = {}
        q['name'] = 'Pulverize'
        q['desc'] = "Active: Alistar smashes the ground where he is standing, dealing damage to all surrounding enemies and knocking them up for 1 second, additionally stunning them upon landing for 0.5 seconds."
        q['range'] = 182.5
        q['cd'] = [0,17,16,15,14,13]
        q['cost_val'] = [0,70,80,90,100,110]
        q['cost_type'] = 'mana'
        q['damage'] = [0,60,105,150,195,240]
        q['damage_type'] = 'magic'
        q['damage_ratio'] = 0.5
        q['damage_ratio_type'] = 'ap'
        # q['energy_restored'] = [0,15,20,25,30,35]
        # q['damage_b'] = [0,40,65,90,115,140]
        # q['damage_b_type'] = 'true'
        # q['damage_b_ratio'] = 0.33
        # q['damage_b_ratio_type'] = 'ap'
        champ.moves['q'] = q

        w ={}
        w['name'] = 'Headbutt'
        w['desc'] = "Active: Alistar dashes to an enemy's position and rams them, dealing damage and knocking them back a set distance over 1 second, also briefly immobilizing them."
        w['range'] = 600
        w['kockback'] = 650
        w['cd'] = [0,17,16,15,14,13]
        w['cost_val'] = [0,80,75,70,65,60]
        w['cost_type'] = 'mana'
        # w['defense_boost'] = [0,10,20,30,40,50]
        # w['ms_reduction'] = [0,14,18,22,26,30]
        # w['ms_reduction_type'] = 'percent'

        w['damage'] = [0,55,110,165,220,275]
        w['damage_type'] = 'magic'
        w['damage_ratio'] = 0.7
        w['damage_ratio_type'] = 'ap'
        # w['damage_max'] = [0,80,130,180,230,280]
        # w['damage_max_ratio'] = 0.4
        # w['damage_max_ratio_type'] = 'ap'
        champ.moves['w'] = w

        e = {}
        e['name'] = 'Triumphant Roar'
        e['desc'] = "Active: Alistar instantly restores health to himself, healing nearby friendly units for half of that amount. The cooldown of this ability is reduced by 2 seconds each time a nearby enemy unit dies."
        e['range'] = 287.5
        e['cd'] = 12
        e['cost_val'] = [0,40,50,60,70,80]
        e['cost_type'] = 'mana'
        # e['damage'] = [0,30,55,80,105,130]
        e['self_heal_val'] = [0,60,90,120,150,180]
        e['self_heal_ratio'] = .2
        e['ally_heal_val'] = [0,30,45,60,75,90]
        e['ally_heal_ratio'] = .1

        # e['damage_type'] = 'physical'
        # e['damage_ratio'] = 0.6
        e['heal_ratio_type'] = 'ap'
        # e['damage_ratio_b'] = 0.3
        # e['damage_ratio_type_b'] = 'ap'
        # e['duration'] = [0,1,1.25,1.5,1.75,2]
        champ.moves['e'] = e

        r ={}
        r['name'] = 'Unbreakable Will'
        r['desc'] = "Active: Alistar instantly gains bonus attack damage and takes reduced physical and magic damage for 7 seconds. If he is under crowd control effects at the time of casting, they are also removed."
        # r['range'] = 800
        r['cd'] = [0,120.0,100.0,80.0]
        r['cost_val'] = 100
        r['cost_type'] = 'mana'
        r['damage_reduction'] = [0,50,60,79]
        r['damage_reduction_type' ] = 'percent'
        # r['damage_type'] = 'magic'
        # r['damage_ratio'] = 0.5
        # r['damage_ratio_type'] = 'ap'
        r['bonus_ad'] = [0,60,75,90]
        champ.moves['r'] = r
        # pprint(champ.to_python())
        # pprint(asdf.items)
        # db.champs.update({'name':"items"},asdf.to_python(),True)
        db.champs.update({'name':champ.name},champ.to_python(),True)
        # # self.write(champ.to_python())
        self.write('stored %s, %s!' %(champ.name.title(), champ.title))

@route('/champions/show/(\w+)')
class ChampPrint(tornado.web.RequestHandler):
    # @engine
    # @asynchronous
    def get(self,input):
        c = getChamp(input)
        if (input == 'akali'):
            a = Akali(c)
        elif (input == 'ahri'):
            a = Ahri(c)
        else:
            self.write('Champion not found')
            assert(1)
    # this is for nice output
        self.write('Name: <b>%s</b>, %s<br>' %(a.name.title(),a.title))
        for s in a.cur_stats:
            self.write('%s: %s <br>' %(s.replace('_',' ').title(), a.cur_stats[s]))
        self.write("<br>Items:")
        self.write(breaks(2))
    #i could have one of these rows in the base class so we could see stuff like this?
        self.write("%s's Q does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.q(),a.c['moves']['q']['damage_type'],a.cur_stats['ap'],a.c['moves']['q']['damage_ratio_type'].upper()))
        self.write("<br><br>")
        self.write("%s's E does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.e(),a.c['moves']['e']['damage_type'],a.cur_stats['ap'],a.c['moves']['e']['damage_ratio_type'].upper()))
        self.write(breaks(2))
        a.items.append('ruby')
        a.items.append('amp_tome')
        a.items.append('dblade')
        a.doItems()
        self.write("<br>Items:<br>")
        self.write(' '.join(a.items)+"<br>")
        self.write(breaks(2))
        for s in a.cur_stats:
            self.write('%s: %s <br>' %(s.replace('_',' ').title(), a.cur_stats[s]))
        self.write("%s's Q does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.q(),a.c['moves']['q']['damage_type'],a.cur_stats[a.c['moves']['q']['damage_ratio_type']],a.c['moves']['q']['damage_ratio_type'].upper()))

        self.write(breaks(2))
        self.write("%s's E does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.e(),a.c['moves']['e']['damage_type'],a.cur_stats[a.c['moves']['e']['damage_ratio_type']],a.c['moves']['e']['damage_ratio_type'].upper()))
        self.write("<br> it would do %.3f against someone with 115 armor"%(damageMult(a.e(),115)))

    #this is for printing the whole response
        # self.write(c)


@route('/patch')
class PatchHandler(tornado.web.RequestHandler):
    def get(self):
        co = pymongo.Connection()
        db = co.loldb
        champlist = ['items','ahri']#,'akali']
        for n in champlist: 
            js = open('champs/%s.json' %n)
            c = json.load(js)
            if (n=='items'):
                ch = ItemBase()
                ch.items = c
                ch.name = 'items'
            else:
                ch = ChampBase()
                attach(ch,c)

            db.champs.update({'name':n},ch.to_python(),True)
            # pprint(ch.to_python())
            js.close()
        self.write('patched to v 1.0.3.1!')
        # js = open('champs/items.json')
        # js2 = open('champs/ahri.json')
        # c = json.load(js)
        # c2 = json.load(js2)
        # i = ItemBase()
        # ch = ChampBase()
        # i.items = c
        # i.name = 'items'
        # attach(ch,c2)
        # db.champs.update({'name':"items"},i.to_python(),True)
        # db.champs.update({'name':"ahri"},ch.to_python(),True)
        # # pprint(c)
        # js.close()
        # js2.close()
