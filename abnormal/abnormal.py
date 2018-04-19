import pandas as pd

#Read in the data to a dataFrame
data = pd.read_csv("-3to3.csv")

#Group by company ticker and evtdate together
groups = data.groupby(["ticker", "evtdate"])
#Create the DataFrame to output to
out = pd.DataFrame(columns = ["ticker", "evtdate", "diff"])
#Use an index to append to the ouptut DataFrame
index = 0
#iterate over the values of the groups
#i contains the ticker/evtdate
#j is a dataframe of the seven days for that event
for i, j in groups:
    sumBefore = 0
    sumAfter = 0
    #Make sure the event has the right number of rows
    if j.shape == (7,4):
        #find the mean of the 3 days before
        sumBefore += float(j.iloc[0,3])
        sumBefore += float(j.iloc[1,3])
        sumBefore += float(j.iloc[2,3])
        meanBefore = sumBefore / 3
        #find the mean of the 3 days after
        sumAfter += float(j.iloc[4,3])
        sumAfter += float(j.iloc[5,3])
        sumAfter += float(j.iloc[6,3])
        meanAfter = sumAfter / 3
    #Find the difference between the means
    diff = meanAfter - meanBefore
    #Append this as a new row with the desired values
    out.loc[index] = [i[0], i[1], diff]
    index= index + 1
#Ouptut to csv
out.to_csv("abnormalDif.csv", index = False)
