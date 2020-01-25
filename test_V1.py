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
df = pd.read_csv('data/4hMFE.csv',skipinitialspace=True, usecols = cols)
df=df.tail(78)
df.reset_index(drop=False,inplace=True )

# data
x = df.index
y = df['High']

# Find the slope and intercept of the best fit line
slope, intercept = np.polyfit(x, y, 1)

#Find the slops and plce them into new columns
df['std_Deviation'] = [slope * i + intercept for i in x]

#Do some calculation to determine upper and lower extremes

_hdh = (df['High'] - df['std_Deviation']).max()        
_hdl = (df['std_Deviation']-df['Low']).max()

#Put the slope into the dataframe
df['Slope_Upper'] = [(slope * i + intercept)+_hdh for i in x]
df['Slope_Lower'] = [(slope * i + intercept)-_hdl for i in x]
    
#Set the main figure proportions
fig = plt.figure(figsize=(20,10))
fig.subplots_adjust(hspace=0.3)
ax1 = fig.add_subplot(111)

# Plot the best fit line over the actual values
ax1.scatter(x, y, marker='.')
plt.scatter(x, y)
plt.plot(x, df['std_Deviation'], 'r')
plt.plot(x, df['Slope_Upper'], 'g')
plt.plot(x, df['Slope_Lower'], 'b')
plt.title(slope)
plt.show()



