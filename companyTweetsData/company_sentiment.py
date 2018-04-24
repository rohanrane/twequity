import sys
import csv
import itertools
import re
import glob
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

for fname in glob.glob('*.csv'):
    table = pd.read_csv(fname)
    count = 0
    table[len(table.columns)] = ""
    table[len(table.columns)] = ""
    table[len(table.columns)] = ""
    for index in table.iterrows():
        string = table.ix[count,2]
        if type(string) is str:
            analysis = TextBlob(clean_tweet(string), analyzer=NaiveBayesAnalyzer())
            table.ix[count,len(table.columns)-3] = analysis.sentiment.classification
            table.ix[count,len(table.columns)-2] = analysis.sentiment.p_pos
            table.ix[count,len(table.columns)-1] = analysis.sentiment.p_neg
        count = count + 1
table.to_csv(fname, index=False, header=False)
