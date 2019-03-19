
# coding: utf-8
# In[1]:


import numpy as np
import pandas as pd


# In[2]:


autos = pd.read_csv('autos.csv', encoding='Latin-1')
print(autos.info())
print(autos.describe(include='all'))


# The dataset contains 20 columns, most of which are strings. Columns "vehicleType", "gearbox", "model", "fuelType", and "notRepairedDamage" contain some null values. Some numeric data presented in str format (columns "dateCrawled", "price", "odometer", "dateCreated", "lastSeen").

# In[3]:


# Format columns of the dataframe
autos.columns = ['date_crawled', 'name', 'seller',
                 'offer_type', 'price', 'abtest',
                 'vehicle_type', 'registration_year',
                 'gearbox', 'power_ps', 'model', 'odometer',
                 'registration_month', 'fuel_type', 'brand',
                 'unrepaired_damage', 'ad_created',
                 'nr_of_pictures', 'postal_code', 'last_seen']


# Columns 'seller', 'offer_type', 'abtest', and 'nr_of_pictures' have mostly one value and can be dropped. Columns that need more investigation:
# - 'name' (car model can be extract from this column);
# - 'price' (need to be cleanded, the most frequent value is zero);
# - 'odometer_km (need to be cleaned);
# - 'vehicle_type' and 'unrepaired_damage'(some words are in German);
# - 'registration year"(unsual min and max values);
# - 'power_ps"(unsual min and max values);
# - Numeric data presented in str format (columns 'date_crawled', 'price", 'odometer', 'date_created', 'last_seen') need to be evaluated;

# In[4]:


# Drop columns 'seller', 'offer_type', 'abtest',
# and'nr_of_pictures'
autos = autos.drop(
    ['seller', 'offer_type', 'abtest', 'nr_of_pictures'],
    axis=1)


# In[5]:


# Explore data in the column 'name'
print(autos['name'].value_counts())


# We can see from the data that in most cases the second word is the model of the car. Let's extract the model and store it in the separate column. 

# In[6]:


# Extract models from name column
autos['model'] = autos['name'].str.split('_', expand=True).iloc[:, 1]
print(autos[['brand','model']].head(20))


# Now the data can be aggregated based on brand and model which will be done later.

# In[7]:


# Clean data in column 'price' and print some statisctis
autos['price'] = (autos['price']
                  .str.replace('$', '')
                  .str.replace(',', '')
                 .astype(float))

print(autos['price'].unique().shape[0])
print(autos['price'].describe())


# Column 'price' contains 2357 unique values. There are unusually min values(0) and unusually max values(8e+08). Based on descriptive statistic the distribution is skewed to the right with some outliers. Let's define a function which will remover outliers. 

# In[8]:


# Definition of function 'remove_outliers'
def remove_outliers(dataset, column):
    return dataset[
        np.abs(dataset[column] - dataset[column].mean()
              ) <= 3*dataset[column].std()]


# In[9]:


# Remove rows with outliers based on column 'price'
autos = remove_outliers(autos, 'price')
print(autos['price'].unique().shape[0])
print(autos['price'].describe())


# In[10]:


# Clean data in column 'odometer', rename the column
autos['odometer'] = (autos['odometer']
                    .str.replace('km', '')
                    .str.replace(',', '')
                    .astype(float))
autos.rename({'odometer': 'odometer_km'},
             axis=1,
             inplace=True)
print(autos['odometer_km'].unique().shape[0])
print(autos['odometer_km'].describe())


# Column 'odometer_km' contains 13 unique values. There are no unusual values. The distribution is skewed to the left, most of the data is located between 125000 and 150000. Now let's translate some German words in English. 

# In[11]:


# Some words in column 'vehicle type' are in German language. Let's
# replace them with English ones. 
mapping = {'limousine': 'limousine',
           'kleinwagen': 'supermini',
           'kombi': 'station wagon',
           'bus': 'bus',
           'cabrio': 'cabrio',
           'coupe': 'coupe',
           'suv': 'suv',
           'andere': 'other'}
autos['vehicle_type'] = autos['vehicle_type'].map(mapping)
print(autos['vehicle_type'].value_counts())


# In[12]:


# 'unrepaired_damage' contains German words.
# Replace them with English. 
mapping = {'ja': 'yes',
          'nein': 'no'}
autos['unrepaired_damage'] = autos['unrepaired_damage'].map(
mapping)
print(autos['unrepaired_damage'].value_counts())


# In[13]:


# Explore data in registration year column
print(autos['registration_year'].describe())


# The 50% of data falls between 1999 and 2008. However, there are unusual values such as 1000 and 9999 which is invalid for the year. There are some outliers which should be dropped. We will use the function 'remove_outliers'.

# In[14]:


# Remove rows with outliers from dataset based on 
# 'registration_year' column
autos = remove_outliers(autos, 'registration_year')
print(autos['registration_year'].describe())


# Because a car can't be first registered before the listing was seen, any vehicle with a registration year above 2016 is definitely inaccurate and should also be removed. The production of petrol engines for automobiles was started in 1886. So, we can drop all years before 1886 and after 2016. 

# In[15]:


# Drop rows with years before 1886 and 2016
autos = autos[autos['registration_year']
              .between(1886, 2016)]

# Calculate distribution of the remaining values
print(autos['registration_year']
      .value_counts(normalize=True, dropna=False)
      .sort_index())


# We can see that the majority of the cars were registered in 1994-2016, however, all other values preserved for the sanity of analysis. The next column to examine is "power_ps".

# In[16]:


# Print descriptive statistics of the column and count
# unique values
print(autos['power_ps'].describe())
print(autos['power_ps'].value_counts().head(10))


# There are some unusually large values and unusually small. Let's removed outlier using remove_outliers function. As the number of zeros is large we will replace them with the mean for all other data. The car with smallest horsepower I could found is Peel P50 with 4.2 ps. So, we will also replace values with the mean that is smaller than 5. 

# In[17]:


# Remove rows with outliers based on column 'power_ps' and replace zeros
# replace small values with mean of other cells. 
autos = remove_outliers(autos, 'power_ps')

autos.loc[autos['power_ps']  < 4, 'power_ps'] = autos.loc[
    autos['power_ps'] >= 4, 'power_ps'].mean()

print(autos['power_ps'].describe())
print(autos['power_ps'].value_counts().head(10))


# Now let's look at the data in columns 'date_crawled', 'ad_created', and 'last_seen'.

# In[18]:


# Print example data from columns
print(autos[['date_crawled',
             'ad_created',
             'last_seen']].head())


# We can extract dates from columns 'date_crawled', 'ad_created', and 'last_seen' using str[:] slice. 

# In[19]:


print(autos['date_crawled'].str[:7].value_counts(
normalize=True, dropna=False).sort_index())


# The 83.7% of data was crawled on March 2016.

# In[20]:


print(autos['ad_created'].str[:7].value_counts(
normalize=True, dropna=False).sort_index())


# The 83.7% of data was created on March 2016.

# In[21]:


print(autos['last_seen'].str[:7].value_counts(
normalize=True, dropna=False).sort_index())


# Although most of the data was created on March 2016 this adds are still interesting for potential buyers as more than a half of it was seen in April. Now let's proceed with analysis.

# In[22]:


# Examining brand column
top_all = autos['brand'].value_counts(
normalize=True,
dropna=False)
print(top_all)


# The data will be aggregated on the top ten brands.

# In[23]:


# Find the mean price for each of top 10 brands
price_agg = {}
for brand in top_all.index[:10]: 
    price_agg[brand] = autos.loc[
        autos['brand'] == brand, 'price'].mean()
print(sorted(price_agg.items(),
   key=lambda x: x[1],reverse=True))


# There is a significant price gap in the top 10 brands. 'audi', 'mercedes_benz', and 'bmw' are the most expensive. 'volkswagen', 'seat' and 'ford' are less expensive. 'peugeot', 'opel', 'fiat', and 'renault' are the cheapest. We will look if the price of the brands depends on the mileage. 

# In[24]:


# Find the mean price for each of top 10 brands
mileage_agg = {}
for brand in top_all.index[:10]:
    mileage_agg[brand] = autos.loc[
        autos['brand'] == brand, 'odometer_km'
    ].mean()
print(sorted(mileage_agg.items(),
            key=lambda x: x[1],
            reverse=True))


# In[25]:


# Convert both dictionaries two the series objects
price_series = pd.Series(price_agg)
mileage_series = pd.Series(mileage_agg)


# In[26]:


price_mileage = pd.DataFrame({'price': price_series,
                 'odometer_km': mileage_series})
print(price_mileage.sort_values(by=['odometer_km']))


# We can see from the aggregate data that the price of the brands does not depend on mileage. In a normal situation the relationship should be negative (the more a mileage the less a price). However, the opposite trend can be seen from this data. It seems like a price depends on the brand of the car.

# In[27]:


# Find the most common brand/model combinations
top_brands = []
top_models =  autos['model'].value_counts().head(10).index
for model in top_models:
    brand = autos.loc[autos['model'] == model, 'brand']
    top_brands.append(brand.iloc[0])

top_brand_model = pd.DataFrame({'top_brands': pd.Series(top_brands),
                               'top_models': pd.Series(top_models)})
print(top_brand_model)


# We can see the top 10 brand/model combinations. For further analysis, the data for mercedes_bens can be investigated more carefully. 

# We will explore the "odometer_km" column to see if the price is dependent on mileage. We know that the minimum value is 5000 and the maximum value is 150000. We define the following groups to explore:
# - 5000-7499 (group1);
# - 7500-9999 (group2);
# - 10000-12499 (group3);
# - 12500-15000 (gropu4);

# In[28]:


# Split 'odometer_km' on groups based on mileage and
# create a dictionary which contains average price for
# each group
splits = {'group1': [5000, 74999],
         'group2': [75000, 99999],
         'group3': [100000, 124999],
         'group4': [125000, 150000]
         }
price_groups = {}

for group in splits:
    price_groups[group] = autos.loc[
        autos['odometer_km'].between(
            splits[group][0],
            splits[group][1]),
        'price'
    ].mean()

print(price_groups)


# We can see from this data that the mileage and the price have a negative relationship: the bigger the mileage, the less the price. Our next step is to analyze the dependence of price from damage. From the previous steps, we know that there are two values in this column: 'yes' and 'no'. Let's see if the average price differs for each group.

# In[29]:


damage_groups = {}
for group in ['yes', 'no']:
    damage_groups[group] = autos.loc[
        autos['unrepaired_damage'] == group, 'price'
    ].mean()
print(damage_groups)


# We can see from the data that damaged cars is cheaper than non-damaged cars. 
# 
# Here is the outcome for our analysis:
# - the price depends on the brand, mileage (negative relationship), and damage (negative relationship);
# - top ten brand/model combinations are presented;
