"""
Some handy util functions
"""

import simplejson as json
import httplib
from datetime import datetime
from bson import objectid
import pymongo

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

def statmult(c,stat, level):
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

    if (ats): value = (base*(1+(gain*(level-1))))
    else: value = (base+(gain*level))
    return value 

def movemult(base, rank, stat, ratio):
    damage = base[rank]
    damage += (stat*ratio) #stat is relevant stat (ap, ad, health, etc)
    return damage

def getChamp(input):
    c = pymongo.Connection()
    db = c.loldb
    champ = db.champs.find({'name':input},limit=1)
    for i in champ:
        c = prepare(i)
    return c

