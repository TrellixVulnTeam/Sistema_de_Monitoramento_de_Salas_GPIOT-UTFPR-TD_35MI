
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import seaborn as sns

get_ipython().magic(u'matplotlib inline')


# In[2]:


df = pd.read_csv('home.csv')


# In[3]:


df.columns


# In[76]:


print len(df)
df.describe() # dos dados numericos


# In[79]:


leitura = len(df)
atual = (np.array(df[leitura-2:leitura-1]).tolist())[0]
#d = (np.array(df[28:29]).tolist())[0]
print atual


# In[75]:


for p in range(len(d)):
    print p,d[p]

