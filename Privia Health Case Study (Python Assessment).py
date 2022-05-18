#!/usr/bin/env python
# coding: utf-8

# In[135]:


#Question 1
import pandas as pd


df = pd.read_excel (r'C:\Users\yemi.fagbade\Privia Family Medicine 113018.xlsx')
df


# In[136]:


df.columns


# In[137]:


header_row = 2
df.columns = df.iloc[header_row]
df.head()


# In[138]:


df.columns


# In[139]:


df.columns = df.columns.str.replace(' ', '')
df.rename(columns = {'DOB[1]':'DOB'}, inplace = True)
df.columns


# In[140]:


df = df.iloc[3:-3,1:]
df.head()


# In[141]:


demographics_df = (df.iloc[:,:7]).reset_index(drop=True)
demographics_df.head()


# In[142]:


import os
import re
head,tail = os.path.split(r"C:\Users\yemi.fagbade\Privia Family Medicine 113018.xlsx")

def extract_basename(path):
  """Extracts basename of a given path"""
  basename = re.search(r'[^\\/]+(?=[\\/]?$)', path)
  if basename:
    return basename.group(0)

filename = extract_basename(tail)[:-5]
filename


# In[143]:


demographics_df['ProviderGroup'] = filename[:-7]
demographics_df['FileDate'] = filename[-7:]
demographics_df.head()


# In[144]:


#Include only the first initial of the Middle Name when applicable.
import numpy as np
demographics_df['MiddleName'] = [x[0] if isinstance(x, str) else np.nan for x in demographics_df['MiddleName']]
demographics_df.head()


# In[145]:



#Convert the Sex value to M or F: M for 0 and F for 1
import datetime
#demographics_df['DOB'] = pd.to_datetime(demographics_df['DOB']).dt.date
demographics_df['FileDate'] = pd.to_datetime(demographics_df['FileDate']).dt.date

demographics_df.loc[demographics_df['Sex'] == 0, 'Sex'] = 'M'
demographics_df.loc[demographics_df['Sex'] == 1, 'Sex'] = 'F'

demographics_df.head()


# In[146]:


df = df[['ID','AttributedQ1', 'AttributedQ2', 'RiskQ1', 'RiskQ2','RiskIncreasedFlag']].merge(demographics_df, how='left', on='ID' ).reset_index(drop=True)
df.head()


# In[147]:


df.columns


# In[148]:


cols = ['ID', 'FirstName', 'MiddleName', 'LastName', 'DOB', 'Sex',
       'FavoriteColor', 'AttributedQ1', 'AttributedQ2', 'RiskQ1', 'RiskQ2',
       'RiskIncreasedFlag', 'FileDate']
qr_df = df.loc[:,cols]
qr_df.head()


# In[149]:


#Question 2


def multi_melt(
    df: pd.DataFrame,
    id_vars=None,
    value_vars=None,
    var_name=None,
    value_name="value",
    col_level=None,
    ignore_index=True,
) -> pd.DataFrame:

    melted_dfs = [
        (
            df.melt(
                id_vars,
                *melt_args,
                col_level,
                ignore_index,
            ).pipe(lambda df: df.set_index([*id_vars, df.groupby(id_vars).cumcount()]))
        )
        for melt_args in zip(value_vars, var_name, value_name)
    ]

    return (
        pd.concat(melted_dfs, axis=1)
        .sort_index(level=3)
        .reset_index(level=3, drop=True)
        .reset_index()
    )


# In[150]:


unpivot_qrdf = qr_df.pipe(
    multi_melt,
    id_vars=['ID', 'FileDate', 'RiskIncreasedFlag'],
    value_vars=[
      ['AttributedQ1','AttributedQ2'],
      ['RiskQ1', 'RiskQ2'],
    ],
    var_name=['Quarter','QuarterR'],
    value_name=['AttributedFlag', 'RiskScore']
)


# In[151]:


unpivot_qrdf


# In[152]:


unpivot_qrdf['Quarter'] = unpivot_qrdf['Quarter'].astype(str).str[-2:]
unpivot_qrdf.drop('QuarterR', axis = 1,inplace=True)
unpivot_qrdf.head()


# In[153]:


df_qr = unpivot_qrdf[unpivot_qrdf['RiskIncreasedFlag'] == 'Yes']
df_qr.head()


# In[154]:


df_qr = df_qr.reindex(['ID','Quarter','AttributedFlag', 'RiskScore', 'FileDate'], axis=1)
df_qr.head()


# In[ ]:




