# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:28:13 2020

@author: grant
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#How to create a random array
#df = pd.DataFrame(np.random.randint(0,20,size=(20, 2)), columns=list('AB'))
cols=['Date', 'Time', 'Open','High','Low','Last']
dfd = pd.read_csv('data/4hMFE.csv',skipinitialspace=True, usecols = cols)
dfd=dfd.tail(78)
#dfd['Slope_Upper']=np.nan
#dfd.reset_index(inplace=True)

# data
x = dfd.index
y = dfd['High']

# Find the slope and intercept of the best fit line
slope, intercept = np.polyfit(x, y, 1)

#Find the slops and plce them into new columns
dfd['std_Deviation'] = [slope * i + intercept for i in x]
dfd['Slope_Upper'] = [(slope * i + intercept)+0.005 for i in x]
dfd['Slope_Lower'] = [(slope * i + intercept)-0.005 for i in x]
    

#Set the main figure proportions
fig = plt.figure(figsize=(20,10))
fig.subplots_adjust(hspace=0.3)
ax1 = fig.add_subplot(111)

# Plot the best fit line over the actual values
ax1.scatter(x, y, marker='.')
plt.scatter(x, y)
plt.plot(x, dfd['std_Deviation'], 'r')
plt.plot(x, dfd['Slope_Upper'], 'g')
plt.plot(x, dfd['Slope_Lower'], 'b')
plt.title(slope)
plt.show()



