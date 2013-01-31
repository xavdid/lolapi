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

# s = "{{Ability|E\
# |name=90 Caliber Net\
# |icon=90CaliberNet.jpg\
# |description={{sbc|Active:}} Caitlyn fires a net, knocking herself back 400 units in the opposite direction. The net will deal magic damage and slow the first enemy hit by 50%.\
# |leveling ={{lc|Magic damage}} {{ap|80|130|180|230|280}} {{ability scaling|(+ 80% AP)}}\
# {{lc|Slow duration}} {{ap|1|1.25|1.5|1.75|2}}\
# |cooldown={{ap|18|16|14|12|10}}\
# |cost=75\
# |costtype=mana\
# |range=1000\
# }}"

# re.search(r'\|leveling[\{\}a-zA-Z\|0-9\n,=\(\)+%\.]*?(?=\n^(\||\}\}))',s,re.M)


c = {}
for ab in ['P','Q','W','E','R']:
# for ab in ['Q','W','E','R']:
	print 'ab is: '+ab
	a = re.search(r'^{{Ability\|(?P<id>%s).*?^}}'%ab,s,re.M|re.DOTALL)
	c[a.group('id').lower()] = {}
	# print 'look: '+a.group(0)
	# things = ['damage','damage_ratio','damage_ratio_type','name','cd','description','range','cost_val','cost_type']
	things = ['description','name','cooldown','cost','costtype','range','leveling']
	for t in things:
		try:
			if t == 'leveling':
				j = re.search(r'\|leveling[. \{\}=A-Za-z\|0-9\(\)+%\n]*?(?=\n^(\||\}))',s,re.M).group(0)
				# print j
			else:
				j = re.search(r'^\|%s=(.+)'%t,a.group(0),re.M).group(1)
				# c[a.group('id').lower()]['desc'] = re.search(r'^\|description=(.+)',a.group(0),re.M).group(1) #i could check for/funct out the {{Active}} bit 
				if j:
					if (t == 'cooldown' or t == 'cost' or t == 'range'): #there's more here than these keys...
						# if len(j) > 4:
							# print 'making pretty for '+t
						j = pretty(j)
					elif (t == 'description'):
						if j[0] == '{':
							if j[6] == 'A':
								j = 'Active: '+j[15:]
							else:
								j = 'Passive: '+j[16:]

					elif t == 'costtype':
						t = 'cost_type'
					elif t == 'leveling':
						print 'FOUND THIS! %s'%j
					c[a.group('id').lower()][t] = j
		except:
			print 'wait! the key %s for %s gives this champ an error!' % (t,ab)
			
pprint(c)

