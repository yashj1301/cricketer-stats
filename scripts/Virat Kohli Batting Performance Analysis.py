#!/usr/bin/env python
# coding: utf-8

# # Analyzing Virat Kohli's overall Batting Performance
# 
# In this project, we will be analyzing Virat Kohli's performance from his debut to the very recent match - WT20 2024 Final against South Africa. 
# 
# ![image.png](attachment:image.png)
# 
# Let us import the necessary libraries first.

# ## Importing necessary libraries

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import seaborn as cb
import warnings as wr

wr.filterwarnings('ignore')


# Now, we will import the <code>html-table-parser </code>, <code>urllib</code>, and <code>pprint</code> libraries to scrape data from ESPNCricInfo website- https://stats.espncricinfo.com/ci/engine/player/253802.html?class=11;template=results;type=batting;view=innings .
# 
# Let us go ahead.

# In[ ]:


get_ipython().system('pip install html-table-parser-python3')
import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser


# ## Extracting Data

# In[ ]:


# Opens a website and read its binary contents (HTTP Response Body)

def url_get_contents(url):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
  req = urllib.request.Request(url=url, headers=headers)
  f = urllib.request.urlopen(req)
  return f.read()


# In[ ]:


xhtml = url_get_contents('https://stats.espncricinfo.com/ci/engine/player/253802.html?class=11;template=results;type=batting;view=innings').decode('utf-8')

# Defining the HTMLTableParser object
p = HTMLTableParser()
p.feed(xhtml)

# converting the parsed data to
# dataframe
virat = pd.DataFrame(p.tables[3])
virat.head()


# We have extracted the data. Now, it is time to get going. We will perform the data cleaning first.

# ## Preparing the Data

# Now, we will be preparing our dataframe. Our first order of business is to modify the metadata of the dataframe. Let us see.

# ### 1. Renaming Columns
# 
# First, we will rename the columns, and remove the row containing the names of the columns. Let us do that.

# In[ ]:


virat.columns=virat.loc[0].values
virat.head()


# ### 2. Removing Unnecessary Rows and Columns
# 
# Now, we would remove the last column, since it is not too relevant in our analysis, and the first row, since it already is there as headers.

# In[ ]:


virat = virat.iloc[1:,:-1]
virat.head()


# Our data is ready for inspection. Let us check.

# ### 3. Inspecting the Data
# 
# Let us start with some basic information about our dataset. It includes size, attributes and types of data.

# In[ ]:


virat.info()


# In[ ]:


orig = virat.shape; orig


# Hence, we have a data of total 616 innings played by Virat Kohli, measured via 13 parameters. We will now proceed towards cleaning the data.

# ### 4. Cleaning the Data
# 
# Now, we will sanitize our data, to prepare it for analysis. Let us start.

# We know that there is an additional column, which seems to be blank. Let us check what it is.

# In[ ]:


display(virat.iloc[:,9].value_counts(),
        virat.columns)


# This column is entirely blank, and does not provide any input to our data. Hence, let us drop it.

# In[ ]:


virat = virat.drop("",axis=1)
virat.info()


# Great. Moving forward, let us change the data types of the columns. Let us study the type of values for each column.

# In[ ]:


for i in virat.columns:
  print(f"\n--------------------- Col Name: {i} ------------------\n")
  print(virat[i].value_counts())


# Now, based on this, we can classify the columns into 3 categories :
# 
# 1. Integer - Runs, Mins, BF, 4s, 6s
# 2. Category - Ground, Opposition, Dismissal, Pos, Inns
# 3. Decimal - Strike Rate (SR)
# 4. Date - Start Date
# 
# Let us transform the columns now.

# In[ ]:


numeric = ['Runs','Mins','BF','4s','6s']
category = ['Ground','Dismissal','Opposition','Pos','Inns']
decimal = 'SR'
date = 'Start Date'


# #### Numeric Columns
# 
# Let us study the numerical columns one by one.

# In[ ]:


virat['Runs'].unique()


# We can see that there are some inconsistencies due to which it cannot be converted to numerical, like -
# 
# 1. The asterisk (*) after the score, indicating him being not out
# 2. The terms TDNB and DNB, indicating the innings where he did not bat, and team did not bat.
# 
# Let us study these first.

# In[ ]:


virat.loc[virat['Runs'].apply(lambda x: '*' in x),['Runs','Dismissal']]


# Hence, we already have a not out dismissal mode. So, the * is not needed. Let us remove it.

# In[ ]:


virat['Runs']=virat['Runs'].str.strip('*')
virat['Runs'].unique()


# Now, we need to check the instances where he did not bat, or the team did not bat.

# In[ ]:


virat.loc[virat['Runs'].isin(['TDNB','DNB']),:]


# The entries where the team did not bat, is not relevant to our study. Hence, it is better we drop them.
# 
# For the innings where Virat did not bat, there cannot be much meaningful conclusions, as numerical data is not available.
# 
# Hence, let us drop all these entries.We won't be deleting them, though.

# In[ ]:


virat_new = virat.loc[~virat['Runs'].isin(['TDNB','DNB']),:]
virat_new.shape


# Virat played 588 innings in 616 matches. Let us move ahead now. We can convert the column 'Runs' to numerical now.

# In[ ]:


virat_new['Runs'] = virat_new['Runs'].astype('int')
virat_new['Runs']


# Now, let us move to another column. We will first check the remaining numerical columns.

# In[ ]:


numeric


# In[ ]:


virat_new[numeric]


# Let us check these one by one. With this preliminary diagnosis, it seems there are not much incorrect values in the columns.

# In[ ]:


display(
    virat_new['Mins'].unique(),
    virat_new['BF'].unique(),
    virat_new['4s'].unique(),
    virat_new['6s'].unique()
)


# We can see a common '-' value in all the columns. Let us check if they are exclusive, or connected to each other.

# In[ ]:


virat_new[virat_new.Mins.apply(lambda x: '-' in x)]


# We can see that 'Minutes spent at crease' data is missing in these entries. Hence, let us study the column a bit more.

# In[ ]:


virat_new['Mins'].unique()


# The column is significantly important to us, studying the trend of the data. Hence, we cannot drop them. However, we can fill these with null values - this will ensure biasness is minimised from the analysis.

# In[ ]:


virat_new['Mins']=virat_new['Mins'].replace('-',np.NaN).astype(float)
virat_new.Mins


# In[ ]:


virat_new['Mins'].describe()


# Great. Now that it is taken care of, let us study the rest of the columns.

# In[ ]:


numeric


# In[ ]:


virat_new[numeric[2:]] = virat_new[numeric[2:]].astype(int)
virat_new[numeric].info()


# Great. Now, let us move towards the categorical columns.

# #### Categorical Columns
# 
# Let us study the categorical columns now.

# In[ ]:


category


# In[ ]:


virat_new[category]


# Let us look at the unique values for each column.

# In[ ]:


for i in category:
  print(f"\n---------- Col Name: {i} --------------------\n")
  print(virat_new[i].value_counts())


# We can split the Opposition column into 'Opponent' and 'Format'. Let us do that now.

# In[ ]:


virat_new.insert(5,'Format',virat_new['Opposition'].str.split(' v ',n=1,expand=True)[0])
virat_new['Opposition'] = virat_new['Opposition'].str.split(' v ',n=1,expand=True)[1]
virat_new.head()


# In[ ]:


virat_new['Format'].value_counts()


# Great. We have extracted the formats. Let us do this same thing for the original dataset as well.

# In[ ]:


virat.insert(5,'Format',virat['Opposition'].str.split(' v ',n=1,expand=True)[0])
virat['Opposition'] = virat['Opposition'].str.split(' v ',n=1,expand=True)[1]
virat.head()


# In[ ]:


virat['Format'].value_counts()


# Now, we have the data for matches and innings played by Virat across each format. Let us move forward with the only decimal column left - "Strike Rate".
# 

# #### Decimal Column
# 
# The column 'Strike Rate' is given as SR. Let us study it.

# In[ ]:


virat_new['SR'].describe()


# In[ ]:


virat_new.SR.unique()


# We have a '-' entry here as well. Let us check it.

# In[ ]:


virat_new[virat_new.SR=='-']


# Here, Virat has a diamond duck as well. Hence, let us impute this to be 0 strike rate.

# In[ ]:


virat_new.loc[virat_new.SR=='-','SR']=0
virat_new[virat_new.SR==0]


# Now, let us convert it to float data type.

# In[ ]:


virat_new['SR'] = virat_new['SR'].astype('float')
virat_new['SR']


# Great, it is done. Let us do the same with the original dataset as well.

# In[ ]:


virat.loc[virat.SR=='-','SR']=0
virat['SR'] = virat['SR'].astype('float')
virat['SR']


# Great. Both datasets are ready. Let us move forward.

# #### Date Column
# 
# Now, let us study the date column in the data.

# In[ ]:


virat_new['Start Date'] = virat_new['Start Date'].astype('datetime64[ns]')
virat_new['Start Date']


# Let us do the same with the original dataset, to avoid any errors at the time of importing.

# In[ ]:


virat['Start Date'] = virat['Start Date'].astype('datetime64[ns]')
virat['Start Date']


# With this, we are done with the data preparation part. Let us move forward with Loading the data to BigQuery.

# ## Loading the Data
# 
# It is time to export the data to an excel file. Both the dataframes - virat and virat_new would be 2 sheets of a single excel file, which would be stored in BigQuery.
# 
# First, let us check the details of both datasets.

# In[ ]:


virat.head()


# In[ ]:


virat_new.head()


# Now, let us import the necessary libraries to do the loading.

# In[ ]:


get_ipython().system('pip install google-cloud-bigquery pandas-gbq')


# In[ ]:


from google.cloud import bigquery
from pandas_gbq import to_gbq


# In[ ]:


client = bigquery.Client()

project_id = 'natural-nimbus-408107'
dataset_id = 'virat_batting'
table1_id = 'virat'  # The table to create or replace
table2_id = 'virat_new'

dataset_ref = client.dataset(dataset_id)
try:
    client.get_dataset(dataset_ref)
    print(f"Dataset {dataset_id} already exists.")
except Exception as e:
    print(f"Dataset {dataset_id} does not exist. Creating dataset...")
    dataset = bigquery.Dataset(dataset_ref)
    dataset = client.create_dataset(dataset)
    print(f"Dataset {dataset_id} created.")

# Wait for dataset creation to complete
dataset = client.get_dataset(dataset_ref)
print(f"Dataset {dataset_id} is ready.")


# In[ ]:


#loading tables to dataset

to_gbq(virat, destination_table=f"{project_id}.{dataset_id}.{table1_id}",
       project_id=project_id, if_exists='replace')

print(f"DataFrame successfully exported to BigQuery table"+
f"{project_id}.{dataset_id}.{table1_id}.")

to_gbq(virat_new, destination_table=f"{project_id}.{dataset_id}.{table2_id}",
       project_id=project_id, if_exists='replace')

print(f"DataFrame successfully exported to BigQuery table"+
f"{project_id}.{dataset_id}.{table2_id}.")


# ## Data Visualization
# 
# Now, it is time to visualize the data. Let us do it one by one.

# In[ ]:


virat.info()


# In[ ]:


virat_new.info()


# Let us begin with the different types of columns now. We previously created arrays for the same.

# In[ ]:


display(numeric,
category,
decimal,
date)


# Let us make the following changes-
# 
# 1. Add Mins to the decimal array, and remove it from numeric.
# 2. Add Format to category array.

# In[ ]:


category+=['Format']
decimal=[decimal,'Mins']
numeric.pop(1)

display(category,
        decimal,
        numeric)


# Now that we have classified the columns, let us move ahead with our analysis.

# ### Preliminary Study

# In[ ]:


round(virat_new[numeric].describe([0,0.25,0.75]),3)


# We can see that he has an overall average of 45.72 in 588 innings. He faces an average of 57 balls per innings. His maximum score is 254 runs, and he hits an average of 9 fours and 1 six every 2 matches (all formats included).
# 
# Let us move ahead.

# In[ ]:


virat_new.sort_values(by='Start Date',ascending=False).head(5)


# His latest 5 innings across formats. This could go well on our dashboard. Let us move towards categorical columns.

# In[ ]:


virat_new[category].describe()


# Virat has played most matches in Mirpur Stadium, Bangladesh. He has played the most against Australia (113 matches across formats), while he has played the most innings in ODIs. He has been caught 356 times in his career, the most frequent form of dismissal.
# 
# Let us do some analysis now.

# ### 1. Number of Matches, innings and not outs
# ### 2. Last 5 innings details
# ### 3. Average runs, BF and SR, mins batted in ODIs
# ### 4. Best and Worst Opposition, Grounds, Position
# ### 5. Highest and lowest modes of dismissal, and averages across them.
# ### 6. Best and worst position for him to bat.
# ### 7. Number of 4s and 6s total, average per game.
# 
# All this to be done for overall, and each format.
# 
# Combinations -
# 
# 1. Ground, Opposition, Dismissal, Position
# 2. Month of the year
# 
# Metrics -
# 
# 1. Total Runs, Average Runs,
# 2. Average Balls faced,
# 3. Average minutes spent at crease,
# 4. Strike Rate
# 

# To find the number of matches played by Virat in each format, we need to work collaboratively with both the datasets - virat and virat_new.
# 
# This will be done in Power BI Dashboard.
