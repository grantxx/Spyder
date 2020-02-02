# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:28:13 2020

@author: grant
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

counter_i = 1

def Create_Plot(df):
    x = df.index
    y = df['Mid']
    
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
    
    
    #Set the main figure proportions
    fig = plt.figure(figsize=(40,20))
    fig.subplots_adjust(hspace=0.3)
    ax = fig.add_subplot(221)  

    
    
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
    ax.set_title('Weekly',fontsize=30)
    ax.text(0.7, 0.96,'Total count: ' + str(_total_record_count),fontsize=20, ha='left', va='center',transform=ax.transAxes)
    ax.text(0.7, 0.9,'Upper quartile count: ' + str(_upper_quartile),fontsize=20, ha='left', va='center',transform=ax.transAxes)
    ax.text(0.7, 0.84,'Lower quartile count: ' + str(_lower_quartile),fontsize=20, ha='left', va='center',transform=ax.transAxes)
    
    # ax2.scatter(dfm.index, dfm['high'])
    # ax2.set_title('Month',fontsize=30)
    # ax3.scatter(dfw.index, dfw['high'])
    # ax3.set_title('Weekly', fontsize=30)
    # ax4.scatter(dfd.index, dfd['high'])
    # ax4.set_title('Daily',fontsize=30)
    plt.show()    

cols=['Date', 'Time', 'Open','High','Low','Last']

dfd = pd.read_csv('C:/SierraChart/Data/ed.txt',skipinitialspace=True, usecols=cols)
dfd = dfd.tail(100)
dfd.reset_index(inplace=True)
dfd['Mid'] = (dfd['High'] + dfd['Low'])/2


dfw = pd.read_csv('C:/SierraChart/Data/euw.txt',skipinitialspace=True, usecols=cols)
dfw = dfw.tail(50)   
dfw.reset_index(inplace=True)
dfw['Mid'] = (dfw['High'] + dfw['Low'])/2

DF_List = [dfw,dfd]


for i in DF_List: 
    Create_Plot(i) 
    counter_i += 1
    



