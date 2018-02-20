
# coding: utf-8

# In[1]:

#Import pandas for table manipulation
import pandas as pd
import datetime
from datetime import timedelta

#Read in the stockReturn data as stockTable
stockTable = pd.read_csv('stockReturn.csv')
#Read in the dataBreach data as dataBreaches
dataBreaches = pd.read_csv('dataBreachesActive.csv')


# In[2]:

#Add columns to store calculated start and end dates
datesFrame = dataBreaches[['EventId', 'Ticker', 'Date Made Public', 'Name']].copy()
datesFrame['StartDate'] = ''
datesFrame['EndDate'] = ''


# In[ ]:

#Add start and end dates to every eventID
for index, row in datesFrame.iterrows():
    #Get the date the breach was made public
    tempDate = datetime.datetime.strptime(row['Date Made Public'], '%x')
    #Calculate 120 days before that date
    start = tempDate-timedelta(days=120)
    #Calculate 30 days after that date
    end = tempDate+timedelta(days=30)
    #Store these values in datesFrame
    datesFrame.set_value(index, 'StartDate', start)
    datesFrame.set_value(index, 'EndDate', end)


# In[ ]:

#Remove the row with column headers from stockTable
stockTable = stockTable[1:]
#Convert the dates in stockTable to datetime format
stockTable['formattedDate'] = pd.to_datetime(stockTable['formattedDate'])
for index, row in datesFrame.iterrows():
    print("Filtering: " + str(row['Name']))
    #Get the current company's rows from stockTable
    tempStock = stockTable[stockTable.TICKER == row.Ticker]
    #Filter the current company's rows to the dates we care about
    tempStock = tempStock[(tempStock.formattedDate>=row['StartDate'])&(tempStock.formattedDate<=row['EndDate'])]
    #Create an EventId column in the new table
    tempStock['EventId'] = row['EventId']
    #Rename the old stock columns
    tempStock.columns = ['PERMNO', 'oldDate', 'Ticker', 'Name', 'Price', 'Date', 'EventId']
    #Pull out only the columsn we care about
    tempStock = tempStock[['EventId', 'Date', 'Ticker', 'Name', 'Price']]
    #Convert this to a new dataFrame
    result = pd.DataFrame(tempStock)
    #Remove / values that would mess with directories
    if(type(row.Name)!=float):
        tempRowName = row.Name.replace('/', '')
    fileName = "csvs/" + str(row.EventId) + "_" + str(tempRowName) + ".csv"
    #Export to a unique csv
    result.to_csv(fileName)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



