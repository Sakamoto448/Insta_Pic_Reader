import numpy as np
import pandas as pd

def addtolist(list,excel, database):
    for x in range(len(excel)):
        list.append(excel.loc[x, "Follower"])
        New_Followers[x][0] = excel.loc[x, "Follower"]
        New_Followers[x][1] = excel.loc[x, "EDIT Follower"]

New_Followers = np.empty([1000,2], dtype=object) #Followers, edit Followers

Followers = []
Prev_Data = pd.read_csv("PSJA Followers List.csv")
New_Data = pd.read_csv("Instagram Followers 10_25_22 .csv")

# Formats Data To be manipulated
addtolist(Followers, Prev_Data, New_Followers)

index = len(Prev_Data)
dup = index
for x in range(len(New_Data)):
    # Name is on followers list
    if str(New_Data.loc[x, "Follower"]) in Followers:
        cindex = Followers.index(New_Data.loc[x, "Follower"])
        New_Data.loc[x, "Follower"] = Prev_Data.loc[cindex, "EDIT Follower"]
    else:
        # Not on followers list, (add to the list)
        New_Followers[index][0] = New_Data.loc[x,"Follower"]
        index += 1

# Cleans Duplicated Cleans
original = [row[0] for row in New_Followers]
edit = [row[1] for row in New_Followers]
for i in range(dup, index):
    if original[i] in edit:
        original[i] = None

New_Followers= np.column_stack((original,edit))

df = pd.DataFrame(data=New_Data)
df.to_csv("Instagram Followers 10_25_22 .csv", index=False)

df = pd.DataFrame(data=New_Followers,columns=["Follower", "EDIT Follower"])
df.to_csv("PSJA Followers List.csv", index=False)
