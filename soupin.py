from bs4 import BeautifulSoup
import re

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

d = {}
df = ''

f = open('champs/cait.html','r')
for line in f:
	df+=line

soup = BeautifulSoup(df) #string name, can build string from file

s = soup.find_all('table')[1] #this is the stats_table tag

#+0.55 / per level
for c in s.contents:
	if str(c)[0] == '<':
		key = namer(c.contents[1].string)
		d[key+'_base'] = float(c.contents[3].string)
		if c.contents[5].span:
			d[key+'_ratio'] = float(re.search(r'\+([ 0-9\.]*)',c.contents[5].span.string).group(1))


# if s.contents[1].contents[1].string == 'Damage': #this is how i'm going to find stuff
	# print 'yes!'

# for c in s.contents:
# 	if str(c)[0] == '<':
# 		if c.contents[5].span:
# 			print c.contents[5].span.string #gets the third, since there's that extra tag
print d

