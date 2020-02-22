from library_simulate_data import *
import pandas as pd
from pandas import DataFrame
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

print('Running program... \n')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# We generate the table of ID's and sign up time stamps
pop_ID = populationID(600)# generates a population of nonrepeated IDs
pop_SgnUp_TS = populationSignUpTimeStamp(pop_ID)# generates a sign up time stamp of format YYYY:MM:DD:hh:mm:ss

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# We store the table in a dataframe
list_cols_SignUp = ['user_id', 'signup_timestamp'] # the column names
table_SignUp = {list_cols_SignUp[0]: pop_ID, list_cols_SignUp[1]: pop_SgnUp_TS}
dfSignUp = DataFrame(table_SignUp, columns=list_cols_SignUp)
# let us see a few rows
print('\nLet us see a few rows of the <<Signup>> table:\n')
print(dfSignUp.head(10))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Now we create a table with the columns ID's and order time stamps
#    (*) note that time stamps of each ID have been generated on dates later or = to sign up date
pop_Order_ID = populationOrderID(1200, pop_ID)
pop_Order_TS = populationOrderTimeStamp(pop_Order_ID, pop_SgnUp_TS, pop_ID)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# We store the table in a dataframe
list_cols_Order = ['user_id', 'order_timestamp'] # the column names
table_Order = {list_cols_Order[0]: pop_Order_ID, list_cols_Order[1]: pop_Order_TS}
dfOrder = DataFrame(table_Order, columns=list_cols_Order)

# let us see a few rows
print('\nLet us see a few rows of the <<Orders>> table:\n')
print(dfOrder.head(10))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Now we create the cohort of Signup to First Order

# STRATEGY:
# First of all, I set a date in which weeks will start counting
init_date = "2018-01-01"
end_date = "2019-01-01"
the_year = pd.Timestamp(init_date).year

# In table Orders, for each ID I add a column with the time stamp of the sign up
df = dfOrder # create a new table from the Orders table
nrows=df.shape[0]
ncols=df.shape[1]
list_sgnupdates = []
for row in range(nrows): # for each row
    dfaux = dfSignUp.loc[dfSignUp['user_id'] == dfOrder.iloc[row, 0]] # I search for the signup date of the ID
    sgdate = dfaux.iloc[0, 1] # get the value
    list_sgnupdates.append(sgdate) # I add an element to the list with the sign up time stamp of the row's ID
df['signup_timestamp'] = list_sgnupdates # add the column to the data frame

# I keep the orders of users which signed up in the year 2018
condition = (df['signup_timestamp'] >= init_date) & (df['signup_timestamp'] < end_date)
df = df.loc[condition]

# I add a column with the week in the year of the order, and the week in the year of the sign up
df['week_signup_timestamp'] = pd.to_datetime(df['signup_timestamp']).dt.week
df['week_order_timestamp'] = pd.to_datetime(df['order_timestamp']).dt.week

print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
      '\nWe add a column to each order with\n' +
      'the signup time stamp of the user in the row.\n' +
      'We further add a column with the week in the\n' +
      'year of each time stamp:\n')
print(df.head(10))

# We order the rows by user_id, keep only the columns with week data and throw away repeated ID's
cols = df.columns.tolist()
cols = [cols[0]] + cols[-1:-3:-1] #+ cols[1:2+1]
df = df[cols]
df = df.sort_values(["user_id", "week_signup_timestamp"], axis=0, ascending=True)
print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
      '\nWe arrange the rows ordered by user id \n' +
      'and by week of order time stamp to keep the first order.\n')
print(df.head(10))

# We keep the first occurrence in user_id to pick up the first order of each user
df = df.drop_duplicates(subset=['user_id'], keep='first')
print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
      '... and keep only first occurrences in user_id. We further  \n' +
      'add a column with the week of first order counting from week\n' +
      'of sign up                                                  \n')
print(df.head(10))

# Now I can create the cohort
rownames = []
colnames = []
maxSUweek = 20#df['week_signup_timestamp'].max()
maxFOweek = 5#df['week_signup_timestamp'].max()
occ_matrix = np.zeros((maxSUweek+1, maxFOweek+1), dtype=np.int32)
for week_sgnUp in range(maxSUweek + 1):
    rownames.append("sign up in week "+str(week_sgnUp))
    colnames.append("first order in week "+str(week_sgnUp))
    for week_FO in range(maxFOweek + 1):
        condition = (df['week_signup_timestamp'] == week_sgnUp) & (df['week_order_timestamp'] == week_FO)
        occ_matrix[week_sgnUp, week_FO] = len(df[condition])
    print(occ_matrix[week_sgnUp, :])




