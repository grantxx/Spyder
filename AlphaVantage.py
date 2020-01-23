# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%% Get the connection
from alpha_vantage.foreignexchange import ForeignExchange
import matplotlib.pyplot as plt
cc = ForeignExchange(key='OGRPFV5D58LC77OL',output_format='pandas')
import pandas as pd
from datetime import datetime
import numpy as np
from numpy.polynomial.polynomial import polyfit
import statistics

dfm = pd.DataFrame()
dfw = pd.DataFrame()
dfd = pd.DataFrame()

if dfm.empty:
    dfm, meta_data = cc.get_currency_exchange_monthly(from_symbol='EUR',to_symbol='USD', outputsize='full')

if dfw.empty:
    dfw, meta_data = cc.get_currency_exchange_weekly(from_symbol='EUR',to_symbol='USD', outputsize='full')  
    
if dfd.empty:
   dfd, meta_data = cc.get_currency_exchange_daily(from_symbol='EUR',to_symbol='USD', outputsize='full')


df60, meta_data = cc.get_currency_exchange_intraday(from_symbol='EUR',to_symbol='USD',interval='60min', outputsize='full')

def clean_Columns(df):
    if 'errorslope' not in df.columns:
        df.reset_index(inplace=True) #reset index to get timestamp out
        df.columns = ['date','open','high','low','close'] #Make sure column names are legit  
        df['index'] = np.arange(len(df)) #create an index 
        df['hilow_median'] = df[['high', 'low']].median(axis=1)
    return df
#%% end of cell begining of new
#Cleanup columns
clean_Columns(dfm)
clean_Columns(dfw)
clean_Columns(dfd)
#clean_Columns(df60)

#For some fuckin reason this has to be done in this order to filter out the weekends...
df60.reset_index(inplace=True) #reset index to get timestamp out
df60.columns = ['date','open','high','low','close'] #Make sure column names are legit 
df60 = df60[df60['date'].dt.weekday < 5] #Filter out all weekend data
df60['index'] = np.arange(len(df60)) #create an index 
df60['errorslope']=np.nan
df60['hilow_median'] = df60[['high', 'low']].median(axis=1)
df60['high_diff']=np.nan
df60['low_diff']=np.nan

#Make copies
dfm_copy = dfm.copy()
dfw_copy = dfw.copy()
dfd_copy = dfd.copy()

#Filter the dates
dfm_copy = dfm_copy[dfm_copy['index'] < 18]
dfw_copy = dfw_copy[dfw_copy['index'] < 10]
dfd_copy = dfd_copy[dfd_copy['index'] < 30]
#%% end of cell begining of new

_val = 'low'
_low = 'low'
hilow_median = 'hilow_median'

#_monthsback = 

def Shade_Reversal_Zones(df,ax):
    ax.fill_between([0,df['index'].count()],df['high'].max(), df['high'].quantile(0.8), alpha=0.4,color='green')
    ax.fill_between([0,df['index'].count()],df['low'].min(),df['low'].quantile(0.2),alpha=0.4,color='orange')

def getregresion_line(df):
    if 'regress' not in df.columns:
        b, m = polyfit(df['index'], df[hilow_median], 1)
        a = (df['index'], b + m * df['index'])
        dft = a[1]
        obj = pd.DataFrame(dft) 
        obj.reset_index(inplace=True)
        obj.rename(columns={'level_0': 'index', 'index': 'regress'}, inplace=True)
        df = df.merge(obj,on='index',how='left')
        return df

def Set_Ylim(df,ax):
    ax.set_ylim([df['low'].min(),df['high'].max()])

def Plot_HiLowBars(df,ax):
    ax.fill_between([0,df['index'].count()],df['high'].max(), df['high'].quantile(0.8), alpha=0.4,color='green')
    ax.fill_between([0,df['index'].count()],df['low'].min(),df['low'].quantile(0.2),alpha=0.4,color='orange')
    ax.yaxis.tick_right()
    #ax.invert_xaxis()

def Plot_errorLine(df,ax):
    b, m = polyfit(df['index'], df[hilow_median], 1)
    ax.plot(df['index'], b + m * df['index'], 'r--')
    ax.yaxis.tick_right()
    
def plot_Reversal_Extremes_HTF(df,ax):
    b, m = polyfit(df['index'], df[hilow_median], 1)
    ax.plot(df['index'], b + m * df['index'], 'r--')
    ax.yaxis.tick_right()
    a = df['high']-df['low']
    a = (a.mean())*0.75
    ax.plot(df['index'], a + (b + m * df['index']), 'g--')
    ax.plot(df['index'], (b + m * df['index']) - a, 'b--')
    
    
def plot_Reversal_Extremes_LTF(df,ax):
    #df['regress'] = np.nan
    b, m = polyfit(df['index'], df[hilow_median], 1)
    ax.plot(df['index'], b + m * df['index'], 'r--')
    ax.yaxis.tick_right()
    diffhigh = (df.loc[df.high.idxmax(), 'regress'])
    diffhigh = df['high'].max() - diffhigh
    diffLow = (df.loc[df.low.idxmin(), 'regress'])
    diffLow = df['low'].min() - diffLow    
    ax.plot(df['index'], diffhigh + (b + m * df['index']), 'g--')
    ax.plot(df['index'], (b + m * df['index']) + diffLow, 'b--')
    
    
def Plot_Medians(df,ax):
    price_median = (df['high'].max() + df['low'].min())/2
     #mean= np.mean(df.loc[:,'hilow_median'])
     #ax.hlines(df.loc[:,'hilow_median'].median(), 0,len(df['index']),color='r', linestyles='--', lw=2)
    ax.hlines(price_median, 0,len(df['index']),color='r', linestyles='--', lw=2)
#     lim = ax.get_xlim()
#     ax.set_xticks(list(ax.get_xticks()) + '1.123')
#     ax.set_xlim(lim)
     #trans = transforms.blended_transform_factory(ax.get_yticklabels()[0].get_transform(), ax.transData)
     #ax.text(0,mean, "{:.0f}".format(mean), color="red", transform=trans,ha="right", va="center")
         
       
#Set the main figure proportions
fig = plt.figure(figsize=(20,25))
fig.subplots_adjust(hspace=0.3)

# Divide the figure into a 2x2 grid, and set sections to ax1 and ax2
ax1 = fig.add_subplot(421)
ax2 = fig.add_subplot(422)
ax3 = fig.add_subplot(423)
ax4 = fig.add_subplot(424)
ax5 = fig.add_subplot(425)
ax6 = fig.add_subplot(426)
ax7 = fig.add_subplot(427)
ax8 = fig.add_subplot(428)


#Monthly
ax1.scatter(dfm_copy['index'], dfm_copy['low'], marker='.')
ax1.scatter(dfm_copy['index'], dfm_copy['high'], marker='.')

#Weekly
ax2.scatter(dfw_copy['index'], dfw_copy['low'], marker='.')
ax2.scatter(dfw_copy['index'], dfw_copy['high'], marker='.')

#Daily 
ax3.scatter(dfd_copy['index'], dfd_copy['low'], marker='.')
ax3.scatter(dfd_copy['index'], dfd_copy['high'], marker='.')

#Daily scatter plot
ax4.scatter(dfd_copy['index'], dfd_copy['low'], marker='.')
ax4.scatter(dfd_copy['index'], dfd_copy['high'], marker='.')

#60 minute
df60.plot(x='index', y=_val, ax=ax5, legend=False)
df60.plot(x='index', y=_val, ax=ax6, kind = 'scatter', marker='.')
df60.plot(x='index', y=_val, ax=ax7, legend=False)
df60.plot(x='index', y=_val, ax=ax8, kind = 'scatter',marker='.')

#for some reason I have to invert these axis
ax1.invert_xaxis()
ax2.invert_xaxis()
ax3.invert_xaxis()
ax4.invert_xaxis()
ax5.invert_xaxis()
ax6.invert_xaxis()
ax7.invert_xaxis()
ax8.invert_xaxis()

#ax1.yaxis.set_label_text("Month")
ax1.set_title("Month")
ax2.set_title("Week")
ax3.set_title("Day high/low median")
ax4.set_title("Day scatter")
ax5.set_title('Linear regression line 60 min')
ax6.set_title('Linear regression Scatter 60 min')
ax7.set_title('Straight reversal regression 60 min')
ax8.set_title('Straight reversal scatter 60 min')

#Set the chart y limits
Set_Ylim(dfd_copy,ax4)
Set_Ylim(df60,ax6)
Set_Ylim(df60,ax8)

#populate the regression line
dfm_copy = getregresion_line(dfm_copy)
dfw_copy = getregresion_line(dfw_copy)
dfd_copy = getregresion_line(dfd_copy)
#df60 = getregresion_line(df60)

#Plot the sloping line
Plot_errorLine(df60,ax5)
Plot_errorLine(df60,ax6)

#Plot the sideways median line
plot_Reversal_Extremes_HTF(dfm_copy,ax1)
plot_Reversal_Extremes_HTF(dfw_copy,ax2)
plot_Reversal_Extremes_LTF(dfd_copy,ax3)
#plot_Reversal_Extremes_LTF(df60,ax6)
Plot_Medians(dfd_copy,ax4)

#Plot the 20% ranges fior high and low bars
Plot_HiLowBars(dfd_copy,ax4)
Plot_HiLowBars(df60,ax7)
Plot_HiLowBars(df60,ax8)
