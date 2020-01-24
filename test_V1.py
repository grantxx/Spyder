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
#dfd.reset_index(inplace=True)

# Some dummy data
x = dfd.index
y = dfd['High']

# Find the slope and intercept of the best fit line
slope, intercept = np.polyfit(x, y, 1)

# Create a list of values in the best fit line
X_deviation = [slope * i + intercept for i in x]
X_deviation_Upper_band = [(slope * i + intercept)+0.005 for i in x]
X_deviation_lower_band = [(slope * i + intercept)-0.005 for i in x]

# Plot the best fit line over the actual values

#Set the main figure proportions
fig = plt.figure(figsize=(15,10))
fig.subplots_adjust(hspace=0.3)
ax1 = fig.add_subplot(111)

ax1.scatter(x, y, marker='.')

plt.scatter(x, y)
plt.plot(x, X_deviation, 'r')
plt.plot(x, X_deviation_Upper_band, 'g')
plt.plot(x, X_deviation_lower_band, 'b')
plt.title(slope)
plt.show()



