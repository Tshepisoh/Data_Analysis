#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

sns.set_style("darkgrid")
sns.set_palette("RdBu")

df = pd.read_excel(r'C:\Users\Tshepiso\Desktop\Coffee Shop Sales.xlsx')
df


# In[9]:


df.isna().sum()


# In[6]:


df2 = df[["store_location","transaction_date","transaction_time","product_category","product_type","unit_price","transaction_qty"]]
df2


# In[83]:


df2['Total_price'] = df2.unit_price*df2.transaction_qty
df2


# In[19]:


df2['transaction_date'] = pd.to_datetime(df2['transaction_date'])

Xp = df2.groupby(df2['transaction_date'].dt.to_period("M"))['transaction_qty'].sum()

Yp = pd.DataFrame({'transaction_date': Xp.index.astype(str), 'transaction_qty': Xp.values})
print(Yp)


# # Data Analysis and Visualisation

# In[21]:


plt.figure(figsize=(10, 6))
plt.plot(Yp['transaction_date'],
         Yp['transaction_qty'],
         marker='o', linestyle='-')

plt.xlabel('DATE OF TRANSACTION')
plt.ylabel('NUMBER OF TRANSACTION')
plt.title('EVOLUTION OF TRANSACTION OVER TIME')

plt.xticks(rotation=45)

for i, txt in enumerate(Yp['transaction_qty']):
  plt.text(Yp['transaction_date'][i], txt, str(txt),
           ha='center', va='bottom')

plt.show()


# **Upon examining sales data over time, a notable and steady increase in transactions becomes evident. This consistent growth in sales suggests a positive trend in sales activity, pointing towards a favorable response from customers or potentially successful strategies implemented by the company. It's also worth considering that changes in seasons may contribute as an influential factor in shaping these patterns.**

# # sales by location

# In[41]:


#Bar Chart
    
df2['transaction_date'] = pd.to_datetime(df['transaction_date'])

KG = df.groupby('store_location')['transaction_qty'].sum()

KG = KG.sort_values(ascending=True)

plt.figure(figsize=(12, 6))
bars = KG.plot(kind='barh', color='tan')

plt.xlabel('Transaction Qty')
plt.ylabel('Store Location')
plt.title('Transactions Per Store')

for bar in bars.patches:
  plt.annotate(f'{bar.get_width():,.0f}',
               (bar.get_width(), bar.get_y() + bar.get_height() / 2),
               ha='center', va='center',
               xytext=(5, 0),
               textcoords='offset points',
               fontsize=8,
               color='black')

plt.show()

# create function that visualized categorical column using pie plot

def pie_plot(column_name, explodeIndex = None):
    """
    1) input : column name, column data type must be object or categorical
    2) explodeIndex, is the index i need to explode it 
    2) output : circle chart that shows size of each unique values and percentage 
    """
    # Create explode list with zeros of size equal to the number of unique values
    explodeList = [0] * df2[column_name].nunique()
    
    # Check and set explodeIndex value 
    if explodeIndex is not None:
        explodeList[explodeIndex] = 0.1
    
    # Create pie plot
    plt.pie(df2[column_name].value_counts(), labels = df2[column_name].value_counts().index, shadow = True, autopct = "%1.1f%%",  explode = explodeList)
    plt.show()
    
    


# In[42]:


pie_plot(column_name = "store_location", explodeIndex = 0)


# **The sales figures across the three stores are relatively consistent, except for the Lower Manhattan store, where a notable disparity is evident, indicating lower sales compared to the other two stores**

# # The best selling product

# In[45]:


# create function to visualized categorical column using count plot

def count_plot(x_axis = None, y_axis = None, hue = None, rotation = 0, top = None):
    """
    1) input : x_axis, column name, data type must be object or categorical
    3) output : cout plot using seaborn modules, unique values in x-axis and frequency in y-axis
    4) use bar_label to show frequency of each unique values above each column in graph
    5) top parameter i use it to specify indexes i want to see it
    """
    if x_axis: # if we neet to visualized in x-axis
        order = df2[x_axis].value_counts().iloc[:top].index
        
    else : # if we neet to visualized in y-axis
        order = df2[y_axis].value_counts().iloc[:top].index
        
    graph = sns.countplot(x = x_axis, y = y_axis, data = df2, hue = hue, order = order, palette = "RdBu")
    for container in graph.containers:
        graph.bar_label(container)
        
        
    plt.xticks(rotation = rotation)
    plt.show()



# see most common category

# set figure size
plt.figure(figsize = (15,6))

# call function i create it in cell 12
count_plot(x_axis = "product_category")


# In[58]:


sns.displot(df2, x="hour", kind="kde", bw_adjust=3)


# sns.displot(df2, x="hour", hue="product_category", kind="kde")

# In[60]:


sns.displot(df2, x="hour", hue="product_category", kind="kde")


# **We've observed a significant surge in activity during the hours of 7 am to 10 am, and this trend aligns with the popularity of coffee and tea, which are the most commonly consumed beverages in the morning. The data suggests a strong preference for these caffeinated options during this time frame, likely reflecting the morning routine and preferences of our customers.**

# # Product type

# In[72]:


# IDENTIFYING WHICH PRODUCT TYPES ARE SOLD MOST OFTEN!

KP = df2['product_type'].value_counts()

TS = KP.sort_values(ascending=False)

plt.figure(figsize=(15, 4))
TS.plot(kind='bar', color='tan')

plt.xlabel('PRODUCT TYPE')
plt.ylabel('QUANTITY OF SALES')
plt.title('BEST-SELLING PRODUCT TYPES')
plt.show()


# **According to our visual representation, brewed chai tea, gourmet brewed coffee, and barista espresso stand out as the most popular and best-selling products. These items not only capture a significant share of customer preferences but also contribute substantially to overall sales. The data suggests a consistent demand and positive reception for these specific beverages, making them key contributors to the success of product offerings.**

# In[73]:


# Assuming 'counts' is the DataFrame obtained from your groupby operation
counts = df2.groupby(["store_location", "product_type"]).size().reset_index(name = "count")


categories = counts['store_location'].unique()

# Create subplots for each category in a 4x2 grid
fig, axes = plt.subplots(5, 2, figsize = (15, 20))


axes = axes.flatten()

for i, category in enumerate(categories):
    # Filter data for each category
    subset = counts[counts['store_location'] == category]
    
    # Sort the data by 'count' column in descending order
    subset = subset.sort_values('count', ascending = False)
    
    # Create a bar plot for each category with sorted order
    sns.barplot(x = 'count', y = 'product_type', data = subset, ax = axes[i], order = subset['product_type'])
    axes[i].set_title(f'Product Types in {category}')
    axes[i].set_ylabel('')
    axes[i].set_xlabel('')
    axes[i].tick_params(axis = 'x', rotation = 45)
    axes[i].grid(True)
    
    # Adding bar labels
    for idx, bar in enumerate(axes[i].patches):
        axes[i].text(bar.get_width(), bar.get_y() + bar.get_height() / 2, subset.iloc[idx]['count'], ha = 'left', va = 'center')

# Hide extra subplots if there are fewer categories than subplots
for j in range(len(categories), len(axes)):
    axes[j].axis('off')

plt.tight_layout()
plt.show()


# **The detailed comparisons of the popularity rankings for the three most sought-after products in Astonia, Hell's Kitchen, and Lower Manhattan offer valuable insights into regional preferences. In Astonia, brewed chai tea emerges as the most popular, while in Hell's Kitchen, barista espresso takes the lead, and in Lower Manhattan, barista espresso is also the top choice. These location-specific patterns underscore the importance of tailoring product offerings to cater to the distinct tastes of customers in different areas.**

# # The best Store by Revenue

# In[106]:


# Stores Vs Total revenue

# Calculate total revenue for each store_location
revenue = df2.groupby("store_location")["Total_price"].sum().reset_index()

# create bar plot
ax = sns.barplot(x = "store_location", y = "Total_price", data = revenue)
plt.title('BEST SELLING STORE BY REVENUE')
# Adding labels to each bar
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', 
                xytext = (0, 5), textcoords = 'offset points')
    
plt.show()


# **It appears that Hell's Kitchen is the top-performing store in terms of sales, followed by Astonia, and Lower Manhattan coming in last. This sales hierarchy provides a valuable overview of the relative performance of the stores, indicating that Hell's Kitchen is leading in terms of sales, followed by Astonia, with Lower Manhattan having comparatively lower sales.**

# # Best products by revenue

# In[104]:


Tot = df2.groupby('product_type')['Total_price'].sum()

rev = Tot.sort_values(ascending=False)

plt.figure(figsize=(12, 6))
Tot.plot(kind='bar',color='tan')

plt.xlabel('PRODUCT')
plt.ylabel('REVENUE')
plt.title('BEST PRODUCT BY REVENUE')
plt.show()


# **By discerning the products that generate the highest revenue through this analysis, we gain valuable insights into the core drivers of the company's financial performance. Understanding the top-performing products is instrumental in devising targeted marketing strategies, optimizing inventory management, and refining product offerings to meet customer demand. Additionally, this information aids in identifying potential areas for expansion or innovation, ensuring that the company remains competitive and adaptable in the market.**

# # CONCLUSION

# **Upon a comprehensive analysis of sales data, several key insights emerge, contributing to a holistic understanding of the company's performance. Over time, a notable and steady increase in transactions signifies a positive trend in sales activity. This growth could be attributed to favorable customer responses, effective strategies, and the consideration of seasonal influences.**
# 
# **Across the three stores, a relative consistency in sales figures is observed, except for Lower Manhattan, which exhibits lower sales compared to Hell's Kitchen and Astonia. Additionally, a significant surge in activity during the hours of 7 am to 10 am aligns with the popularity of morning beverages such as coffee and tea, reflecting customers' morning routines and preferences.**
# 
# **Visual representations highlight brewed chai tea, gourmet brewed coffee, and barista espresso as the most popular and best-selling products. These items not only capture significant customer preferences but also contribute substantially to overall sales, indicating a consistent demand and positive reception.**
# 
# **Regional preferences further emphasize the importance of tailoring product offerings to different locations. In Astonia, brewed chai tea is the top choice, while in Hell's Kitchen, barista espresso takes the lead. Lower Manhattan exhibits a preference for barista espresso as well, albeit with a lower overall sales performance.**
# 
# **The sales hierarchy positions Hell's Kitchen as the top-performing store, followed by Astonia, with Lower Manhattan having comparatively lower sales. This ranking provides valuable insights into the relative success of each store.**
# 
# **Lastly, identifying products with the highest revenue underscores their pivotal role in shaping the company's financial success. This knowledge facilitates strategic decision-making, allowing for targeted marketing, optimized inventory management, and ongoing innovation to ensure competitiveness in the market.**
# 
# **In conclusion, this multifaceted analysis equips the company with a comprehensive understanding of customer behavior, sales dynamics, and revenue generation. It provides the foundation for informed decision-making and strategic planning to sustain growth and success in the market.**

# In[ ]:




