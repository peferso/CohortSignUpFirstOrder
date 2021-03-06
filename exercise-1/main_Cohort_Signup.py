from library_simulate_data import *
import pandas as pd
from pandas import DataFrame
import numpy as np

number_of_IDs = 600
number_of_Orders = 1200

print('Running program... \n')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# We generate the table of ID's and sign up time stamps
pop_ID = populationID(number_of_IDs)# generates a population of nonrepeated IDs
pop_SgnUp_TS = populationSignUpTimeStamp(pop_ID)# generates a sign up time stamp of format YYYY:MM:DD:hh:mm:ss

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# We store the table in a dataframe
list_cols_SignUp = ['user_id', 'signup_timestamp'] # the column names
table_SignUp = {list_cols_SignUp[0]: pop_ID, list_cols_SignUp[1]: pop_SgnUp_TS}
dfSignUp = DataFrame(table_SignUp, columns=list_cols_SignUp)
# let us see a few rows
print('\nLet us see a few rows of the <<Signup>> table:\n')
print(dfSignUp.head(10))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Now we create a table with the columns ID's and order time stamps
#    (*) note that time stamps of each ID have been generated on dates later or = to sign up date
pop_Order_ID = populationOrderID(number_of_Orders, pop_ID)
pop_Order_TS = populationOrderTimeStamp(pop_Order_ID, pop_SgnUp_TS, pop_ID)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# We store the table in a dataframe
list_cols_Order = ['user_id', 'order_timestamp'] # the column names
table_Order = {list_cols_Order[0]: pop_Order_ID, list_cols_Order[1]: pop_Order_TS}
dfOrder = DataFrame(table_Order, columns=list_cols_Order)

# let us see a few rows
print('\nLet us see a few rows of the <<Orders>> table:\n')
print(dfOrder.head(10))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# script to create the cohort of Signup to First Order

# (*) STRATEGY: add a column to the dataframe dfOrder with the signup timestamp of each ID.
# (*) After that, everything reduces to operating with timestamps and counting occurrences

# First of all, I set a date in which weeks will start counting
init_date = "2018-01-01"
end_date = "2019-01-01"

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
# I also add a column with the difference btw week of order and week of sgnup
df['week_signup_timestamp'] = pd.to_datetime(df['signup_timestamp']).dt.week
df['week_order_timestamp'] = pd.to_datetime(df['order_timestamp']).dt.week
df['week_order_dif'] = df['week_order_timestamp'] - df['week_signup_timestamp']

print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
      '\nWe add a column to each order with\n' +
      'the signup time stamp of the user in the row.\n' +
      'We further add a column with the week in the\n' +
      'year of each time stamp and another with the difference:\n')
print(df.head(10))

# We order the rows by user_id and order_timestamp, keep only the columns with week data
cols = df.columns.tolist()
cols = [cols[0]] + cols[-1:-4:-1] #+ cols[1:2+1]
df = df[cols]
df = df.sort_values(["user_id", "week_order_timestamp"], axis=0, ascending=True)
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
maxSUweek = df['week_signup_timestamp'].max()
maxFOweek = df['week_order_dif'].max()
# matrix of occurrence counting
# indices go to +1 because row 0 will no be used and col 0 will keep total occurrences in row
occ_matrix = np.zeros((maxSUweek+1, maxFOweek+1), dtype=np.single)

# the labels of the cohort
colnames.append('number')
for week_sgnUp in range(1, maxSUweek + 1):
    rownames.append("SU N=" + str(week_sgnUp))
for week_FO in range(maxFOweek):
    colnames.append("FO N+" + str(week_FO)+" [%]")

# we compute the cohort checking number of occurrences for each entry
# and then transforming it to percentage dividing by total number
# of occurrences in each row
for week_sgnUp in range(1, maxSUweek + 1):
    for week_FO in range(1, maxFOweek + 1):
        condition = (df['week_signup_timestamp'] == week_sgnUp) & (df['week_order_dif'] == week_FO - 1)
        occ_matrix[week_sgnUp, week_FO] = len(df[condition])
    rowsum = np.sum(occ_matrix[week_sgnUp, 1:], dtype=np.int32)
    occ_matrix[week_sgnUp, 0] = rowsum
    occ_matrix[week_sgnUp, 1:] = occ_matrix[week_sgnUp, 1:]/rowsum*100.0
    print(np.round(occ_matrix[week_sgnUp, :], 2))

# build the dataframe
dict_cohort = {}
icol = 0
for i in colnames:
    dict_cohort[i] = list(occ_matrix[1:, icol])
    icol = icol + 1

cohort = DataFrame(dict_cohort, columns=colnames, index=rownames)
# we round the entries
cohort = cohort.round(2)
# and include the number of occurrences in each row as an integer
cohort[colnames[0]] = pd.to_numeric(cohort[colnames[0]], downcast='integer')

# we see the result
print(cohort.to_string())
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# export to latex
with open('myCohort.tex', 'w') as op:
    op.write(cohort.to_latex(bold_rows=True,index_names=True))


# check sum of numbers is at most as large as the number of ID's
check = cohort.loc[:, 'number']
check = check.sum()
print('\nThis should be <=', number_of_IDs,'\n')
print(check)

# check sum of percentages
check = cohort
check.drop('number', axis=1, inplace=True)
check = check.sum(axis=1)
print('\nAll the following entries should be close to 100\n')
print(check.to_string())
