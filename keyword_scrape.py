import sys
import got
import csv
import itertools
from datetime import datetime, timedelta
from dateutil import parser

dates = []
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
        eventIDs.append(row[0])

with open(sys.argv[2]) as keywordFile:
	lines = keywordFile.read().splitlines()
	for line in lines:
		keywords.append(line)

for date, handle, ID in itertools.izip(dates, handles, eventIDs):
	event_date = parser.parse(date)

	start_date = (event_date - timedelta(days=days_before)).strftime("%Y-%m-%d")
	end_date = (event_date + timedelta(days=days_after)).strftime("%Y-%m-%d")

	print handle + ":"
	print "Event Date: ", event_date
	print "Start Date: ", start_date
	print "End Date: ", end_date

	tweetCriteria = got.manager.TweetCriteria().setUsername(handle).setSince(start_date).setUntil(end_date)

	#reset tweet list for each company
	tweets = []

	#loop through keywords and scrape the tweets
	for keyword in keywords:
		keywordCriteria = tweetCriteria.setQuerySearch(keyword)
		tweets = tweets + got.manager.TweetManager.getTweets(keywordCriteria)

	
	print "Total Tweets(with duplicates): ", len(tweets)

	# Get rid of duplicate tweets
	# Hopefully this isn't too expensive
	ids = set()
	noDupTweets = []
	for tweet in tweets:
		if not tweet.id in ids:
			ids.add(tweet.id)
			noDupTweets.append(tweet)

	print "Total Tweets(without duplicates): ", len(noDupTweets)
	filename = str(ID) + "_" + handle + "_keywords" + ".csv"

	with open(filename, "w") as output:
	        writer = csv.writer(output, delimiter=',')
	        for t in noDupTweets:
	        	row = t.date, t.text, t.retweets, t.favorites, t.mentions, t.hashtags, t.id
	        	writer.writerow([unicode(s).encode("utf-8") for s in row])
