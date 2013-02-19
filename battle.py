import sys, traceback
from functions import *
import pymongo
from base import *
import simplejson as json
import tornado.web

def checkState(c1,c2):
    winner = False
    if c1.hp() <= 0:
        print 'Game over, the computer has defeated you!'
        sys.exit(0)
    elif c2.hp() <= 0:
        print 'Well done, you\'ve bested the computer as %s'%c2.name()
        sys.exit(0)
    else:
        pass

def act(c1,c2):
    a = raw_input('What would you like to do (Type h for help)? ').lower()
    if a == 'h':
        help()
        act(c1,c2)
    elif a == 'q' or a == 'w' or a == 'e' or a == 'r':
        if 'on' in c1.moves[a]:
            c1.useAbility(a,c[c2],toggle=True)
        else:
            c1.useAbility(a,[c2])
    elif a == 'aa':
        c1.autoAttack(c2)
    elif a == 'p':
        shop()
    elif a == 'exit':
        sys.exit(0)

def help():
    print 'Type (Q|W|E|R) to use that ability.\nType A to auto-attack\nType S for stats (hp, mana, cooldowns)\nType C for current status (all stats)\nType P to shop\nType exit to quit\nEverything is type-insensitive'

def shop(c1):
    conn = pymongo.Connection('mongodb://d:b@ds031877.mongolab.com:31877/lolapi')
    db = conn.lolapi
    champ = db.champs.find({'name':'items'},limit=1)
    for i in champ:
        c = prepare(i)
    k = c['items']
    s = raw_input('type an item\'s name to buy it, or "list" to see all of the items names ')
    if s == 'list':
        shoplist(k)
        s = raw_input('type an item\'s name to buy it, or "list" to see all of the items names ')
    if s in k:
        c1.items.append('s')
        c1.doItems()

def shoplist(i):
    for item in i:
        print item,

def init(p):
    conn = pymongo.Connection('mongodb://d:b@ds031877.mongolab.com:31877/lolapi')
    db = conn.lolapi
    if p == 1:
        while True:
            inp = raw_input('Who do you want to play as? ')
            if inp == 'akali' or inp == 'ahri' or inp == 'alistar' or inp == 'amumu' or inp == 'anivia' or inp == 'annie' or inp == 'ashe':
                break
    else:
        inp = 'akali'

    champ = db.champs.find({'name':inp},limit=1)
    for i in champ:
        c = prepare(i)
    if (inp == 'akali'):
        a = Akali(c)
    elif (inp == 'ahri'):
        a = Ahri(c)
    elif (inp == 'alistar'):
        a = Alistar(c)
    elif (inp == 'amumu'):
        a = Amumu(c)
    elif (inp == 'anivia'):
        a = Anivia(c)
    elif (inp == 'annie'):
        a = Annie(c)
    elif (inp == 'ashe'):
        a = Ashe(c)

    return a
        


    


c1 = init(1)
c2 = init(2)
while True:
    act(c1,c2)
