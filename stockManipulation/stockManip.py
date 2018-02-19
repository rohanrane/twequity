#Import pandas for table manipulation
import pandas

#Read in the stockReturn data as stockTable
stockTable = pandas.read_csv('stockReturn.csv')
#Read in the dataBreach data as dataBreaches
dataBreaches = pandas.read_csv('dataBreachesActive.csv')

print(dataBreaches[['EventId', 'Date Made Public']])
