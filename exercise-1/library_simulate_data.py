from random import randrange
from random import choices
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def populationID(number):
    "Generates the population of user ID's. I choose users of the type <<abcdX>>, were X is a letter and abcd are 4 integer numbers"
    idPopulation = []
    letters = ["A", "B", "C", "D", "E"]
    while len(idPopulation) < number:
        idnum = str(randrange(0, 9999)).zfill(4) + str(choices(letters, k=1))
        idele = cleanString(idnum)
        if idele not in idPopulation:
            idPopulation.append(idele)
    return idPopulation

def populationSignUpTimeStamp(idPopulation):
    "Generates a population of sign up time stamps for each ID"
    sgnUpPopulation = []
    for idEl in idPopulation:
        seconds = cleanString(str(randrange(0, 60)).zfill(2))
        minutes = cleanString(str(randrange(0, 60)).zfill(2))
        hour = cleanString(str(randrange(0, 23)).zfill(2))
        year = '2018'# cleanString(str(randrange(2018, 2019)))
        month = cleanString(str(randrange(1, 5)).zfill(2))
        if month in ["01", "03", "05", "07", "08", "10", "12"]:
            day = cleanString(str(randrange(1, 31)).zfill(2))
        elif month == "02":
            if int(year) % 4 == 0:
                day = cleanString(str(randrange(1, 29)).zfill(2))
            else:
                day = cleanString(str(randrange(1, 28)).zfill(2))
        else:
            day = cleanString(str(randrange(1, 30)).zfill(2))
        sgnUp = year + "-" + month + "-" + day + " " + hour + ":" + minutes + ":" + seconds
        sgnUpPopulation.append(sgnUp)
    return sgnUpPopulation

def cleanString(str1):
    str1 = str1.replace("[", "")
    str1 = str1.replace("]", "")
    str1 = str1.replace("'", "")
    return str1

def populationOrderID(number, idPopulation):
    sampleIDs = choices(idPopulation, k=number)
    return sampleIDs

def populationOrderTimeStamp(sampleIDs, sgnUpPopulation, idPopulation):
    # we create a dictionary which relates a given ID with its sign up date
    dicIDSgUp = {}
    i = 0
    for key in idPopulation:
        dicIDSgUp[key] = sgnUpPopulation[i]
        i = i + 1

    sampleOrderTimeStamp = []
    for ID in sampleIDs:
        #for each ID in the sample we sum a random number of days equivalent to 1 and 20 weeks
        sudate = dicIDSgUp[ID]
        pop = np.arange(0, 35, 1).tolist()
        wgh = np.arange(3500, 0, -100).tolist()
        day = choices(pop, wgh, k=1)
        newdate = sumdays(sudate[0:10], day[0])+sudate[10:]
        sampleOrderTimeStamp.append(newdate)
    return sampleOrderTimeStamp

def sumdays(indate, ndays):
    enddate = str(pd.to_datetime(indate) + pd.DateOffset(days=ndays))
    enddate = enddate[0:10]
    return enddate


def histOrderID(idPopulation):
    countID = Counter(idPopulation)
    n = countID
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=idPopulation, bins=19, color='#0504aa',
                            alpha=0.7, rwidth=0.5, align='mid')
    plt.xticks(rotation='vertical')
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('ID')
    plt.ylabel('Frequency')
    plt.title('Histogram of number the of orders of each ID')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.show()