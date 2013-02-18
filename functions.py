import simplejson as json
import httplib
from datetime import datetime
from bson import objectid
import pymongo
from pprint import pprint
import urllib2
import sys
from secrets import username, password

def api_response(status,response,handler=None,code=200,errors=[]):
    if handler: handler.set_status(code)
    return dict(status=status,response=response,errors=errors)

def db_error(handler):
    return api_response('error','database error',handler,500)

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
    elif stat == 'ms_base':
        base = c['ms_base']
        gain = 0
    # elif (stat == 'cooldowns' or stat == 'ability_rank'):
        # return {'i':0,'q':0,'w':0,'e':0,'r':0}
    # elif (stat == 'status' or stat == 'on_hit'): #these are indivitually defined since they're dicts and shouldn't be set to 0
        # return {}
    elif (isinstance(stat,dict) or isinstance(stat,list)):
        pass
    else: return False #honesly, this is bad because i end up with things being 0 that shoudln't. namely, dictionaries. 

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
    if ('scaling' not in ability):
        damage_total = ability['damage']
    if (ability['dtype'] == 'physical'):
        de = c2.armor()
        de -= c1.cur_stats['flat_armor_pen']
    elif (ability['dtype'] == 'magic'):
        # magic pen, blah blah
        de = c2.mr()
    if 'scaling' in ability:
        damage_total = ability['base_damage']+(ability['scaling_damage']*c2.cur_stats[ability['scaling']])
    # elif (dt == 'true'):
        # d = damageMult(c1.q(),c2.mr())
    da = damageMult(damage_total,de)    
    return da

def getChamp(input):
    conn = pymongo.Connection('mongodb://%s:%s@ds031877.mongolab.com:31877/lolapi'%(username,password))
#the line below is the read-only, non-authenticated version.
    # conn = pymongo.Connection('mongodb://ds031877.mongolab.com:31877/lolapi')
    db = conn.lolapi
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

#these are for scraping
def namer(s):
    if s == 'Damage':
        return 'ad'
    elif s == 'Health':
        return 'hp'
    elif s == 'Mana':
        return 'mana'
    elif s == 'Move Speed':
        return 'ms'
    elif s == 'Armor':
        return 'armor'
    elif s == 'Spell Block':
        return 'mr'
    elif s == 'Health Regen':
        return 'hpreg'
    elif s == 'Mana Regen':
        return 'manareg'

def pretty(s,ult=False):
    s = s.strip('{}')
    s = s.replace('ap','0')
    s = s.replace('|',',')
    s = s.split(',')
    s = [float(x) for x in s]
    if len(s) == 1:
        s.append(s[0])
        s[0] = 0
        if ult:
            for i in range(2,4):
                s.append(s[1])
        else:
            for i in range(2,6):
                s.append(s[1])
    return s

def urlGrab(url):
    resp = urllib2.urlopen(url)
    s = resp.read()
    return s

