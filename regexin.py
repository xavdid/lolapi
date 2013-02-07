import re
from pprint import pprint

def pretty(s):
	s = s.strip('{}')
	s = s.replace('ap','0')
	s = s.replace('|',',')
	s = s.split(',')
	s = [int(x) for x in s]
	if len(s) == 1:
		s = s[0]
	return s

f = open('champs/cait.txt','r')
s=''
for line in f:
	s+=line

c = {}
for ab in ['P','Q','W','E','R']:
	print 'ab is: '+ab
	a = re.search(r'^{{Ability\|(?P<id>%s).*?^}}'%ab,s,re.M|re.DOTALL)
	c[a.group('id').lower()] = {}
	# things = ['damage','damage_ratio','damage_ratio_type','name','cd','description','range','cost_val','cost_type']
	things = ['description','name','cooldown','cost','costtype','range','leveling']
	for t in things:
		try:
			if t == 'leveling':
				j = re.search(r'\|leveling *=([. \{\}A-Za-z\|0-9\(\)+%\n]*?)(?=\n^(\||\}))',a.group(0),re.M).group(1)
			else:
				j = re.search(r'^\|%s=(.+)'%t,a.group(0),re.M).group(1)
			if j:
				if (t == 'cooldown' or t == 'cost' or t == 'range'): #there's more here than these keys...
					# if len(j) > 4:
						# print 'making pretty for '+t
					j = pretty(j)
				elif (t == 'leveling'):
					ratio = re.search(r'ability scaling\|\(\+([ 0-9]*)',j).group(1).strip()
					c[a.group('id').lower()]['damage_ratio'] = float(ratio)/100.0

					damage_type = re.search(r'{{lc\|(.*?})',j).group(1)
					if damage_type[0] == 'P':
						c[a.group('id').lower()]['damage_type'] = 'physical'
					elif damage_type[0] == 'M':
						c[a.group('id').lower()]['damage_type'] = 'magic'
					else:
						c[a.group('id').lower()]['damage_type'] = 'true'

					damage = re.search(r'ap[\|0-9]*',j).group(0)
					damage = pretty(damage)
					c[a.group('id').lower()]['damage'] = damage
				elif (t == 'description'):
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

