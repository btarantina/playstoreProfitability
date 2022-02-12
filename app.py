import pandas as pd

#######################################################################################################################
#This simple app will read a static CSV file of Google Play Store App reviews and perform the following modifications:
# 1. Cleanse - remove dupes and listing with invalid ratings
# 2. Enhance - add a gross revenue feature
# 3. Report - report the top 3 apps in each category (by gross revenue)
#######################################################################################################################

# grab the file
print ("Reading the data file")
df = pd.read_csv("googleplaystore.csv")

################
# 1. Cleanse
################

#drop the duplicates
print("trimming category values")
df['Category'].str.strip()
df['App'].str.strip()
print("removing duplicates")
df.drop_duplicates(inplace = True)

print("removing invalid ratings...")
df_clean = df.dropna(subset = ["Rating"])

#swap null values
df_clean.fillna(value={"Installs":0})

# massage some data fields for computations
df_clean["Price"]    = df_clean["Price"].str.replace('Free', "0")
df_clean["Installs"] = df_clean["Installs"].str.replace('Free', "0")
df_clean["Price"]    = df_clean["Price"].str.replace("Everyone", "0")

# strip out the commas and + signs from the Installs ("50,000+" -> "50000")
df_clean["Installs"] = df_clean["Installs"].str.replace(',', "")
df_clean["Installs"] = df_clean["Installs"].str.replace('+', "")

# change the currency to a float.. it would be better to have this as a method if dealing with more than one currency
df_clean["Price"] = df_clean["Price"].str.replace(',','')
df_clean["Price"] = df_clean["Price"].str.replace('$','')

df_clean[["Installs", "Price"]] = df_clean[["Installs", "Price"]].astype(float)

###############################
# 2. Calculate Gross Revenue
###############################
df_clean['Gross Revenue'] = df_clean["Installs"]*df_clean["Price"]

#####################################################
# 3. Report top 3 apps in each category by revenue
#####################################################

df1 = df_clean[['Category','App','Gross Revenue']]
groups = df1.sort_values(['Category', 'Gross Revenue'], ascending=False).groupby(['Category'], group_keys=False).head(n=3)

print(groups.to_string())