# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:03:59 2020

@author: grant
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:28:13 2020

@author: grant
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



#cols=['Date', 'Time', 'Open','High','Low','Last']

df = pd.read_csv('Data/zig.csv',skipinitialspace=True)
df.columns = ['a','b','c','d','e','fred']
df['tom'] = df['fred']*10000
#df = df['fred']
x = df['tom'].value_counts()


plt.hist(x, range=(-100,100))
plt.ylabel('Probability');






