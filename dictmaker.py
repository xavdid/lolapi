from bs4 import BeautifulSoup
import re
import urllib2
from functions import namer,pretty,urlGrab

def souper(url): #takes the na.leagueoflegends.com url
	champ = {}
	soup = BeautifulSoup(urlGrab(url)) #string name, can build string from file
	s = soup.find_all('table')[1] #this is the stats_table tag
	
	for c in s.contents:
		if str(c)[0] == '<':
			key = namer(c.contents[1].string)
			champ[key+'_base'] = float(c.contents[3].string)
			if c.contents[5].span:
				champ[key+'_ratio'] = float(re.search(r'\+([ 0-9\.]*)',c.contents[5].span.string).group(1))
	return champ

def regexer(url): #takes the lolwiki url
	s = urlGrab(url)
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
					if (t == 'cooldown' or t == 'cost'): #there's more here...
						if ab == 'R':
							j = pretty(j,True)
						else:
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
	return c

# print d

