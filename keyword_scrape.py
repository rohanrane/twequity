import sys
import got
import csv
import itertools
from datetime import datetime, timedelta
from dateutil import parser

#TODO: needs to scrape all of twitter for tweets with a keyword AND one of either the company twitter handle or company name
#TODO: also write the user who tweeted to row in csv file

dates = []
names = []
handles = []
eventIDs = []
keywords = []
tweets = []

days_before = 10
days_after = 30

if len(sys.argv) != 3:
	print "run using the following command line arguments: python keyword_scrape.py CSVFILE.csv KEYWORDFILE.txt"
	sys.exit(0)

if (not('.csv' in sys.argv[1]) or not('.txt' in sys.argv[2])):
	print "run using the following command line arguments: python keyword_scrape.py CSVFILE.csv KEYWORDFILE.txt"
	sys.exit(0)


with open(sys.argv[1]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	date = datetime.strptime(row[3], "%m/%d/%Y").strftime("%Y-%m-%d")
        dates.append(date)
        handles.append(row[4])
        names.append(row[2])
        eventIDs.append(row[0])

with open(sys.argv[2]) as keywordFile:
	lines = keywordFile.read().splitlines()
	for line in lines:
		keywords.append(line)

for date, handle, ID, name in itertools.izip(dates, handles, eventIDs, names):
	event_date = parser.parse(date)

	start_date = (event_date - timedelta(days=days_before)).strftime("%Y-%m-%d")
	end_date = (event_date + timedelta(days=days_after)).strftime("%Y-%m-%d")

	print handle + ":"
	print "Event Date: ", event_date
	print "Start Date: ", start_date
	print "End Date: ", end_date

	tweetCriteria = got.manager.TweetCriteria().setSince(start_date).setUntil(end_date)


	#build tweet query
	query = ''
	#add company name queries
	for keyword in keywords:
		query = query + name + ' AND ' + keyword +' OR '
	#add company handle queries
	for keyword in keywords:
		query = query + handle + ' AND ' + keyword +' OR '

	#get rid of OR at end
	query = query[:-3]
	#turn it into a list
	queries = query.split(' OR ')

	# for q in queries:
	# 	print q

	#First scrape for company name
	# keywordCriteria = tweetCriteria.setQuerySearch()
	# tweets = got.manager.TweetManager.getTweets(keywordCriteria)
	# print "added name tweets"

	#loop through queries and collect tweets for each
	ids = set()
	noDupTweets = []
	for q in queries:
		print 'Query: '+ q
		keywordCriteria = tweetCriteria.setQuerySearch(q)
		tweets = got.manager.TweetManager.getTweets(keywordCriteria)
		print 'Total tweets this query: ' + str(len(tweets))
		#remove duplicates
		for tweet in tweets:
			if not tweet.id in ids:
				ids.add(tweet.id)
				noDupTweets.append(tweet)

	print "Total Tweets: ", len(noDupTweets)
	filename = str(ID) + "_" + handle + "_keywords" + ".csv"

	with open(filename, "w") as output:
	    writer = csv.writer(output, delimiter=',')
	    for t in noDupTweets:
	        row = t.date, t.text, t.retweets, t.favorites, t.mentions, t.hashtags, t.id
	        writer.writerow([unicode(s).encode("utf-8") for s in row])
