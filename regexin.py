import re
from pprint import pprint
import urllib2

def pretty(s):
	s = s.strip('{}')
	s = s.replace('ap','0')
	s = s.replace('|',',')
	s = s.split(',')
	s = [int(x) for x in s]
	if len(s) == 1:
		s = s[0]
	return s

# f = open('champs/leona.txt','r')
# f = open('champs/cait.txt','r')
resp = urllib2.urlopen('http://leagueoflegends.wikia.com/api.php?action=query&titles=leona&prop=revisions&rvprop=content&format=dumpfm')

s = resp.read()
# s=''
# for line in f:
	# s+=line

c = {}
for ab in ['P','Q','W','E','R']:
	print 'ab is: '+ab
	a = re.search(r'^{{Ability\|(?P<id>%s).*?^}}'%ab,s,re.M|re.DOTALL)
	c[a.group('id').lower()] = {}

	things = ['description','description2','name','cooldown','cost','costtype','range','leveling']
	for t in things:
		try:
			if t == 'leveling':
				j = re.search(r'\|leveling *=([. \{\}A-Za-z\|0-9\(\)+%\n]*?)(?=\n^(\||\}))',a.group(0),re.M).group(1)
			else:
				j = re.search(r'^\|%s *= *(.+)'%t,a.group(0),re.M).group(1).strip()
			if j:
				if (t == 'cooldown' or t == 'cost' or t == 'range'): #there's more here...
					j = pretty(j)
				elif (t == 'leveling'):
					#first ability ratio
					ratio = re.search(r'\{\{(ability scaling|as)\|\(\+([ 0-9]*)',j).group(2).strip()
					c[a.group('id').lower()]['damage_ratio'] = float(ratio)/100.0
					#ability's damage type
					damage_type = re.search(r'{{lc\|(.*?})',j).group(1)
					if damage_type[0] == 'P':
						c[a.group('id').lower()]['damage_type'] = 'physical'
					elif damage_type[0] == 'M':
						c[a.group('id').lower()]['damage_type'] = 'magic'
					elif damage_type[0] == 'H':
						print 'healing!'
						damage = re.search(r'ap[\|0-9]*',j).group(0)
						damage = pretty(damage)
						c[a.group('id').lower()]['ally_heal_val'] = damage
					else:
						c[a.group('id').lower()]['damage_type'] = 'true'

					if damage_type[0] != 'H':	
						damage = re.search(r'ap[\|0-9]*',j).group(0)
						damage = pretty(damage)
						c[a.group('id').lower()]['damage'] = damage
				elif (t == 'description' or t == 'description2'):
					if j[0] == '{':
						if j[6] == 'A':
							j = 'Active: '+j[15:]
						else:
							j = 'Passive: '+j[16:]


				elif t == 'costtype':
					t = 'cost_type'
				c[a.group('id').lower()][t] = j
		except:
			print 'wait! the key %s for %s gives this champ an error!' % (t,ab)
			
pprint(c)

