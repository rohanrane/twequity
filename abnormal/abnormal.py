
# coding: utf-8

# In[3]:


import pandas as pd

#Read in the data to a dataFrame
data = pd.read_csv("-3to3.csv")


# In[4]:


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
out.to_csv("abnormalDif.csv")


# In[5]:


import numpy
import matplotlib.pyplot
table = pd.read_csv('abnormalDif.csv')
mean = numpy.mean(table["diff"])
stdDev = numpy.std(table["diff"])
bottom = [x for x in table["diff"] if (x < mean - 2.5 * stdDev)]
top = [x for x in table["diff"] if (x > mean + 2.5 * stdDev)]
table["Z"] = [(x-mean)/stdDev for x in table["diff"]]


# In[16]:


bottom6 = table.sort_values("Z")[0:len(bottom)]
bottom6


# In[13]:


top7 = table.sort_values("Z",ascending=False)[0:len(top)]
top7


# In[348]:


HPY_user = pd.read_csv("4_HeartlandHPY_user.csv")
HPY_user= HPY_user[:len(HPY_user)-1]
FRP_user = pd.read_csv("101_Fairpoint_user.csv")
SHLD_company = pd.read_csv("160_searsholdings.csv")
SHLD_user = pd.read_csv("160_searsholdings_keywords.csv")
TWTR_company = pd.read_csv("632_twitter.csv")
TWTR_user = pd.read_csv("632_twitter_keywords.csv")
DYN_company = pd.read_csv("647_Dyn_company.csv")
DYN_user = pd.read_csv("647_Dyn_user.csv")
DYN_user= DYN_user[:len(DYN_user)-1]
PRAN_company = pd.read_csv("665_prAna.csv")
PRAN_user = pd.read_csv("665_prAna_keywords.csv")
EFX_user= pd.read_csv("690_equifax_user.csv")
EFX_sentiment_user = pd.read_csv("690_equifax_user_sentiment_250.csv")
EFX_company = pd.read_csv("690_Equifax_company.csv")
RAD_company = pd.read_csv("699_riteaid.csv")
RAD_user = pd.read_csv("699_riteaid_keywords.csv")


# In[355]:


columns=["Date","Ticker","Diff","TotalFollowers","TotalFollowing", "VerifiedUsers","TotalNeg","TotalPos","TotalNegPercent","TotalPosPercent","TotalLinkCount"]
UserAnalysis = pd.DataFrame(columns=columns)
row = [bottom6.iloc[2]["evtdate"],bottom6.iloc[2]["ticker"],bottom6.iloc[2]["diff"],sum([int(x.replace(",","")) for x in HPY_user["Followers"]]), sum([int(x.replace(",","")) for x in HPY_user["Following"]]), sum([int(x) for x in HPY_user["Verified"]]), sum([1 for x in HPY_user["Sent"] if x == "neg"]),sum([1 for x in HPY_user["Sent"] if x == "pos"]), sum([float(x) for x in HPY_user["neg"]])/len(HPY_user), sum([float(x) for x in HPY_user["pos"]])/len(HPY_user),int(sum([x for x in HPY_user["LinkCount"]]))]
UserAnalysis.loc[len(UserAnalysis)] = row
row = [bottom6.iloc[0]["evtdate"],bottom6.iloc[0]["ticker"],bottom6.iloc[0]["diff"],sum([int(x.replace(",","")) for x in FRP_user["Followers"]]), sum([int(x.replace(",","")) for x in FRP_user["Following"]]), sum([int(x) for x in FRP_user["Verified"]]), sum([1 for x in FRP_user["Sent"] if x == "neg"]),sum([1 for x in FRP_user["Sent"] if x == "pos"]), sum([float(x) for x in FRP_user["neg"]])/len(FRP_user), sum([float(x) for x in FRP_user["pos"]])/len(FRP_user),int(sum([x for x in FRP_user["LinkCount"]]))]
UserAnalysis.loc[len(UserAnalysis)] = row
row = [top7.iloc[0]["evtdate"],top7.iloc[0]["ticker"],top7.iloc[0]["diff"],sum([int(x) for x in SHLD_user["Followers"]]), sum([int(x) for x in SHLD_user["Following"]]), sum([int(x) for x in SHLD_user["Verified"]]), sum([1 for x in SHLD_user["Sent"] if x == "neg"]),sum([1 for x in SHLD_user["Sent"] if x == "pos"]), sum([float(x) for x in SHLD_user["neg"]])/len(SHLD_user), sum([float(x) for x in SHLD_user["pos"]])/len(SHLD_user),int(sum([x for x in SHLD_user["LinkCount"]]))]
UserAnalysis.loc[len(UserAnalysis)] = row
row = [top7.iloc[4]["evtdate"],top7.iloc[4]["ticker"],top7.iloc[4]["diff"],sum([int(x) for x in TWTR_user["Followers"]]), sum([int(x) for x in TWTR_user["Following"]]), sum([int(x) for x in TWTR_user["Verified"]]), sum([1 for x in TWTR_user["Sent"] if x == "neg"]),sum([1 for x in TWTR_user["Sent"] if x == "pos"]), sum([float(x) for x in TWTR_user["neg"]])/len(TWTR_user), sum([float(x) for x in TWTR_user["pos"]])/len(TWTR_user),int(sum([x for x in TWTR_user["LinkCount"]]))]
UserAnalysis.loc[len(UserAnalysis)] = row
row = [bottom6.iloc[5]["evtdate"],bottom6.iloc[5]["ticker"],bottom6.iloc[5]["diff"],sum([int(x.replace(",","")) for x in DYN_user["Followers"] if type(x) != float]), sum([int(x.replace(",","")) for x in DYN_user["Following"] if type(x) != float]), sum([float(x) for x in DYN_user["Verified"]]), sum([1 for x in DYN_user["Sent"] if x == "neg"]),sum([1 for x in DYN_user["Sent"] if x == "pos"]), sum([0 if math.isnan(x) else float(x) for x in DYN_user["neg"]])/len(DYN_user), sum([0 if math.isnan(x) else float(x) for x in DYN_user["pos"]])/len(DYN_user),sum([int(x) if x == 1.0 else 0 for x in DYN_user["LinkCount"]])]
UserAnalysis.loc[len(UserAnalysis)] = row
row = [top7.iloc[5]["evtdate"],top7.iloc[5]["ticker"],top7.iloc[5]["diff"],sum([int(x) for x in PRAN_user["Followers"]]), sum([int(x) for x in PRAN_user["Following"]]), sum([int(x) for x in PRAN_user["Verified"]]), sum([1 for x in PRAN_user["Sent"] if x == "neg"]),sum([1 for x in PRAN_user["Sent"] if x == "pos"]), sum([float(x) for x in PRAN_user["neg"]])/len(PRAN_user), sum([float(x) for x in PRAN_user["pos"]])/len(PRAN_user),int(sum([x for x in PRAN_user["LinkCount"]]))]
UserAnalysis.loc[len(UserAnalysis)] = row
row = [bottom6.iloc[4]["evtdate"],bottom6.iloc[4]["ticker"],bottom6.iloc[4]["diff"],sum([int(x.replace(",","")) for x in EFX_user["Followers"] if type(x) != float]), sum([int(x.replace(",","")) for x in EFX_user["Following"] if type(x) != float]), sum([int(x) if x == 1.0 else 0 for x in EFX_user["Verified"]]), sum([1 for x in EFX_sentiment_user["Sent"] if x == "neg"]),sum([1 for x in EFX_sentiment_user["Sent"] if x == "pos"]), sum([float(x) for x in EFX_sentiment_user["neg"]])/len(EFX_sentiment_user), sum([float(x) for x in EFX_sentiment_user["pos"]])/len(EFX_sentiment_user),sum([int(x) if x == 1.0 else 0 for x in EFX_user["LinkCount"]])]
UserAnalysis.loc[len(UserAnalysis)] = row
row = [top7.iloc[1]["evtdate"],top7.iloc[1]["ticker"],top7.iloc[1]["diff"],0, 0, sum([int(x) if x == 1.0 else 0 for x in RAD_user["Verified"]]), sum([1 for x in RAD_user["Sent"] if x == "neg"]),sum([1 for x in RAD_user["Sent"] if x == "pos"]), sum([float(x) for x in RAD_user["neg"]])/len(RAD_user), sum([float(x) for x in RAD_user["pos"]])/len(RAD_user),sum([int(x) if x == 1.0 else 0 for x in RAD_user["LinkCount"]])]
UserAnalysis.loc[len(UserAnalysis)] = row


# In[356]:


UserAnalysis


# In[303]:


row = [top7.iloc[0]["evtdate"],top7.iloc[0]["ticker"], sum([int(x) if x == 1.0 else 0 for x in SHLD_company["LinkCount"]]),sum([1 if x == "Reply" else 0 for x in SHLD_company["Type"]]),sum([1 if x == "Announcement" else 0 for x in SHLD_company["Type"]])]
row


# In[331]:


columns=["Date","Ticker","Diff","TotalLinkCount","NumReplies", "NumAnnouncements","TotalTweets"]
CompanyAnalysis = pd.DataFrame(columns=columns)
row = [top7.iloc[0]["evtdate"],top7.iloc[0]["ticker"],top7.iloc[0]["diff"], sum([int(x) if x == 1.0 else 0 for x in SHLD_company["LinkCount"]]),sum([1 if x == "Reply" else 0 for x in SHLD_company["Type"]]),sum([1 if x == "Announcement" else 0 for x in SHLD_company["Type"]]),len(SHLD_company)]
CompanyAnalysis.loc[len(CompanyAnalysis)] = row
row = [top7.iloc[4]["evtdate"],top7.iloc[4]["ticker"],top7.iloc[4]["diff"], sum([int(x) if x == 1.0 else 0 for x in TWTR_company["LinkCount"]]),sum([1 if x == "Reply" else 0 for x in TWTR_company["Type"]]),sum([1 if x == "Announcement" else 0 for x in TWTR_company["Type"]]),len(TWTR_company)]
CompanyAnalysis.loc[len(CompanyAnalysis)] = row
row = [bottom6.iloc[5]["evtdate"],bottom6.iloc[5]["ticker"], bottom6.iloc[5]["diff"],sum([int(x) if x == 1.0 else 0 for x in DYN_company["LinkCount"]]),sum([1 if x == "Reply" else 0 for x in DYN_company["Type"]]),sum([1 if x == "Announcement" else 0 for x in DYN_company["Type"]]),len(DYN_company)]
CompanyAnalysis.loc[len(CompanyAnalysis)] = row
row = [top7.iloc[5]["evtdate"],top7.iloc[5]["ticker"], top7.iloc[5]["diff"],sum([int(x) if x == 1.0 else 0 for x in PRAN_company["LinkCount"]]),sum([1 if x == "Reply" else 0 for x in PRAN_company["Type"]]),sum([1 if x == "Announcement" else 0 for x in PRAN_company["Type"]]),len(PRAN_company)]
CompanyAnalysis.loc[len(CompanyAnalysis)] = row
row = [bottom6.iloc[4]["evtdate"],bottom6.iloc[4]["ticker"], bottom6.iloc[4]["diff"],sum([int(x) if x == 1.0 else 0 for x in EFX_company["LinkCount"]]),sum([1 if x == "Reply" else 0 for x in EFX_company["Type"]]),sum([1 if x == "Announcement" else 0 for x in EFX_company["Type"]]),len(EFX_company)]
CompanyAnalysis.loc[len(CompanyAnalysis)] = row
row = [top7.iloc[1]["evtdate"],top7.iloc[1]["ticker"], top7.iloc[1]["diff"],sum([int(x) if x == 1.0 else 0 for x in RAD_company["LinkCount"]]),sum([1 if x == "Reply" else 0 for x in RAD_company["Type"]]),sum([1 if x == "Announcement" else 0 for x in RAD_company["Type"]]),len(RAD_company)]
CompanyAnalysis.loc[len(CompanyAnalysis)] = row


# In[332]:


CompanyAnalysis


# In[373]:


get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
plot = plt.scatter(x = CompanyAnalysis["NumReplies"]/CompanyAnalysis["TotalTweets"], y = CompanyAnalysis["Diff"], linewidths=2, c="g")
plt.title("Ratio of Replies to Total Company Tweets vs Stock Difference")
plt.xlabel("Ratio of Replies to Total Company Tweets ")
plt.ylabel("Stock Difference")
plot.figure.show()
#This makes a non-interactive image


# In[367]:


get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
plot = plt.scatter(x = UserAnalysis["TotalNegPercent"], y = UserAnalysis["Diff"], linewidths=2, c="r",marker="*")
plt.title("User Negative Sentiment vs Stock Difference")
plt.xlabel("Negative Sentiment")
plt.ylabel("Stock Difference")
plot.figure.show()


# In[371]:


get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
plot = plt.scatter(x = UserAnalysis["TotalNeg"], y = UserAnalysis["Diff"], linewidths=2, c="r",marker="*")
plt.title("User Negative Sentiment vs Stock Difference")
plt.xlabel("Negative Sentiment")
plt.ylabel("Stock Difference")
plot.figure.show()

