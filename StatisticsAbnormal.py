
# coding: utf-8

# In[7]:


import numpy 
import pandas 
import matplotlib.pyplot

table = pandas.read_csv('abnormalDif.csv')


# In[10]:


mean = numpy.mean(table["diff"])
stdDev = numpy.std(table["diff"])
stdDev


# In[25]:


bottom = [x for x in table["diff"] if (x < mean - 2.5 * stdDev)]
top = [x for x in table["diff"] if (x > mean + 2.5 * stdDev)]
table["Z"] = [(x-mean)/stdDev for x in table["diff"]]


# In[28]:


table.sort_values("Z")


# In[26]:


matplotlib.pyplot.scatter(table["Z"], table["diff"])

