#!/usr/bin/env python
# coding: utf-8

# In[40]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[62]:


complaint_df = pd.read_csv(r'./input/complaints.csv')


# In[63]:


complaint_df['Consumer disputed?']=complaint_df["Consumer disputed?"].replace(np.nan, 1)
complaint_df['Consumer disputed?']=np.where(complaint_df['Consumer disputed?']=="Yes",0,1)


# In[64]:


complaint_df.head()


# In[65]:


complaint_df['Date received'] = pd.to_datetime(complaint_df['Date received'])
print(complaint_df['Date received'].dtype)


# 

# In[66]:


complaint_df['Year'] = complaint_df['Date received'].dt.year


# In[67]:


complaint_df.head()


# In[68]:


missing_data = complaint_df.isnull()
missing_data.head()


# In[69]:


for col in missing_data.columns.values.tolist():
    print (col)
    print(missing_data[col].value_counts())
    print("")


# In[70]:


complaint_df.dropna(subset=["Product"], axis = 0, inplace=True)
complaint_df.reset_index(drop = True, inplace = True)


# In[71]:


complaint_df.head()


# In[72]:


complaint_df.drop(['Sub-product','Date received', 'Issue', 'Sub-issue','Consumer complaint narrative', 'Company public response', 'State','ZIP code', 'Tags', 'Consumer consent provided?', 'Submitted via', 'Date sent to company', 'Company response to consumer', 'Timely response?', 'Complaint ID'], axis = 1, inplace = True)


# In[73]:


complaint_df.head()


# In[74]:


complaint_df = complaint_df.sort_values('Product')


# 

# In[75]:


complaint_df.head()


# In[76]:


num = complaint_df.groupby(['Product', 'Year','Company']).agg({'Consumer disputed?': ['sum']})
total = complaint_df.groupby(['Product', 'Year']).agg({'Consumer disputed?': ['sum']})
total.columns = ['total'] 
num.columns = ['Number of complaints']
num = num.reset_index()
total = total.reset_index()
num.head()


# In[77]:


total.head()


# In[78]:


complaint = num.groupby(['Product', 'Year']).max()[['Number of complaints']]
complaint.columns = ['Num of Complaints']
complaint = complaint.reset_index()
complaint.head()


# In[79]:


cx_complaint = pd.merge(complaint, total)
cx_complaint


# In[80]:


cx_complaint['Percentage'] = np.round((cx_complaint['Num of Complaints']/cx_complaint['total'])*100)
cx_complaint['Percentage']=cx_complaint["Percentage"].replace(np.nan, 0)
cx_complaint


# In[81]:


cx_complaint.to_csv(r'./output/report.csv')


# In[ ]:




