loldb
=====

A restful API for returning champion and item stats for League of Legends. The database holds all the stats. It's updated from a bunch of jsons. 

To see it run, follow a few easy steps:

1. Make sure you've got mongodb installed and running (`sudo mongod`).
2. Run `python main.py` in the correct directory.
3. Go to [localhost/patch](http://localhost:8888/patch) to populate the database.
4. Hit [localhost/champions/show/ahri](http://localhost:8888/champions/show/ahri) (Ahri is the only one coded for now) to see the fruits of your labor.
5. You can also check Akali, Alistar and items now. Patching updates the jsons of all 4, so go nuts. 
6. You can change any of the numbers in the jsons, swing by [/patch](http://localhost:8888/patch) and back to [/show/ahri](http://localhost:8888/champions/show/ahri) see it change before your very eyes!
7. Also, if you're just interested in the whole json, go to [/champions/show/NAME/json](http://localhost:8888/champions/show/ahri/json)


How it works
------------
For now, ignore everything in <champions/add> as it's just placeholder code (routes.py, lines 12-136. The meat is in <champions/show>, which writes out the stats based on level and items. If right now it's just missing a bunch of champs and items, but that's just a matter of data input, so I'll get it done. Honestly, if you can write some inheritence and lines 161+162 (in <routes.py>), we'll be golden. 