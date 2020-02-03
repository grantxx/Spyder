# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:28:13 2020

@author: grant
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

counter_i = 1
fig = plt.figure(figsize=(40,20))
fig.subplots_adjust(hspace=0.3)
    
def Create_Plot(df):
    x = df.index
    y = df['Mid']
    
    if counter_i == 1:
        ChartHeader = 'Monthly'
    elif counter_i == 2:
        ChartHeader = 'Weekly'
    elif counter_i == 3:
        ChartHeader = 'Daily'
    elif counter_i == 4:
        ChartHeader = '4 Hour'
    
    # Find the slope and intercept of the best fit line
    slope, intercept = np.polyfit(x, y, 1)
    
    # #Find the slopes and plce them into new columns
    df['std_Deviation'] = [slope * i + intercept for i in x]
    df['SLU_Max'] = (df['High'] - df['std_Deviation'])
    df['SLU_Min'] = (df['std_Deviation']-df['Low'])
    # #Put the slope into the dataframe
    df['Slope_Upper'] = [(slope * i + intercept)+((df['High'] - df['std_Deviation']).max()) for i in x]
    df['Slope_Lower'] = [(slope * i + intercept)-(df['SLU_Min'].max()) for i in x]
    
        
    # #Get data of only highs above deviation and low below deviation
    x1=df.loc[df['High'] >= df['std_Deviation']].copy()
    x2=df.loc[df['Low'] < df['std_Deviation']]
    
    y5= df['std_Deviation']
    y6=df['Slope_Upper']
    y7=df['Slope_Lower']
    y8=df['Slope_Lower']+(df['SLU_Min'].max()/3)
    y9=df['Slope_Upper']-(df['SLU_Max'].max()/3)
    
    _lower_quartile = len(x2[x2.Low <= x2.Slope_Lower+(df['SLU_Min'].max()/3)])
    _upper_quartile = len(x1[x1.High >= x1['Slope_Upper']-(x1['SLU_Max'].max()/3)].index)
    _total_record_count = len(df.index)
    

    ax = fig.add_subplot(2,2,counter_i)  

        
    # Plot the best fit line over the actual values
    #ax1.scatter(x, y, marker='.') #Plot only highs above std deviation line
    ax.plot(x,df['std_Deviation'],'r--')
    ax.plot(x,df['Slope_Upper'],'r--')
    ax.plot(x,df['Slope_Lower'],'r--')
    
    ax.scatter(x1.index, x1['High'], marker='.') #Plot only highs above std deviation line
    ax.scatter(x2.index, x2['Low'], marker='.')#Plot only Lows below std deviation line
    ax.plot(x, y5, 'r--')
    ax.plot(x, y6, 'g')
    ax.plot(x, y7, 'b')
    ax.plot(x, y8, 'b--')
    ax.plot(x, y9, 'b--')
    ax.fill_between(x, y7,y8,color='lightslategrey',alpha=.55)
    ax.fill_between(x, y6,y9,color='burlywood',alpha=.5)
    ax.set_title(ChartHeader,fontsize=30)
    ax.text(0.7, 0.96,'Total count: ' + str(_total_record_count),fontsize=20, ha='left', va='center',transform=ax.transAxes)
    ax.text(0.7, 0.9,'Upper quartile count: ' + str(_upper_quartile),fontsize=20, ha='left', va='center',transform=ax.transAxes)
    ax.text(0.7, 0.84,'Lower quartile count: ' + str(_lower_quartile),fontsize=20, ha='left', va='center',transform=ax.transAxes)
    

cols=['Date', 'Time', 'Open','High','Low','Last']

dfm = pd.read_csv('C:/SierraChart/Data/em.txt',skipinitialspace=True, usecols=cols)
dfm = dfm.tail(17)
dfm.reset_index(inplace=True)
dfm['Mid'] = (dfm['High'] + dfm['Low'])/2


dfw = pd.read_csv('C:/SierraChart/Data/ew.txt',skipinitialspace=True, usecols=cols)
dfw = dfw.tail(50)   
dfw.reset_index(inplace=True)
dfw['Mid'] = (dfw['High'] + dfw['Low'])/2

dfd = pd.read_csv('C:/SierraChart/Data/ed.txt',skipinitialspace=True, usecols=cols)
dfd = dfd.tail(80)   
dfd.reset_index(inplace=True)
dfd['Mid'] = (dfd['High'] + dfd['Low'])/2

df4 = pd.read_csv('C:/SierraChart/Data/e4.txt',skipinitialspace=True, usecols=cols)
df4 = df4.tail(136)   
df4.reset_index(inplace=True)
df4['Mid'] = (df4['High'] + df4['Low'])/2


DF_List = [dfm,dfw, dfd, df4]#Add the dataframes to a list


for i in DF_List: 
    Create_Plot(i) 
    counter_i += 1

plt.show()   
    



