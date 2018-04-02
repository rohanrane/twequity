import numpy
from numpy import nan
import pandas 
import matplotlib.pyplot
import glob
path = "*.csv"

for fname in glob.glob(path):
    table = pandas.read_csv(fname, header=None)
    table[len(table.columns)] = ["Announcement" if x is nan else "Reply" for x in table[4]]
    table.to_csv(fname)