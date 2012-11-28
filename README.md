loldb
=====

A restful API for returning champion and item stats for League of Legends. The database holds all the stats. It's updated from a bunch of jsons. 

To see it run, follow a few easy steps:

1. Make sure you've got mongodb installed and running (`sudo mongod`).
2. Run `python main.py` in the correct directory.
3. Go to [localhost/patch](http://localhost:8888/patch) to populate the database.
4. Hit [localhost/champions/show/ahri](http://localhost:8888/champions/show/ahri) (Ahri is the only one coded for now) to see the fruits of your labor.
5. You can also check Akali/items now. Patching updates the jsons of all 3, so go nuts. 
6. You can change any of the numbers in the jsons, swing by [/patch](http://localhost:8888/patch) and back to [/show/ahri](http://localhost:8888/champions/show/ahri) see it change before your very eyes!

Please leave any feedback you've got so far!
