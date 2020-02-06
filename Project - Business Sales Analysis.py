#!/usr/bin/env python
# coding: utf-8

# ## Introduction
# 
# In this mini project, you will explore and analyze the Business Sales dataset. The dataset shows the sales of a company in different shops. Each row shows how many items of a specific product were sold on some date in some shop. The focus is on number of products sold and revenues.
# 
# The guideline is only there to give you some ideas. You don't have to follow or complete all of them. The important thing is to create a coherent analysis with meaningful comments. However, we expect that you are able to do the first 4 sections. Section 5 and 6 have more advanced questions and you may choose to do them according to your current level.

# Data fields
# 
#     date - date in format yyyy-mm-dd
#     date_block_num - a consecutive month number, used for convenience. January 2013 is 0, February 2013 is 1,..., October 2015 is 33
#     shop_id - unique identifier of a shop
#     shop_name - name of shop
#     item_id - unique identifier of a product
#     item_price - current price of the item (in Russian RUB)
#     item_cnt_day - number of products sold on that date in that shop
#     item_name - name of item
#     item_category_id - unique identifier of item category
#     item_category_name - name of item category
# 

# Shop name: The first word in shop_name is the name of a city in Russia
# 
# Item category name: Contains the general category and sub category, separated by -

# In[85]:


get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[86]:


sales = pd.read_csv('sales_eng.csv')


# In[87]:


sales


# 1- Initial inspection
# 
# 
# 2- Data cleaning:
#     - Convert the date column to Datetime object (optional: you can choose to set it as index)
#     - Inspect and handle missing values
#     - Correct/remove outliers (too high item_price/item_cnt_day, negative values)
# 
# 
# 3- Create new information (only do the ones you think is needed for your analysis):
#     - Revenues (items sold * item price)
#     - City name
#     - Product general category
# 
# 
# 4- Explore the data from different angles:
#     - Plot the total amount of items sold by day. Which time of the year company makes more sales?
#     - Plot the total amount sold by day of the week. Were more sales being made during the weekends?
#     - Plot the top (20-30) shops by amount sold (or revenues). Which cities are they usually located?
#     - Plot the top products by amount sold (or revenues). Plot the top general categories / sub-categories.
#     - Bin the item_price into categories (range of your choice) and plot them.
#     
# 
# 5- If you want more brain burner challenges, try focusing on items through these in-depth questions
#     - Which were the best selling item for each month by amounts sold / revenue?
#     - How many items haven't made a sale in the last 6 months?
#     - A manager wants to know which items have been selling consistently well. She defines that an item has a good  month if it accumulates more than 100000 RUB in revenues. Show 10 items that have the most good months and their average monthly revenues.
#     - Sometimes an item is sold at a higher or lower than its usual price. A manager wants to know if they make more sales (in total and on average) when they increase or decrease the product price. An item is deemed overpriced (underpriced) when it's sold at 10% higher (lower) than the item's average price, otherwise it's priced normally. 
#     
# 
# 6- Alternatively, you can focus on the shop
#     - Plot the daily revenues of the top 5 shops (in terms of total revenues).
#     - Show the top 10 shops that sell the widest range of products (hint: nunique). Plot a double bar chart showing the number of unique product and total revenues (hint: use .agg()).
#     - What is the correlation between yesterday revenues and today revenues? For easy version, do it on the global  scale. For a very hard version, group the data by shop and then by date (sum revenues), then create a column     that shows the previous day's revenue.

# In[88]:


sales.info()


# In[89]:


sales.date = pd.to_datetime(sales.date, format="%Y-%m-%d", errors="coerce")


# In[90]:


sales.date


# In[91]:


sales.isnull().sum()#missing values in each columns


# In[92]:


sales.isnull().sum().values.sum()#total amount of missing values


# In[93]:


sales[sales.isnull().any(axis=1)]#selecting rows with missing data in each row


# In[94]:


sales.dropna(thresh=5,inplace=True) #to keep the rows with meaning values indirectly removing 


# In[95]:


sales.tail(10)


# In[101]:


sales.isnull().sum()


# In[102]:


sales.isnull().head(10)


# In[103]:


sales["item_price"].fillna(sales["item_price"].mean(),inplace=True)


# In[135]:


sales.item_category_name=sales.groupby("item_id").item_category_name.transform("first")


# In[137]:


sales.item_category_id=sales.groupby("item_id").item_category_id.transform("first")


# In[138]:


sales.isnull().sum()


# In[106]:


sales.item_id.unique()


# In[107]:


sales1=sales[["item_id","item_category_id","item_category_name"]]
sales1.tail(10)


# In[108]:


sales[sales.item_id==3876]


# In[109]:


#fill the missing value
sales["item_category_id"].fillna(value=28.0)


# In[110]:


sales.shape


# In[111]:


sales.columns


# In[112]:


sales.describe()


# In[113]:


sales.item_price.plot("hist")


# In[115]:


sales[sales.item_price>5000].item_price.plot("hist")


# In[119]:


sales.drop(sales[sales.item_price>30000].index,axis=0)


# In[121]:


sales.item_cnt_day.plot("hist")


# In[123]:


sales[sales.item_cnt_day>200].item_cnt_day.plot("hist")


# In[124]:


sales.drop(sales[sales.item_cnt_day>1800].index,axis=0)


# In[129]:


sales[sales.item_cnt_day<0]


# In[140]:


sales["Revenue"]=sales.item_cnt_day*sales.item_price
sales


# In[153]:


sales["City"]=sales["shop_name"].str.split(" ").str[0]
sales


# In[159]:


#Plot the total amount of items sold by day. Which time of the year company makes more sales?
gb=pd.DataFrame(sales.groupby(["date_block_num"])["item_cnt_day"].sum().reset_index())
gb


# In[167]:


gb1 = sales.groupby(["date"])["item_cnt_day"].sum() #Plot the total amount of items sold by day. Which time of the year company makes more sales?


# In[168]:


gb1


# In[171]:


gb1.plot("line",figsize=(12,6))#Plot the total amount of items sold by day. Which time of the year company makes more sales?


# In[173]:


#Plot the total amount sold by day of the week. Were more sales being made during the weeks
sales = sales.set_index(sales.date)
gb2 = sales["day_of_week"]= sales.index.day_name()
gb2


# In[174]:


gb3=sales.groupby(["day_of_week"])["item_cnt_day"].sum()


# In[175]:


gb3


# In[176]:


gb3.plot("line")#saturday is highest


# In[202]:


#Plot the top (20-30) shops by amount sold (or revenues). Which cities are they usually located?
gb4=pd.DataFrame(sales.groupby(["City"],as_index=False)["Revenue"].sum())


# In[203]:


gb4


# In[208]:


gb5 = gb4.sort_values(by=['Revenue'], ascending=False)
gb5


# In[211]:


plt.figure(figsize=(12,6))
top_20= sns.barplot(x=gb5["City"][:20], y=gb5["Revenue"])
top_20.set_xticklabels(top_20.get_xticklabels(), rotation=45)
plt.show(top_20)


# In[213]:


gb6= pd.DataFrame(sales.groupby(["shop_name"])["Revenue"].sum())
gb6.sort_values("Revenue",ascending=False).iloc[:20].plot(kind="bar",figsize=(12,6))


# In[217]:


#Plot the top products by amount sold (or revenues). Plot the top general categories / sub-categories.
gb7= pd.DataFrame(sales.groupby(["item_category_name"])["Revenue"].sum())
gb7


# In[219]:


gb7.sort_values("Revenue",ascending=False).iloc[:20].plot(kind="bar",figsize=(12,6))


# In[228]:


#Bin the item_price into categories (range of your choice) and plot them.
sales.describe().round(2)


# In[227]:


sales[sales.item_price==-1]
sales=sales[sales.item_price!=-1]


# In[232]:


bins = [0, 10000, 15000, 25000, 30000]
labels = ['low', 'medium', 'high', 'very high']


# In[237]:


sales['Price_cat'] = pd.cut(x=sales.item_price, bins=bins, labels=labels)

sales.Price_cat.value_counts().plot("bar",logy=True)


# In[240]:


#Which were the best selling item for each month by amounts sold / revenue?
sales["Month"]=sales.index.month_name()
sales.groupby(["Month","item_name"])["Revenue"].sum()


# In[247]:


df=sales.groupby(["Month","item_name"])["Revenue"].sum()
df.groupby(level=0).apply(max).round(2)


# In[251]:


df1= sales.groupby(["Month","item_name"]).sum()
item= df1["Revenue"].groupby(level=0, group_keys=False)
item.nlargest(1)


# In[ ]:




