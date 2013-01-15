import re
from pprint import pprint

def pretty(s):
	s = s.strip('{}')
	s = s.replace('ap','0')
	s = s.replace('|',',')
	s = s.split(',')
	s = [int(x) for x in s]
	# if len(s) == 0:
		# s = s[0]
	return s

f = open('champs/cait.txt','r')
s=''
for line in f:
	s+=line

c = {}
for ab in ['P','Q','W','E','R']:
# for ab in ['Q','W','E','R']:
	print 'ab is: '+ab
	a = re.search(r'^{{Ability\|(?P<id>%s).*?^}}'%ab,s,re.M|re.DOTALL)
	c[a.group('id').lower()] = {}
	# things = ['damage','damage_ratio','damage_ratio_type','name','cd','description','range','cost_val','cost_type']
	things = ['description','name','cooldown','cost','costtype','range']
	for t in things:
		try:
			j = re.search(r'^\|%s=(.+)'%t,a.group(0),re.M).group(1)
			# c[a.group('id').lower()]['desc'] = re.search(r'^\|description=(.+)',a.group(0),re.M).group(1) #i could check for/funct out the {{Active}} bit 
			if j:
				if (t == 'cooldown' or t == 'cost' or t == 'range'): #there's more here...
					if len(j) > 3:
						# print 'making pretty for '+t
						j = pretty(j)
				if (t == 'description'):
					if j[0] == '{':
						if j[6] == 'A':
							j = 'Active: '+j[15:]
						else:
							j = 'Passive: '+j[16:]

				if t == 'costtype':
					t = 'cost_type'
				c[a.group('id').lower()][t] = j
		except:
			print 'wait! the key %s for their %s this champ gives an error!' % (t,ab)
			pass
			
pprint(c)

