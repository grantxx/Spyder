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

#Find the slopes and plce them into new columns
df['std_Deviation'] = [slope * i + intercept for i in x]
df['SLU_Max'] = (df['High'] - df['std_Deviation'])
df['SLU_Min'] = (df['std_Deviation']-df['Low'])
#Put the slope into the dataframe
df['Slope_Upper'] = [(slope * i + intercept)+((df['High'] - df['std_Deviation']).max()) for i in x]
df['Slope_Lower'] = [(slope * i + intercept)-(df['SLU_Min'].max()) for i in x]

    
#Get data of only highs above deviation and low below deviation
x1=df.loc[df['High'] >= df['std_Deviation']].copy()
x2=df.loc[df['Low'] < df['std_Deviation']]

#Set the main figure proportions
fig = plt.figure(figsize=(20,10))
fig.subplots_adjust(hspace=0.3)
ax1 = fig.add_subplot(111)

y5= df['std_Deviation']
y6=df['Slope_Upper']
y7=df['Slope_Lower']
y8=df['Slope_Lower']+(df['SLU_Min'].max()/3)
y9=df['Slope_Upper']-(df['SLU_Max'].max()/3)

# Plot the best fit line over the actual values
#ax1.scatter(x, y, marker='.')
ax1.scatter(x1.index, x1['High'], marker='.') #Plot only highs above std deviation line
ax1.scatter(x2.index, x2['Low'], marker='.')#Plot only Lows below std deviation line
plt.plot(x, y5, 'r--')
plt.plot(x, y6, 'g')
plt.plot(x, y7, 'b')
plt.plot(x, y8, 'b--')
plt.plot(x, y9, 'b--')
plt.fill_between(x, y7,y8,color='lightslategrey',alpha=.55)
plt.fill_between(x, y6,y9,color='burlywood',alpha=.5)
plt.title('Linear Regression')
plt.show()


