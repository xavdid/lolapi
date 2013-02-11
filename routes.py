from functions import *
import pymongo
# from base import route, Champion, Ahri, ItemBase, ChampBase, Akali
from base import *
import simplejson as json
import asyncmongo
import tornado.web
from tornado.web import asynchronous
from tornado.gen import engine, Task
from pprint import pprint
from secrets import patchkey
from dictmaker import *

@route('/champions/add')
class ChampAdd(tornado.web.RequestHandler):
    def get(self):
    	c = pymongo.Connection()
        db = c.loldb
        champ = ChampBase()

        champ.stats = souper('http://na.leagueoflegends.com/champions/34/anivia_the_cryophoenix')
        champ.moves = regexer('http://leagueoflegends.wikia.com/api.php?action=query&titles=anivia&prop=revisions&rvprop=content&format=dumpfm')
        #boom
        # asdf = ItemBase()
        # asdf.items = {"ruby":{"name":"Ruby Crystal","effect":{"hp":180},"cost":475,"tag":"ruby"},
            # "amp_tome":{"name":"Amplification Tome","effect":{"ap":20},"cost":435,"tag":"amp_tome"}}
        # asdf.name = 'items'
        champ.name = 'anivia'
        champ.title = 'the Cryophoenix'
        # st = {}
        # st['hp_base'] = 472.0
        # st['hp_ratio'] = 84.0
        # st['hpreg_base'] = 7.45
        # st['hpreg_ratio'] = 0.85
        # # st['energy'] = 200
        # st['mana_base'] = 220.0
        # st['mana_ratio'] = 40.0
        # st['manareg_base'] = 6.50
        # st['manareg_ratio'] = 0.525
        # st['arange'] = 125.0
        # st['ad_base'] = 47.0
        # st['ad_ratio'] = 3.80
        # st['as_base'] = 0.638
        # st['as_ratio'] = 2.18
        # st['armor_base'] = 18.0
        # st['armor_ratio'] = 3.3
        # st['mr_base'] = 30.0
        # st['mr_ratio'] = 1.25
        # st['ms'] = 335.0
        # champ.stats = st
        
        # i = {}
        # i['name'] = 'Cursed Touch'
        # i['desc'] = 'Amumu\'s attacks reduce the target\'s magic resistance by 15/25/35 for 3 seconds. The debuff doesn\'t stack but it refreshes with every attack.'
        # i['on_hit'] = {'mr':[-15,-25,-35]}
        # # i['damage_ratio'] = 1
        # # i['damage ratio type'] = 'level'
        # # i['damage_ratio_b'] = .1
        # # i['damage_ratio_type_b'] = 'ap'
        # champ.moves['i'] = i
        
        # q = {}
        # q['name'] = 'Bandage Toss'
        # q['desc'] = "(Active): Amumu tosses a sticky bandage towards a target location, if it contacts an enemy Amumu pulls himself to it and will deal magic damage and stun the target for 1 second."
        # q['range'] = 1100.0
        # q['cd'] = [0,16.0,14.0,12.0,10.0,8.0]
        # q['cost_val'] = [0,80,90,100,110,120]
        # q['cost_type'] = 'mana'
        # q['damage'] = [0,80,140,200,260,320]
        # q['damage_type'] = 'magic'
        # q['damage_ratio'] = 0.7
        # q['damage_ratio_type'] = 'ap'
        # # q['energy_restored'] = [0,15,20,25,30,35]
        # # q['damage_b'] = [0,40,65,90,115,140]
        # # q['damage_b_type'] = 'true'
        # # q['damage_b_ratio'] = 0.33
        # # q['damage_b_ratio_type'] = 'ap'
        # champ.moves['q'] = q

        # w ={}
        # w['name'] = 'Despair'
        # w['desc'] = "(Toggle): Overcome by anguish, nearby enemies will be dealt a percentage of their maximum health plus a base amount as magic damage each second."
        # w['range'] = 300
        # # w['kockback'] = 650
        # w['cd'] = [0,1,1,1,1,1]
        # w['cost_val'] = [0,8,8,8,8,8]
        # w['cost_type'] = 'mana'
        # w['on'] = False
        # # w['defense_boost'] = [0,10,20,30,40,50]
        # # w['ms_reduction'] = [0,14,18,22,26,30]
        # # w['ms_reduction_type'] = 'percent'
        # w['damage'] = [0,8,12,16,20,24]
        # w['damage_type'] = 'magic'
        # w['damage_b'] = [0,1.5,1.8,2.1,2.4,2.7]
        # w['damage_ratio_b'] = 0.01
        # w['damage_ratio_type_b'] = 'ap'
        # # w['damage_max'] = [0,80,130,180,230,280]
        # # w['damage_max_ratio'] = 0.4
        # # w['damage_max_ratio_type'] = 'ap'
        # champ.moves['w'] = w

        # e = {}
        # e['name'] = 'Tantrum'
        # e['desc'] = "(Passive): Amumu takes reduced damage from physical attacks. Each time Amumu is hit by an attack, the cooldown on Tantrum's active is reduced by half a second. \
        #             (Active): Amumu deals magic damage to surrounding units. "
        # e['range'] = 200.0
        # e['cd'] = [0,10,9,8,7,6]
        # e['cost_val'] = [0,35,35,35,35,35]
        # e['cost_type'] = 'mana'
        # e['damage'] = [0,75,100,125,150,175]
        # e['damage_block'] = [0,2,4,6,8,10]
        # # e['self_heal_val'] = [0,60,90,120,150,180]
        # # e['self_heal_ratio'] = .2
        # # e['ally_heal_val'] = [0,30,45,60,75,90]
        # # e['ally_heal_ratio'] = .1
        # e['damage_type'] = 'magic'
        # e['damage_ratio'] = 0.5
        # e['damage_ratio_type'] = 'ap'
        # # e['heal_ratio_type'] = 'ap'
        # # e['damage_ratio_b'] = 0.3
        # # e['damage_ratio_type_b'] = 'ap'
        # # e['duration'] = [0,1,1.25,1.5,1.75,2]
        # champ.moves['e'] = e

        # r ={}
        # r['name'] = 'Curse of the Sad Mummy'
        # r['desc'] = "(Active): Amumu entangles surrounding enemy units in bandages, dealing magic damage upfront and rendering them unable to attack or move for 2 seconds."
        # r['range'] = 600
        # r['cd'] = [0,150.0,130.0,110.0,110.0,110.0]
        # r['cost_val'] = [0,100,150,200,200,200]
        # r['damage'] = [0,150,250,350,350,350]
        # r['cost_type'] = 'mana'
        # r['damage_type'] = 'magic'
        # r['damage_ratio'] = 0.8
        # r['damage_ratio_type'] = 'ap'
        # champ.moves['r'] = r
        # pprint(champ.to_python())
        # pprint(asdf.items)
        # db.champs.update({'name':"items"},asdf.to_python(),True)


        db.champs.update({'name':champ.name},champ.to_python(),True)
        c = getChamp(champ.name)
        # self.write(c)
        f = open('champs/%s.json'%champ.name,'w+')
        # f.write()
        # f.close()

        # self.write(champ.to_python())
        # self.write('stored %s, %s!' %(champ.name.title(), champ.title))

@route('/champions/show/(\w+)')
class ChampPrint(tornado.web.RequestHandler):
    # @engine
    # @asynchronous
    def get(self,input):
        c = getChamp(input)
        try:
            if (input == 'akali'):
                a = Akali(c)
            elif (input == 'ahri'):
                a = Ahri(c)
            elif (input == 'alistar'):
                a = Alistar(c)
            elif (input == 'amumu'):
                a = Amumu(c)
            else:
                assert(1==0)
        except AssertionError:
            self.write('Champion not found')

        else:
        #this is for nice output
            # self.write(c)
            a.items.append('faeriecharm')
            a.items.append('faeriecharm')
            # a.items.append('brutalizer')
            a.doItems()
            self.write('Name: <b>%s</b>, %s<br>' %(a.name.title(),a.title))
            for s in a.cur_stats:
                self.write('%s: %s <br>' %(s.replace('_',' ').title(), a.cur_stats[s]))

            # self.write(str(a.canCast('q')))

            # self.write("<br>Items:")
            # self.write(breaks(2))
        #i could have one of these rows in the base class so we could see stuff like this?

        #these lines are for testing each ability- they're not vital right now
            # self.write("%s's Q does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.q(),a.c['moves']['q']['damage_type'],a.cur_stats['ap'],a.c['moves']['q']['damage_ratio_type'].upper()))
            # self.write("<br><br>")
            # self.write("%s's E does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.e(),a.c['moves']['e']['damage_type'],a.cur_stats['ap'],a.c['moves']['e']['damage_ratio_type'].upper()))
            # self.write(breaks(2))
            # a.items.append('ruby')
            # a.items.append('amp_tome')
            # a.items.append('dblade')
            # a.items.append('brutalizer')
            # a.doItems()
            self.write(breaks(1))
        # # initializing second champ, only needed for fighting
            asdf = getChamp('akali')
            b = Akali(asdf)
            self.write('Name: <b>%s</b>, %s<br>' %(b.name.title(),b.title))
            b.items.append('nullmagic')
            b.items.append('giantbelt')
            b.items.append('giantbelt')
            b.items.append('giantbelt')
            # b.doItems()
            for s in b.cur_stats:
                self.write('%s: %s <br>' %(s.replace('_',' ').title(), b.cur_stats[s]))
        
        # # where they fight!
            i = 0
            cooldown = 0
            # while (True):
            while(i<700):
                self.write(breaks(1))
                self.write('%s has %i HP left\n' %(a.name,a.hp()))
                self.write('%s has %i HP left\n' %(b.name,b.hp()))
                a.useAbility('q',b)
                    # a.mana(-(a.c['moves']['q']['cost_val'][5]))
                # else: 
                    # self.write('unable to cast')
                    # print 'mana when can\'t cast: '+str(a.cur_stats['mana'])
            # exit condition!
                if b.hp()<=0:
                    break
                a.tick()
                b.tick()
                self.write(" tick "+str(i))
                i+=1
                # hp = b.hp()
                # print 'mana:'+str(a.mana())+' tick: '+str(i)





            # self.write("<br>Items:<br>")
            # self.write(' '.join(a.items)+"<br>")
            # self.write(breaks(2))
            # for s in a.cur_stats:
            #     self.write('%s: %s <br>' %(s.replace('_',' ').title(), a.cur_stats[s]))
            # self.write("%s's Q does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.q(),a.c['moves']['q']['damage_type'],a.cur_stats[a.c['moves']['q']['damage_ratio_type']],a.c['moves']['q']['damage_ratio_type'].upper()))

            # self.write(breaks(2))
            # self.write("%s's E does %s %s damage at lvl 18 with %s %s" %(a.name.title(), a.e(),a.c['moves']['e']['damage_type'],a.cur_stats[a.c['moves']['e']['damage_ratio_type']],a.c['moves']['e']['damage_ratio_type'].upper()))
            # self.write("<br> it would do %.3f against someone with 115 armor"%(damageMult(a.e(),115)))

        #this is for printing the whole response
            # self.write(c)

@route('/champions/show/(\w+)/json')
class ChampPrintJson(tornado.web.RequestHandler):
    def get(self,input):
        c = getChamp(input)
        try:
            if (input == 'akali'):
                a = Akali(c)
            elif (input == 'ahri'):
                a = Ahri(c)
            elif (input == 'alistar'):
                a = Alistar(c)
            else:
                assert(1==0)
        except:
            self.write('Champion not found')

        else:
            self.write(c)
            
@route('/patch/(\w+)')
class PatchHandler(tornado.web.RequestHandler):
    def get(self,input):
        if input == patchkey:
            co = pymongo.Connection()
            db = co.loldb
            champlist = ['items','ahri','akali','alistar','amumu']
            for n in champlist: 
                js = open('champs/%s.json' %n)
                c = json.load(js)
                if (n=='items'):
                    ch = ItemBase()
                    ch.items = c
                    ch.name = 'items'
                else:
                    ch = ChampBase()
                    attach(ch,c)

                db.champs.update({'name':n},ch.to_python(),True)
                # pprint(ch.to_python())
                js.close()
            self.write('patched to v 1.0.3.1!')
        else:
            self.write('secret key not included, patching failed')

