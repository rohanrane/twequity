import glob
import re
import pandas as pd

#Iterates over the CSVs in the current directory, counts number of URLs
#in each tweet, indicates if there are > 0 tweets in one column and counts
#them in the next, by appending to the original CSV. Don't run multiple
#times on the same files, or else you'll end up with duplicate columns

def FindURL(string):
    url = re.findall('http[s]?://[ ]?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url

for fname in glob.glob('*.csv'):
    table = pd.read_csv(fname)
    count = 0
    table[len(table.columns)] = ""
    table[len(table.columns)] = ""
    for index in table.iterrows():
        string = table.ix[count,1]
        listOfURLs = FindURL(string)
        if len(listOfURLs) > 0:
            table.ix[count,len(table.columns)-2] = 1
        else:
            table.ix[count,len(table.columns)-2] = 0
        table.ix[count,len(table.columns)-1] = len(listOfURLs)
        count = count + 1
    table.to_csv(fname, index=False, header=False)
