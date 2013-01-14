"""
Some handy util functions
"""

import simplejson as json
import httplib
from datetime import datetime
from bson import objectid
import pymongo
from pprint import pprint

def api_response(status,response,handler=None,code=200,errors=[]):
    if handler: handler.set_status(code)
    return dict(status=status,response=response,errors=errors)

def db_error(handler):
    return api_response('error','database error',handler,500)

def set_vars(handler,**kwargs):
    """
    Sets the API request parameters and their desired default values
    handler - the RequestHandler object for the request
    kwargs - key/value pairs of the request parameter and its default value
    """
    vars = Vars()
    for arg in kwargs:
        setattr(vars,arg,handler.get_argument(arg,default=kwargs[arg]))
    return vars

class Vars(object):
    """Empty object allowing for dot-declaration"""
    pass

class MongoEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, objectid.ObjectId):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)

def prepare(response):
    return json.loads(json.dumps(response, cls = MongoEncoder))

def statMult(c, stat, level):
    ats = False
    if (stat == 'hp' or stat == 'hp_max'):
        base = c['hp_base']
        gain = c['hp_ratio']
    elif stat == 'hp_regen':
        base = c['hpreg_base']
        gain = c['hpreg_ratio']
    elif (stat == 'mana' or stat == 'mana_max'):
        base = c['mana_base']
        gain = c['mana_ratio']
    elif stat == 'mana_regen':
        base = c['manareg_base']
        gain = c['manareg_ratio']
    elif stat == 'ad':
        base = c['ad_base']
        gain = c['ad_ratio']
    elif stat == 'as':
        base = c['as_base']
        gain = c['as_ratio']
        ats = True
    elif stat == 'armor':
        base = c['armor_base']
        gain = c['armor_ratio']
    elif stat == 'mr':
        base = c['mr_base']
        gain = c['mr_ratio']
    elif stat == 'energy':
        return 200
    elif stat == 'ms':
        base = c['ms']
        gain = 0
    # elif (stat == 'cooldowns' or stat == 'ability_rank'):
        # return {'i':0,'q':0,'w':0,'e':0,'r':0}
    # elif (stat == 'status' or stat == 'on_hit'): #these are indivitually defined since they're dicts and shouldn't be set to 0
        # return {}
    elif (isinstance(stat,dict)):
        pass
    else: return 0 #honesly, this is bad because i end up with things being 0 that shoudln't. namely, dictionaries. 

    if (ats): value = (base*(1.0+(gain*(level-1))))
    else: value = (base+(gain*level))
    return value 

def moveMult(base, rank, stat, ratio, stat2='',ratio2=0):
    damage = base[rank]
    damage += (stat*ratio) #stat is relevant stat (ap, ad, level, health, etc)
    if (stat2):
        damage += (stat2*ratio2)
    return damage

def damageMult(damage,defense):
    # print damage
    # print defense
    if (defense>=0):
        multi = 100.0/(100+defense)
        # print multi
    elif (defense<0):
        multi = 2.0-(100/(100+defense))
    return damage*multi

def damageCalc(c1,c2,ability):
    # penlist = ['flat_armor_pen','perc_armor_pen','flat_magic_pen','perc_magic_pen']
    if (ability['dtype'] == 'physical'):
        de = c2.armor()
        de -= c1.cur_stats['flat_armor_pen']
    elif (ability['dtype'] == 'magic'):
        # magic pen, blah blah
        de = c2.mr()
    da = damageMult(ability['damage'],de)
    # elif (dt == 'true'):
        # d = damageMult(c1.q(),c2.mr())
    return da

def getChamp(input):
    c = pymongo.Connection()
    db = c.loldb
    champ = db.champs.find({'name':input},limit=1)
    for i in champ:
        c = prepare(i)
    if input == 'items':
        return c['items']
    else:
        return c

def attach(ch,c):
    ch.name = c['name']
    ch.title = c['title']
    ch.stats = c['stats']
    ch.moves = c['moves']

def breaks(i):
    s = ''
    for j in range(i):
        s+="<br>"
    return s


