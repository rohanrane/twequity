import sys
import got
import csv
import itertools
from datetime import datetime, timedelta
from dateutil import parser

dates = []
handles = []
eventIDs = []

days_before = 120
days_after = 30

if len(sys.argv) == 1:
	print "Missing input CSV file"
	sys.exit(0)

with open(sys.argv[1]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	date = datetime.strptime(row[3], "%m/%d/%y").strftime("%Y-%m-%d")
        dates.append(date)
        handles.append(row[4])
        eventIDs.append(row[0])


for date, handle, ID in itertools.izip(dates, handles, eventIDs):
	event_date = parser.parse(date)

	start_date = (event_date - timedelta(days=days_before)).strftime("%Y-%m-%d")
	end_date = (event_date + timedelta(days=days_after)).strftime("%Y-%m-%d")

	print handle + ":"
	print "Event Date: ", event_date
	print "Start Date:: ", start_date
	print "End Date: ", end_date

	tweetCriteria = got.manager.TweetCriteria().setUsername(handle).setSince(start_date).setUntil(end_date)
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)

	print "Total Tweets: ", len(tweets)
	filename = str(ID) + "_" + handle + ".csv"

	with open(handle+".csv", "w") as output:
	        writer = csv.writer(output, delimiter=',')
	        for t in tweets:
	        	row = t.date, t.text, t.retweets, t.favorites, t.mentions, t.hashtags
	        	writer.writerow([unicode(s).encode("utf-8") for s in row])
