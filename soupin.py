from bs4 import BeautifulSoup


d = {}
df = ''

f = open('champs/cait.html','r')
for line in f:
	df+=line

soup = BeautifulSoup(df) #string name, can build string from file

s = soup.find_all('table')[1] #this is the stats_table tag

for c in s.contents:
	if str(c)[0] == '<':
		# print c.contents[1].string
		d[c.contents[1].string] = float(c.contents[3].string)

# if s.contents[1].contents[1].string == 'Damage': #this is how i'm going to find stuff
	# print 'yes!'
# print s.contents[1].contents[5].span.string #gets the third, since there's that extra tag
print d