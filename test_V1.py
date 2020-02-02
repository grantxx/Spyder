# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:28:13 2020

@author: grant
"""
from alpha_vantage.foreignexchange import ForeignExchange
cc = ForeignExchange(key='OGRPFV5D58LC77OL',output_format='pandas')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# This is for alphavnatage data:
dfm = pd.DataFrame()
dfw = pd.DataFrame()
dfd = pd.DataFrame()

def clean_Columns(df):
    if 'errorslope' not in df.columns:
        df.reset_index(inplace=True) #reset index to get timestamp out
        df.columns = ['date','open','high','low','close'] #Make sure column names are legit  
        df['index'] = np.arange(len(df)) #create an index 
        #df['hilow_median'] = df[['high', 'low']].median(axis=1)
    return df

if dfm.empty:
    dfm, meta_data = cc.get_currency_exchange_monthly(from_symbol='EUR',to_symbol='USD', outputsize='full')
    clean_Columns(dfm)
    dfm = dfm.tail(12)

if dfw.empty:
    dfw, meta_data = cc.get_currency_exchange_weekly(from_symbol='EUR',to_symbol='USD', outputsize='full') 
    clean_Columns(dfw)
    dfw = dfw.tail(24)
    
if dfd.empty:
   dfd, meta_data = cc.get_currency_exchange_daily(from_symbol='EUR',to_symbol='USD', outputsize='full')
   clean_Columns(dfd)
   dfd = dfd.tail(90)


#How to create a random array
#df = pd.DataFrame(np.random.randint(0,20,size=(20, 2)), columns=list('AB'))
cols=['Date', 'Time', 'Open','High','Low','Last']
df = pd.read_csv('data/4hMFE.csv',skipinitialspace=True, usecols = cols)
df=df.tail(78)
df.reset_index(drop=False,inplace=True )

#%% end of cell begining of new
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

y5= df['std_Deviation']
y6=df['Slope_Upper']
y7=df['Slope_Lower']
y8=df['Slope_Lower']+(df['SLU_Min'].max()/3)
y9=df['Slope_Upper']-(df['SLU_Max'].max()/3)

_lower_quartile = len(x2[x2.Low <= x2.Slope_Lower+(df['SLU_Min'].max()/3)])
_upper_quartile = len(x1[x1.High >= x1['Slope_Upper']-(x1['SLU_Max'].max()/3)].index)
_total_record_count = len(df.index)

#%% end of cell begining of new

#Set the main figure proportions
fig = plt.figure(figsize=(40,20))
fig.subplots_adjust(hspace=0.3)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)


# Plot the best fit line over the actual values
#ax1.scatter(x, y, marker='.')
ax1.scatter(x1.index, x1['High'], marker='.') #Plot only highs above std deviation line
ax1.scatter(x2.index, x2['Low'], marker='.')#Plot only Lows below std deviation line
ax1.plot(x, y5, 'r--')
ax1.plot(x, y6, 'g')
ax1.plot(x, y7, 'b')
ax1.plot(x, y8, 'b--')
ax1.plot(x, y9, 'b--')
ax1.fill_between(x, y7,y8,color='lightslategrey',alpha=.55)
ax1.fill_between(x, y6,y9,color='burlywood',alpha=.5)
ax1.set_title('4 hour',fontsize=30)
ax1.text(0.7, 0.96,'Total count: ' + str(_total_record_count),fontsize=20, ha='left', va='center',transform=ax1.transAxes)
ax1.text(0.7, 0.9,'Upper quartile count: ' + str(_upper_quartile),fontsize=20, ha='left', va='center',transform=ax1.transAxes)
ax1.text(0.7, 0.84,'Lower quartile count: ' + str(_lower_quartile),fontsize=20, ha='left', va='center',transform=ax1.transAxes)

ax2.scatter(dfm.index, dfm['high'])
ax2.set_title('Month',fontsize=30)
ax3.scatter(dfw.index, dfw['high'])
ax3.set_title('Weekly', fontsize=30)
ax4.scatter(dfd.index, dfd['high'])
ax4.set_title('Daily',fontsize=30)
plt.show()


