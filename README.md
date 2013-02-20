#LoLdb


A restful API for returning champion and item stats for League of Legends. The database holds all the info you could ever want to know about LoL champions. It's updated from a bunch of jsons that I maintain. You can see the live version at (lolapi.net)[lolapi.herokuapp.com].


##About the code

This code is actually 2 products side by side: 

1. A restful API full of data on champions and their abilities. This is mean to be used by the public for the creation of awesome LoL apps. 
2. A duel between champions taking into account most of the LoL engine created entirely in Python. This was intended to fill the gap of a sandbox mdoe for LoL (or -wtf for the Dota vets). This is mostly a proof of concept for using my own API, but it was also an awesome coding exercise. 

###The story

I’ve always loved coding and working with databases, so the natural idea was a simulator to test champion builds. Unfortunately, routinely maintained champ data is hard to come by and/or hard to parse. So, I decided that I needed to make my own dataset if I was going to have any sort of stability. After typing the first couple of .json files manually, I recognized that an automated algorithm was the way to go. Processing what I scraped from both the lolwiki source and the league site itself yielded nicely formatted results. Those files in hand, I could easily edit them and patch to a cloud database so that anyone using my API would have current data.  

With my database in hand, I turned my focus to the simulator. It grew rapidly in both size and complexity when I realized I not only wanted to test builds, but champion matchups as well. I fervently coded an entire LoL engine complete with abilities, buffs, items, stat caps, resistances, and champions (which became dramatically harder than I had initially expected). It was quite the journey- realizing every 10 lines that I needed another feature or function, which kept me on my toes throughout.

##Where does this data come from?

All of the data about champion base stats is scraped from [Riot's Champion info section](http://na.leagueoflegends.com/champions) using the python library Beautiful Soup. 

All of the ability descriptions, damage, and scaling is pulled from the [LoLWiki](http://leagueoflegends.wikia.com/api.php?action=query&titles=ashe&prop=revisions&rvprop=content&format=dumpfm) source and parsed using Python's Regex library (re).

All of the code from both can be found in `dictmaker.py`.

##I want to play in the sandbox!
Cool! Clone the repo, install the requirements (`pip install requirements.txt`) and run battle (`python battle.py`)! At this point, you shouldn't get any errors, but... well, we know how that works. Kindy contact me through git or email me at beamneocube (at) gmail (dot) com to report bugs.
###Notable changes in the sandbox vs the real LoL client
Firstly, the sandbox is commandline. One second passes per actual action taken. You can reduce cooldowns to non-whole numbers, but you still can't use the ability until the cooldown is < 0.  
The big change is in attack speed- since there wasn't a great way to adjust the time frame, each attack is your AD*your attack speed. So, if your attack speed is only .7, you would have only launched most of your attack, so you don't get the full value.  
Also, slow's (while accounted for), don't really do much, as there's no motion.
###Will there be an AI?
Maybe at some point. As it stands, there's an Akali that just auto attacks you until one of you is dead. I've got a plan for AI, but as of today (Feb 20, 2013), I'm too busy to do something that non-essential. 

##Frequently Answered Queries

1.  Q: Why did you make this?  
	A: First and foremost, I love League and wanted to enable other developers to make great things with conveniently available datasets. Secondly, I really want to work at Riot and thought the best way to get my foot in the door was to make a totally badass project and get it shipped, so I did. 
	
2.  Q: Can I count on you to keep the database stay updated?  
	A: It should! Now that all the data is in, it should be quite easy to maintain. If I'm going to be indisposed for an inordinate amount of time, I'll make sure it gets seen to.

3.  Q: What's in it for you?  
	A: Personally, not much. It was a fun puzzle and I learned a lot. Hopefully other devs in the LoL community will utilize it and make some awesome apps! Also, see 'job at Riot'.


##I want to fiddle with your code!
Awesome! I encourage it. Hopefully I've made it easy enough to understand and it can be used to answer some mid level python/tornado questions.
#####To run a local instance using the cloud database, follow a few easy steps:

1. Make sure to use the non-authenticated connection version (found in `functions.py@getChamp()`.
2. run `python main.py` in the appropriate directory (default port is 8888, you can change it on the command line if you're so inclined).
4. Visit [localhost/champions/show/ahri](http://localhost:8888/champions/show/ahri) (or any champion who's name starts with A) to see them duel to the death against Akali. As it stands, they're coded to auto attack each other the while time, but you can change that behavior in `routes.py` under the comment header "#Where they fight!".
7. To see a champion's whole json, append/json to any /champions/show/NAME; that is, [/champions/show/ahri/json](http://localhost:8888/champions/show/ahri/json).

#####To create and use a local database:

1. Right now my code references the cloud, so you'll need to change each instance of `pymongo.connection()` to the default. You may be able to just leave those parens blank and it'll use 27017. For reference, you can check their site [here](http://docs.mongodb.org/manual/tutorial/manage-mongodb-processes/).
1. You'll need your own instance of mongo running. Download it and run it with `sudo mongod`.
1. Then, start following at #2 in the above section.