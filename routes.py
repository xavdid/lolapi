from functions import api_response, db_error, set_vars, Vars, statMult, prepare, MongoEncoder, moveMult, getChamp, attach
import pymongo
from base import route, Champion, Ahri, ItemBase, ChampBase
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
        # champ = Champion()
        asdf = ItemBase()
        asdf.items = {"ruby":{"name":"Ruby Crystal","effect":{"hp":180},"cost":475,"tag":"ruby"},
            "amp_tome":{"name":"Amplification Tome","effect":{"ap":20},"cost":435,"tag":"amp_tome"}}
        asdf.name = 'items'
        # champ.name = 'ahri'
        # champ.title = 'the Nine-Tailed Fox'
        # st = {}
        # st['hp_base'] = 380
        # st['hp_ratio'] = 80
        # st['hpreg_base'] = 5.5
        # st['hpreg_ratio'] = 0.6
        # st['mana_base'] = 230
        # st['mana_ratio'] = 50
        # st['manareg_base'] = 6.25
        # st['manareg_ratio'] = .6
        # st['arange'] = 550
        # st['ad_base'] = 50
        # st['ad_ratio'] = 3
        # st['as_base'] = 0.668
        # st['as_ratio'] = 0.02
        # st['armor_base'] = 11
        # st['armor_ratio'] = 3.50
        # st['mr_base'] = 30
        # st['move'] = 305
        # champ.stats = st
        
        # i = {}
        # i['name'] = 'Essence Theft'
        # i['desc'] = "Ahri gains a charge of Essence Theft whenever one of her spells hits an enemy. This caps at 3 charges per spell cast. Upon reaching 9 charges, Ahri's next spell will have 35% bonus spell vamp."
        # champ.moves['i'] = i
        
        # q = {}
        # q['name'] = 'Orb of Deception'
        # q['desc'] = "Active: Ahri sends out an orb in a line in front of her and then pulls it back, dealing magic damage on the way out and true damage on the way back."
        # q['range'] = 880
        # q['cd'] = 6
        # q['cost_val'] = [0,70,75,80,85,90]
        # q['cost_type'] = 'mana'
        # q['damage'] = [0,40,65,90,115,140]
        # q['damage_type'] = 'magic'
        # q['damage_ratio'] = 0.33
        # q['damage_ratio_type'] = 'ap'
        # q['damage_b'] = [0,40,65,90,115,140]
        # q['damage_b_type'] = 'true'
        # q['damage_b_ratio'] = 0.33
        # q['damage_b_ratio_type'] = 'ap'
        # champ.moves['q'] = q

        # w ={}
        # w['name'] = 'Fox-Fire'
        # w['desc'] = "Active: Ahri will blow a kiss that travels in a line in front of her. It will damage and charm the first enemy it encounters, forcing them to walk harmlessly towards her, while being slowed by 50% for the duration."
        # w['range'] = 800
        # w['cd'] = [0,9,8,7,6,5]
        # w['cost_val'] = 60
        # w['cost_type'] = 'mana'
        # w['damage'] = [0,40,65,90,115,140]
        # w['damage_type'] = 'magic'
        # w['damage_ratio'] = 0.4
        # w['damage_ratio_type'] = 'ap'
        # w['damage_max'] = [0,80,130,180,230,280]
        # w['damage_max_ratio'] = 0.4
        # w['damage_max_ratio_type'] = 'ap'
        # champ.moves['w'] = w

        # e = {}
        # e['name'] = 'Charm'
        # e['desc'] = "Active: Ahri will blow a kiss that travels in a line in front of her. It will damage and charm the first enemy it encounters, forcing them to walk harmlessly towards her, while being slowed by 50% for the duration."
        # e['range'] = 975
        # e['cd'] = 12
        # e['cost_val'] = [0,40,65,80,95,110]
        # e['cost_type'] = 'mana'
        # e['damage'] = [0,60,90,120,150,180]
        # e['damage_type'] = 'magic'
        # e['damage_ratio'] = 0.35
        # e['damage_ratio_type'] = 'ap'
        # e['duration'] = [0,1,1.25,1.5,1.75,2]
        # champ.moves['e'] = e

        # r ={}
        # r['name'] = 'Spirit Rush'
        # r['desc'] = "Active: Ahri dashes towards the cursor and fires essence bolts, dealing damage to up to 3 nearby enemies, prioritizing champions. In the next 10 seconds, Spirit Rush can be cast two additional times before going on cooldown. Each enemy can only be hit once per dash."
        # r['range'] = 550
        # r['cd'] = 100
        # r['cost_val'] = [0,40,65,80,95,110]
        # r['cost_type'] = 'mana'
        # r['damage'] = [0,85,125,165]
        # r['damage_type'] = 'magic'
        # r['damage_ratio'] = 0.35
        # r['damage_ratio_type'] = 'ap'
        # r['dash_range'] = 450
        # champ.moves['r'] = r
        # # pprint(champ.to_python())
        pprint(asdf.items)
        db.champs.update({'name':"items"},asdf.to_python(),True)
        # self.db.champs.update({'name':champ.name},champ.to_python(),True)
        # # self.write(champ.to_python())
        # self.write('stored %s, %s!' %(champ.name.title(), champ.title))

@route('/champions/show/(\w+)')
class ChampPrint(tornado.web.RequestHandler):
    # @engine
    # @asynchronous
    def get(self,input):
        c = getChamp(input)
        a = Ahri(c)
    # this is for nice output
        self.write('Name: <b>%s</b>, %s<br>' %(a.name.title(),a.title))
        for s in a.cur_stats:
            self.write('%s: %s <br>' %(s.replace('_',' ').title(), a.cur_stats[s]))
        self.write("<br><br>")
        self.write("%s's Q does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.q(),a.c['moves']['q']['damage_type'],a.cur_stats['ap'],a.c['moves']['q']['damage_ratio_type'].upper()))
        self.write("<br><br>")
        a.items.append('ruby')
        a.items.append('amp_tome')
        a.doItems()
        self.write("%s's Q does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.q(),a.c['moves']['q']['damage_type'],a.cur_stats['ap'],a.c['moves']['q']['damage_ratio_type'].upper()))

    #this is for printing the whole response
        # self.write(c)


@route('/patch')
class PatchHandler(tornado.web.RequestHandler):
    def get(self):
        co = pymongo.Connection()
        db = co.loldb
        # c = {}
        # champ = db.champs.find({'name':'items'},limit=1)
        # for i in champ:
            # c = prepare(i)
        # self.write(c)
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
