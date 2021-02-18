#!/usr/bin/env python
# coding: utf-8

# # @USRebellion1776 claims that the Michigan and Georgia democratic ballots could be suspicious due to differences in senate votes versus presidential votes cast in voter ballots. 
# 
# ## Let's check this out with some data!

# Story: https://www.zerohedge.com/political/why-does-biden-have-so-many-more-votes-democrat-senators-swing-states?fbclid=IwAR1qj4L3RstEHmxr_FIHkeV4GPXmJsd4kX7fU8yIQMawJ2VSj3JiFZbl8Tk

# Data Sources:
# https://electionlab.mit.edu/data and US Census Bureau
# 
# Skip down to "Main Questions" section for the TLDR if you don't care about the data carpentry, shaping, and calculations.

# In[30]:


import pandas as pd


# State votes for President and Senate

# In[31]:


senate = pd.read_csv('senate.csv', encoding='latin-1')
senate.head()


# In[32]:


president = pd.read_csv('president.csv', encoding = 'latin-1')
president.head()


# Let's rename candidate votes to say senate votes so we can merge with the presidential data.

# In[33]:


senate.rename(columns = {'candidatevotes': 'senatevotes'}, inplace = True)


# Let's rename candidate votes to say president votes so we can merge with the senate data above.

# In[34]:


president.rename(columns = {'candidatevotes': 'presidentvotes'}, inplace = True)


# Select columns that we care about (year, state, candidate votes, total votes) for each data frame and then merge together.

# In[35]:


senate_trim = senate[['year', 'state', 'party', 'senatevotes']] 
president_trim = president[['year', 'state', 'party', 'presidentvotes']]
general_election = pd.merge(senate_trim, president_trim, on = ['year', 'state', 'party']).dropna()
general_election.head()


# `'president_no_senate_diff` is the number of voters who voted for a president but not a senator.

# In[74]:


general_election['president_no_senate_diff'] = (general_election['presidentvotes'] - general_election['senatevotes'])
general_election['president_no_senate_prop'] = (general_election['presidentvotes'] / general_election['senatevotes'])


# Let's look at republicans vs democrats only

# In[75]:


general_election = general_election.loc[(general_election['party'] == 'republican') | (general_election['party'] == 'democrat')]


# In[76]:


general_election.head()


# In[77]:


dems = general_election.loc[general_election['party'] == 'democrat']
reps = general_election.loc[general_election['party'] == 'republican']


# Remove outliers from the datasets (take roughly only 99.4% of the data)

# In[105]:


from scipy import stats
dems = dems[(np.abs(stats.zscore(dems.select_dtypes('int64', 'float64'))) < 3).all(axis=1)]
reps = reps[(np.abs(stats.zscore(reps.select_dtypes('int64', 'float64'))) < 3).all(axis=1)]


# ## Bring in 2020 Data for Michigan and Georgia

# 2020 data is not quite available but let's look at the two states in this article: Georgia and Michigan
# Source: https://abcnews.go.com/Elections/2020-us-presidential-election-results-live-map

# In[108]:


#2020 Data pulled from five thirty eight....lets look
georgia_rep_pres = 2454729
georgia_rep_senate = 2455583

georgia_dem_pres = 2463889
georgia_dem_senate = 2364345

michigan_dem_pres = 2794853
michigan_dem_senate = 2722724 

michigan_rep_pres = 2646956
michigan_rep_senate = 2636667


# Senate versus President vote diff proportion calculations

# In[109]:


georgia_dem_pres_senate_prop = georgia_dem_pres / georgia_dem_senate
georgia_rep_pres_senate_prop = georgia_rep_pres / georgia_rep_senate

print('Georgia Democratic President, No Senate Vote Proportion: ', georgia_dem_pres_senate_prop)
print('Georgia Republican President, No Senate Proportion: ', georgia_rep_pres_senate_prop)


# In[110]:


michigan_dem_pres_senate_prop = michigan_dem_pres / michigan_dem_senate
michigan_rep_pres_senate_prop = michigan_rep_pres / michigan_rep_senate

print('Michigan Democratic President, No Senate Vote: ', michigan_dem_pres_senate_prop)
print('Michigan Republican President, No Senate Vote: ', michigan_rep_pres_senate_prop)


# ## QUESTION 1: 
# Are Georgia Democrats abnormally voting for the president but not the senate this year? What percentile would the 2020 President to Senate voting proportions rank historically against elections going back to 1976? 

# In[140]:


ga_dem2020_z_score = (georgia_dem_pres_senate_prop - np.mean(dems['president_no_senate_prop']))/ np.std(dems['president_no_senate_prop'])
stats.norm.cdf(ga_dem2020_z_score)


# Answer: No. This year's proportion of ballots voting for president but not for the senate versus ballots that voted for both offices ranks in the 57th percentile meaning that historically there are 43% of historical elections saw a higher proportion of ballots that voted for the presidential race but not the senate race.

# ## Question 2:
# Are Michigan Democrats abnormally voting for the president but not the senate this year? What percentile would the 2020 President to Senate voting proportions rank historically against elections going back to 1976? 

# In[142]:


mich_dem2020_z_score = (michigan_dem_pres_senate_prop - np.mean(dems['president_no_senate_prop']))/ np.std(dems['president_no_senate_prop'])
stats.norm.cdf(mich_dem2020_z_score)


# Answer for Michigan: No. This year's proportion of ballots voting for president but not for the senate versus ballots that voted for both offices ranks in the 55th percentile meaning that historically 45% of historical elections saw a higher proportion of ballots that voted for the presidential race but not the senate race.
