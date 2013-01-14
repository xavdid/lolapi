import re
from pprint import pprint

def pretty(s):
	s = s.strip('{}')
	s = s.replace('ap','0')
	s = s.replace('|',',')
	s = s.split(',')
	s = [int(x) for x in s]
	return s

f = open('cait.txt','r')
s=''
for line in f:
	s+=line

c = {}
for ab in ['P','Q','W','E','R']:
	a = re.search(r'^{{Ability\|(?P<id>%s).*?^}}'%ab,s,re.M|re.DOTALL)
	c[a.group('id').lower()] = {}
	things = ['damage','damage_ratio','damage_ratio_type','name','cd','desc','range','cost_val','cost_type']
	for t in things:
		try:
			c[a.group('id').lower()]['name'] = re.search(r'^\|name=(.+)',a.group(0),re.M).group(1)
			c[a.group('id').lower()]['desc'] = re.search(r'^\|description=(.+)',a.group(0),re.M).group(1) #i could check for/funct out the {{Active}} bit 
		
			j = re.search(r'^\|cost=(.+)',a.group(0),re.M).group(1)
			if len(j) > 3:
				j = pretty(j)
			c[a.group('id').lower()]['cost'] = j
		except:
			print 'wait! the key %s for this champ gives and error!' % t
			
pprint(c)

