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
    if stat == 'hp':
        base = c['hp_base']
        gain = c['hp_ratio']
    elif stat == 'hpreg':
        base = c['hpreg_base']
        gain = c['hpreg_ratio']
    elif stat == 'mana':
        base = c['mana_base']
        gain = c['mana_ratio']
    elif stat == 'manareg':
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
    else: return 0

    if (ats): value = (base*(1.0+(gain*(level-1))))
    else: value = (base+(gain*level))
    return value 

def moveMult(base, rank, stat, ratio, stat2='',ratio2=0):
    damage = base[rank]
    damage += (stat*ratio) #stat is relevant stat (ap, ad, level, health, etc)
    if (stat2):
        damage += (stat2*ratio2)
    return damage

def itemMult(stat, c): #i don't think i need this anymore
    if stat == 'hp':
        targ = c['hp_base']
        gain = c['hp_ratio']
    elif stat == 'hpreg':
        base = c['hpreg_base']
        gain = c['hpreg_ratio']
    elif stat == 'mana':
        base = c['mana_base']
        gain = c['mana_ratio']
    elif stat == 'manareg':
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

def damageMult(damage,defense):
    # print damage
    # print defense
    if (defense>=0):
        multi = 100.0/(100+defense)
        # print multi
    elif (defense<0):
        multi = 2.0-(100/(100+defense))
    return damage*multi

def damageCalc(c1,c2,dtype):
    dt = typeFigurer(c1,dtype)
    # penlist = ['flat_armor_pen','perc_armor_pen','flat_magic_pen','perc_magic_pen']
    if (dt == 'physical'):
        de = c2.armor()
        # pprint(c1.c)
        # print 'armor first: '+str(c2.armor())
        de -= c1.cur_stats['flat_armor_pen']
        # print 'armor second '+str(de)
        d = damageMult(c1.ad(),de)
    elif (dt == 'magical'):
        d = damageMult(c1.q(),c2.mr())
    return d
  
def typeFigurer(c1,dtype):
    if (dtype == 'aa'):
        return 'physical'
    elif (dtype == 'i'):
        return c1.i(True)
    elif (dtype == 'q'):
        return c1.q(True)
    elif (dtype == 'w'):
        return c1.w(True)
    elif (dtype == 'e'):
        return c1.e(True)
    elif (dtype == 'r'):
        return c1.r(True)

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


