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
			if t == 'leveling':
				j = re.search(r'\|leveling *=([. \{\}A-Za-z\|0-9\(\)+%\n]*?)(?=\n^(\||\}))',a.group(0),re.M)
			else:
				j = re.search(r'^\|%s *= *(.+)'%t,a.group(0),re.M)
			if j:
				j = j.group(1).strip()
				if (t == 'cooldown' or t == 'cost'): #there's more here...
					if ab == 'R':
						j = pretty(j,True)
					else:
						j = pretty(j)
				elif (t == 'leveling'):
					#first ability ratio
					try:
						ratio = re.search(r'\{\{(ability scaling|as)\|\(\+([ 0-9]*)% ([A-Z]*)',j)
						c[a.group('id').lower()]['damage_ratio'] = float(ratio.group(2).strip())/100.0
						c[a.group('id').lower()]['damage_ratio_type'] = ratio.group(3).lower()
					except:
						print 'wait! the ratio in leveling throws and error!'
					#ability's damage type
					try:
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
					except:
						print 'damage type in leveling throws an error!'
					try:
						if damage_type[0] != 'H':	
							damage = re.search(r'ap[\|0-9]*',j).group(0)
							damage = pretty(damage)
							c[a.group('id').lower()]['damage'] = damage
					except:
						print 'still an error in here'

				elif (t == 'description' or t == 'description2'):
					if j[0] == '{':
						if j[6] == 'A':
							j = 'Active: '+j[15:]
						else:
							j = 'Passive: '+j[16:]


				elif t == 'costtype':
					t = 'cost_type'
				try:
					c[a.group('id').lower()][t] = j.lower()
				except:
					c[a.group('id').lower()][t] = j
			
	return c

# print d

