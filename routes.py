from functions import api_response, db_error, set_vars, Vars, statmult, prepare, MongoEncoder, movemult
import pymongo
from base import route, Champion
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
        champ = Champion()
        champ.name = 'ahri'
        champ.title = 'the Nine-Tailed Fox'
        st = {}
        st['hp_base'] = 380
        st['hp_ratio'] = 80
        st['hpreg_base'] = 5.5
        st['hpreg_ratio'] = 0.6
        st['mana_base'] = 230
        st['mana_ratio'] = 50
        st['manareg_base'] = 6.25
        st['manareg_ratio'] = .6
        st['arange'] = 550
        st['ad_base'] = 50
        st['ad_ratio'] = 3
        st['as_base'] = 0.668
        st['as_ratio'] = 0.02
        st['armor_base'] = 11
        st['armor_ratio'] = 3.51
        st['mr_base'] = 30
        st['move'] = 305
        champ.stats = st
        

        i = {}
        i['name'] = 'Essence Theft'
        i['desc'] = "Ahri gains a charge of Essence Theft whenever one of her spells hits an enemy. This caps at 3 charges per spell cast. Upon reaching 9 charges, Ahri's next spell will have 35% bonus spell vamp."
        champ.moves['i'] = i
        
        q = {}
        q['name'] = 'Orb of Deception'
        q['desc'] = "Active: Ahri sends out an orb in a line in front of her and then pulls it back, dealing magic damage on the way out and true damage on the way back."
        q['range'] = 880
        q['cd'] = 6
        q['cost_val'] = [0,70,75,80,85,90]
        q['cost_type'] = 'mana'
        q['damage'] = [0,40,65,90,115,140]
        q['damage_type'] = 'magic'
        q['damage_ratio'] = 0.33
        q['damage_ratio_type'] = 'ap'
        q['damage_b'] = [0,40,65,90,115,140]
        q['damage_b_type'] = 'true'
        q['damage_b_ratio'] = 0.33
        q['damage_b_ratio_type'] = 'ap'
        champ.moves['q'] = q

        db.champs.update({'name':champ.name},champ.to_python(),True)
        # self.write(champ.to_python())
        self.write('stored %s, %s!' %(champ.name.title(), champ.title))

@route('/champions/show/(\w+)')
class ChampPrint(tornado.web.RequestHandler):
    # @engine
    # @asynchronous
    def get(self,input):
        c = pymongo.Connection()
        db = c.loldb
        # champ = db.champs.find({'name':input},limit=1)
        # champ = yield Task(db.champs.find,{'name':input},limit=1)
        # for i in champ:
            # c = prepare(i)
        # # this is for nice output
        #     self.write('Name: <b>%s</b>, %s<br>' %(c['name'].title(),c['title']))
        #     for s in c['stats']:
        #         self.write('%s: %s <br>' %(s.replace('_',' ').title(), c['stats'][s]))
        #     self.write("<br><br>")
        #     self.write("%s's Q does %s %s damage at lvl 18 with 500 %s" %(c['name'].title(), movemult(c['moves']['q']['damage'],5,500,c['moves']['q']['damage_ratio']),c['moves']['q']['damage_type'],c['moves']['q']['damage_ratio_type']))
        #this is for printing the whole response
            # self.write(c)
        json_data=open('champs/ahri.json')
        data = json.load(json_data)
        pprint(data)
        json_data.close()
        # pprint(data)
