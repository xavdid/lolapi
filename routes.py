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
from secrets import username,password
from dictmaker import *
import sys, traceback

@route('/')
class FrontPage(tornado.web.RequestHandler):
    def get(self):
        s = '<html><title>LoL API</title>\
            <body> <font size = 8> Welcome to the LoL API!</font><br><br>\
            Click on a champion name below to get a .json of their data:<br>\
            <a href = "/champions/show/ahri/json">Ahri</a><br>\
            <a href = "/champions/show/akali/json">Akali</a><br>\
            <a href = "/champions/show/alistar/json">Alistar</a><br>\
            <a href = "/champions/show/amumu/json">Amumu</a><br>\
            <a href = "/champions/show/anivia/json">Anivia</a><br>\
            <a href = "/champions/show/annie/json">Annie</a><br>\
            <a href = "/champions/show/ashe/json">Ashe</a><br>\
            <a href = "/champions/show/items/json">Items</a><br><br>'
        s += 'I also made an app to test builds and champion matchups! To download it, just click <a href="/download"> here</a>!<br><br><br>'
        s += '<footer>\
                <p>Made by David <a href="http://www.umich.edu/~brownman">Brownman</a> (who is not a web designer)</p>\
                <p>Contact him <a href=mailto:beamneocube@gmail.com>here</a>.\
                <p> LoL API isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.\
                </footer> '
        s += '</body>\
            </html>'
        self.write(s)

@route('/download')
class DLPage(tornado.web.RequestHandler):
    def get(self):
        self.set_header ('Content-Type', 'archive/tar')
        self.set_header ('Content-Disposition', 'attachment; filename=battle.tar')
        f = open('battle.tar','r')
        self.write(f.read())

@route('/champions/add')
class ChampAdd(tornado.web.RequestHandler):
    def get(self):
    	# c = pymongo.Connection()
        # db = c.loldb
        champ = ChampBase()

        champ.stats = souper('http://na.leagueoflegends.com/champions/34/anivia_the_dark_child') #takes na.league url
        champ.moves = regexer('http://leagueoflegends.wikia.com/api.php?action=query&titles=annie&prop=revisions&rvprop=content&format=dumpfm') #takes lolwiki
        champ.name = 'annie'
        champ.title = 'the Dark Child'
        
        self.write(champ.to_python())


        # self.write(champ.to_python())
        # self.write('stored %s, %s!' %(champ.name.title(), champ.title))

@route('/champions/show/(\w+)')
class ChampPrint(tornado.web.RequestHandler):
    # @engine
    # @asynchronous
    def get(self,input):
        c = getChamp(input)
        # print 'in print, input is',input
    # try:
        if (input == 'akali'):
            a = Akali(c)
        elif (input == 'ahri'):
            a = Ahri(c)
        elif (input == 'alistar'):
            a = Alistar(c)
        elif (input == 'amumu'):
            a = Amumu(c)
        elif (input == 'anivia'):
            a = Anivia(c)
        elif (input == 'annie'):
            a = Annie(c)
        elif (input == 'ashe'):
            a = Ashe(c)
        else:
            assert(1==0)
    # except:
            # self.write('Champ not found')
        #this is for nice output
        # self.write(c)
        if 1==0: pass
        else:
            a.items.append('faeriecharm')
            a.items.append('faeriecharm')
            a.items.append('recurvebow')
            a.items.append('giantbelt')
            a.items.append('chainvest')
            a.items.append('amptome')
            # a.items.append('brutalizer')`
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
            
            # a.items.append('dblade')
            # a.items.append('brutalizer')
            # a.doItems()
            self.write(breaks(1))
        # # initializing second champ, only needed for fighting
            asdf = getChamp('akali')
            b = Akali(asdf)
            self.write('Name: <b>%s</b>, %s<br>' %(b.name.title(),b.title))
            b.items.append('nullmagic')
            # b.items.append('giantbelt')
            # b.items.append('giantbelt')
            # b.items.append('giantbelt')
            # b.doItems()
            for s in b.cur_stats:
                self.write('%s: %s <br>' %(s.replace('_',' ').title(), b.cur_stats[s]))
        
        # # where they fight!
            i = 0
            cooldown = 0
            # while (True):
            # a.useAbility('r',[b],toggle=True)
            while(i<300):
                self.write(breaks(1))
                self.write('%s has %i HP left\n' %(a.name,a.hp()))
                self.write('%s has %i HP left\n' %(b.name,b.hp()))
                a.useAbility('w',[b])
                # a.autoAttack(b)
                b.autoAttack(a)
                    # a.mana(-(a.c['moves']['q']['cost_val'][5]))
                # else: 
                    # self.write('unable to cast')
                    # print 'mana when can\'t cast: '+str(a.cur_stats['mana'])
            # exit condition!
                # self.write('e\'s cooldown is%s'%a.cur_stats['cooldowns']['e'])

                a.tick()
                if b.hp()<=0:
                    break
                b.tick()
                self.write(" tick "+str(i))
                i+=1
                # hp = b.hp()
                # print 'mana:'+str(a.mana())+' tick: '+str(i)

            for s in a.cur_stats:
                self.write('%s: %s <br>' %(s.replace('_',' ').title(), a.cur_stats[s]))
            self.write('<br>')
            for s in b.cur_stats:
                self.write('%s: %s <br>' %(s.replace('_',' ').title(), b.cur_stats[s]))


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
        self.write(c)
            
@route('/patch')
class PatchHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            if (not username or not password):
                assert(1==0)
            conn = pymongo.Connection('mongodb://%s:%s@ds031877.mongolab.com:31877/lolapi'%(username,password))
        #the line below is the read-only, non-authenticated version.
            # conn = pymongo.Connection('mongodb://ds031877.mongolab.com:31877/lolapi')
            db = conn.lolapi
            champlist = ['items','ahri','akali','alistar','amumu','anivia','annie','ashe']
            for n in champlist: 
                js = open('champs/%s.json' %n) #that is, js = json
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
            self.write('patched to v3.0.1')
        except json.JSONDecodeError:
            self.write('json error')
        except:
            self.write('Authentication error!')

        

