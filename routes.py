from functions import api_response, db_error, set_vars, Vars, statMult, prepare, MongoEncoder, moveMult, getChamp, attach
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
        # champ.name = 'akali'
        # champ.title = 'the Fist of Shadow'
        # st = {}
        # st['hp_base'] = 445
        # st['hp_ratio'] = 85
        # st['hpreg_base'] = 7.25
        # st['hpreg_ratio'] = 0.65
        # st['energy'] = 200
        # # st['mana_base'] = 230
        # # st['mana_ratio'] = 50
        # # st['manareg_base'] = 6.25
        # # st['manareg_ratio'] = .6
        # st['arange'] = 125
        # st['ad_base'] = 53
        # st['ad_ratio'] = 3.2
        # st['as_base'] = 0.694
        # st['as_ratio'] = 3.1
        # st['armor_base'] = 16.5
        # st['armor_ratio'] = 3.5
        # st['mr_base'] = 30
        # st['mr_ratio'] = 1.25
        # st['move'] = 325
        # champ.stats = st
        
        # i = {}
        # i['name'] = 'Twin Disciplines'
        # i['desc'] = 'her ablities hurt and she heals'
        # i['f_value'] = 7.916
        # i['m_value'] = 7.916
        # champ.moves['i'] = i
        
        # q = {}
        # q['name'] = 'Mark of the Assassin'
        # q['desc'] = "Active: Akali throws her kama at a target enemy, dealing magic damage and marking the target for 6 seconds. Akali's melee attacks or Crescent Slashes against a marked target will consume the mark dealing the same magic damage again and restoring energy."
        # q['range'] = 600
        # q['cd'] = 6
        # q['cost_val'] = 60
        # q['cost_type'] = 'energy'
        # q['damage'] = [0,5,70,95,120,145]
        # q['damage_type'] = 'magic'
        # q['damage_ratio'] = 0.4
        # q['damage_ratio_type'] = 'ap'
        # q['energy_restored'] = [0,15,20,25,30,35]
        # # q['damage_b'] = [0,40,65,90,115,140]
        # # q['damage_b_type'] = 'true'
        # # q['damage_b_ratio'] = 0.33
        # # q['damage_b_ratio_type'] = 'ap'
        # champ.moves['q'] = q

        # w ={}
        # w['name'] = ' Twilight Shroud '
        # w['desc'] = "Active: Akali throws down a circular cover of smoke that lasts for 8 seconds. While inside the area, Akali gains armor and magic resistance and becomes stealthed. Attacking or using abilities reveals her for 0.5 seconds. Enemies inside the smoke have their movement speed reduced."
        # w['range'] = 700
        # w['diameter'] = 300
        # w['cd'] = 20
        # w['cost_val'] = [0,80,75,70,65,60]
        # w['cost_type'] = 'energy'
        # w['defense_boost'] = [0,10,20,30,40,50]
        # w['ms_reduction'] = [0,14,18,22,26,30]
        # w['ms_reduction_type'] = 'percent'

        # # w['damage'] = [0,40,65,90,115,140]
        # # w['damage_type'] = 'magic'
        # # w['damage_ratio'] = 0.4
        # # w['damage_ratio_type'] = 'ap'
        # # w['damage_max'] = [0,80,130,180,230,280]
        # # w['damage_max_ratio'] = 0.4
        # # w['damage_max_ratio_type'] = 'ap'
        # champ.moves['w'] = w

        # e = {}
        # e['name'] = 'Crescent Slash'
        # e['desc'] = "Active: Akali flourishes her kamas, hitting nearby units for physical damage."
        # e['range'] = 325
        # e['cd'] = [0,7,6,5,4,3]
        # e['cost_val'] = [0,60,55,50,45,40]
        # e['cost_type'] = 'energy'
        # e['damage'] = [0,30,55,80,105,130]
        # e['damage_type'] = 'physical'
        # e['damage_ratio'] = 0.6
        # e['damage_ratio_type'] = 'ad'
        # e['damage_ratio_b'] = 0.3
        # e['damage_ratio_type_b'] = 'ap'
        # # e['duration'] = [0,1,1.25,1.5,1.75,2]
        # champ.moves['e'] = e

        # r ={}
        # r['name'] = 'Shadow Dance'
        # r['desc'] = "Active: Akali moves through the shadows to quickly appear next to her target and deal magic damage to it. Akali gains an Essence of Shadow periodically, affected by cooldown reduction, up to a maximum of 3. Additionally, Akali gains an Essence of Shadow for each kill or assist."
        # r['range'] = 800
        # r['cd'] = [0,2,1.5,1]
        # r['cost_val'] = 1
        # r['cost_type'] = 'essence of shadow'
        # r['essence_regen_rate'] = [0,25,20,15]
        # r['damage'] = [0,100,175,250]
        # r['damage_type'] = 'magic'
        # r['damage_ratio'] = 0.5
        # r['damage_ratio_type'] = 'ap'
        # # r['dash_range'] = 450
        # champ.moves['r'] = r
        # # pprint(champ.to_python())
        # # pprint(asdf.items)
        # # db.champs.update({'name':"items"},asdf.to_python(),True)
        # db.champs.update({'name':champ.name},champ.to_python(),True)
        # # # self.write(champ.to_python())
        # self.write('stored %s, %s!' %(champ.name.title(), champ.title))

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
        self.write("<br><br>")
        # self.write("%s's Q does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.q(),a.c['moves']['q']['damage_type'],a.cur_stats['ap'],a.c['moves']['q']['damage_ratio_type'].upper()))
        # self.write("<br><br>")
        # a.items.append('ruby')
        # a.items.append('amp_tome')
        # a.doItems()
        # self.write("%s's Q does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.q(),a.c['moves']['q']['damage_type'],a.cur_stats['ap'],a.c['moves']['q']['damage_ratio_type'].upper()))

    #this is for printing the whole response
        # self.write(c)


@route('/patch')
class PatchHandler(tornado.web.RequestHandler):
    def get(self):
        co = pymongo.Connection()
        db = co.loldb
        champlist = ['items','ahri','akali']
        js = open('champs/items.json')
        js2 = open('champs/ahri.json')
        c = json.load(js)
        c2 = json.load(js2)
        i = ItemBase()
        ch = ChampBase()
        i.items = c
        i.name = 'items'
        attach(ch,c2)
        db.champs.update({'name':"items"},i.to_python(),True)
        db.champs.update({'name':"ahri"},ch.to_python(),True)
        # pprint(c)
        js.close()
        js2.close()
