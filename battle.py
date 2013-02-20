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
        print 'Well done, you\'ve bested the computer(%s) with %s!'%(c2.name.title(),c1.name.title())
        sys.exit(0)
    else:
        pass

def act(c1,c2):
    a = raw_input('What would you like to do (Type h for help)? -->').lower()
    if a == 'h':
        help()
        return 0
    #using an ability
    elif a == 'q' or a == 'w' or a == 'e' or a == 'r':
        if 'on' in c1.moves[a]:
            g = c1.useAbility(a,[c2],toggle=True)
        else:
            g = c1.useAbility(a,[c2])
        if g:
            return 1

    #autoattack
    elif a == 'a':
        c1.autoAttack(c2)
        return 1
    #shop
    elif a == 'p':
        shop(c1)
        return 0
    elif a == 's':
        c1.showStats()
        return 0
    elif a == 'i':
        c1.showItems()
        return 0
    elif a == 'exit' or a == 'quit':
        sys.exit(0)
    else:
        print 'Incorrect input'
        return 0

def help():
    print 'Type (Q|W|E|R) to use that ability.\nType A to auto-attack\nType S for stats (hp, mana, ad, ap, as, buffs, and cooldowns)\nType C for current status (all stats)\nType I to show inventory\nType P to shop\nType exit to quit\nEverything is type-insensitive'

def shop(c1):
    c = getChamp('items')
    k = c['items']
    #check if items are full
    while True:
        a = buy(c1,k)
        if a == 1:
            break

def buy(c1, k):
    if len(c1.items) >= 6:
        print 'Items are full, choose item to sell:'
        c1.showItems()
        r = raw_input('Which item slot do you want to emtpy? -->')
        try:
            c1.items.pop(int(r))
        except:
            print 'List index out of range, you\'ve been booted from the shop for tomfoolery'
            return 1
    s = raw_input('type an item\'s name to buy it, or "list" to see all of the items names -->')
    if s == 'list':
        shoplist(k)
        s = raw_input('type an item\'s name to buy it -->').lower()

    if s in k:
        c1.items.append(s)
        c1.doItems()
        print 'purchased',k[s]['name'],'!'
    else:
        print 'item not found, sorry!'

    l = raw_input('Would you like to keep shopping (Y|N)? -->').lower()
    if l == 'yes' or l == 'y':
        return 0
    else:
        return 1

def shoplist(k):
    # print i
    l = []
    for item in k:
        print item
        # l.append(k[item])
    # print l
    # l.sort()
    # print l

def init(p):
    # conn = pymongo.Connection('mongodb://d:b@ds031877.mongolab.com:31877/lolapi')
    # db = conn.lolapi
    if p == 1:
        while True:
            inp = raw_input('Who do you want to play as? -->').lower()
            if inp == 'akali' or inp == 'ahri' or inp == 'alistar' or inp == 'amumu' or inp == 'anivia' or inp == 'annie' or inp == 'ashe':
                break
    else:
        inp = 'akali'
    c = getChamp(inp)
    # champ = db.champs.find({'name':inp},limit=1)
    # for i in champ:
        # c = prepare(i)
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
    while True:
        a = act(c1,c2)
        if a: 
            break
    checkState(c1,c2)
    try:
        c1.tick(c2)
    except:
        c1.tick()
    c2.tick()
