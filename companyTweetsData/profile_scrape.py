import sys
import csv
import os
import glob
path = "*.csv"

try:
    import bs4
except ImportError:
    raise ImportError('BeautifulSoup needs to be installed. Please run "sudo apt-get install python-bs4"')
except AttributeError:
	raise AttributeError('bs4 needs to be upgraded. Please run "pip install --upgrade beautifulsoup4"')
try:
    import requests
except ImportError:
    raise ImportError('Requests needs to be installed. Please run "sudo pip install requests"')

for fname in glob.glob(path):
	if (fname != 'temp.csv'):
		with open(fname) as csvfile :
			readCSV = csv.reader(csvfile, delimiter=',')
			with open('temp.csv', "w") as output:
				print 'file: ' + fname
				for row in readCSV:
					url = 'https://twitter.com/FalcoLombardi/status/' + row[6]
					page = requests.get(url)
					soup = bs4.BeautifulSoup(page.text, 'html.parser')

					usernameTag = soup.find('b', {'class':'u-linkComplex-target'})
					username = usernameTag.text.encode('utf-8') 

					url = 'https://twitter.com/' + username

					page = requests.get(url)
					soup = bs4.BeautifulSoup(page.text, 'html.parser')
					bioTag = soup.find('p', {'class':'ProfileHeaderCard-bio u-dir'})
					bio = bioTag.text.encode('utf-8') 
					followersTag = soup.find('a', {'data-nav':'followers'})
					followingTag = soup.find('a', {'data-nav':'following'})
					verifiedTag = soup.find('span', {'class':'ProfileHeaderCard-badges'})
	
					try:
						following = followingTag['title'].split(' ')[0]
					except TypeError:
						following = 0
					try:
						followers = followersTag['title'].split(' ')[0]
					except TypeError:
						followers = 0

					verified = 1
					if (verifiedTag is None):
						verified = 0
					
					writer = csv.writer(output, delimiter=',')
					r = row[0], row[1], row[2], row[3], row[4], row[5], row[6], username, bio, following, followers, verified
					writer.writerow([s for s in r])
		os.rename('temp.csv', fname)
print '- - Finished - -'










