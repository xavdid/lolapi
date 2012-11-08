from functions import api_response, db_error, set_vars, Vars, mult, prepare, MongoEncoder
import pymongo
from base import route, BaseAPIHandler, Champion
import simplejson as json

@route('/champions/add')
class ChampAdd(BaseAPIHandler):
    def get(self):
    	c = pymongo.Connection()
        db = c.loldb
        champ = Champion()
        champ.name = 'ahri'
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
        st['armor_base'] = 11
        st['armor_ratio'] = 3.5
        st['mr_base'] = 30
        st['move'] = 305
        champ.stats = st
        db.champs.update({'name':champ.name},champ.to_python(),True)
        self.write('stored %s!' %champ.name)

@route('/champions/show/(\w+)')
class ChampPrint(BaseAPIHandler):
    def get(self,input):
        c = pymongo.Connection()
        db = c.loldb
        champ = db.champs.find({'name':input},limit=1)
        for i in champ:
            c = prepare(i)
            self.write('Name: <b>%s</b><br>' %c['name'])
            for s in c['stats']:
                self.write('%s: %s <br>' %(s, c['stats'][s]))



            # self.write(prepare(i))

        # dchamp = json.loads(json.dumps(champ))
        # self.write(dchamp)
        # if (dchamp):
            # self.write('found her!')
        # else:
            # self.write('not found')
        # for k in champ:
        	# self.write(k)
