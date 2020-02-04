# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 17:54:56 2020

@author: grant
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict



#cols=['Date', 'Time', 'Open','High','Low','Last']

df = pd.read_csv('Data/d.csv',skipinitialspace=True)
format = '%Y-%m-%d %H:%M:%S'
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format=format)
df = df.set_index(pd.DatetimeIndex(df['Datetime']))
#df.index = pd.to_datetime(df.index, unit='s')


def Market_Profile_G(df, frequency='30Min', debug=0):   
   #intialize dictionary and char 'A, B, C..'    
   md=defaultdict(str)
   char_a=64
   #make a group based on Timestamp with frequency 30min
   TGroups=df.groupby([pd.Grouper(key='Date', freq=frequency)]) 
    #iterate over each group and add to dictionary, 
   #dictionary keys are 'High' and 'Low' of each group, rounded and values are 
   #char A, B incremented for each period(freq group), default 30 min 
   #since we grouped based on freq, for each group increment the char i.e +1
 

   for t,g in TGroups:
       char_a +=1     
       #skip non alphabets
       if char_a == 91:
          char_a=97
       min_price=np.round(g.Low.min())
       max_price=np.round(g.High.max())
       if debug==1:
          print(g.Low.min(), g.High.max()) 
       for price in  range(int(min_price), int(max_price+1)):
          md[price]+=(chr(char_a))
   return sorted(md.items(), key=lambda k:k,reverse=1)

Market_Profile_G(df)