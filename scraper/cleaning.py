# 01 - Load csv into a df

import pandas as pd
df=pd.read_csv("../data/immo_eliza_final_dataset.csv")

# 02 - Data Cleaning
import re

## Add City column & arrange order

df['City']=''
df=df.loc[:,['URL', 'Zip code','City', 'Locality', 'Type of property', 'Subtype of property', 'Price',
       'Type of sale', 'Number of rooms', 'Living Area',
       'Fully equipped kitchen', 'Furnished', 'Open fire', 'Terrace',
       'Terrace area', 'Garden', 'Garden area', 'Surface of the land',
       'Number of facades', 'Swimming pool', 'State of the building',
       ]]

for index in df.index:

    ## City - Keep only name (from Locality column)
    if pd.notna(df.loc[index, "Locality"]):
        new_value=re.search(r"[A-Za-zÀ-ÿ-]+",df.loc[index,"Locality"])
        df.loc[index,"City"]=new_value.group(0)

    ## Create scale for Fully equipped kitchen
    if pd.notna(df.loc[index, "Fully equipped kitchen"]):
        if df.loc[index,"Fully equipped kitchen"] == "Fully equipped":
            df.loc[index,"Fully equipped kitchen"]=3

        elif df.loc[index,"Fully equipped kitchen"] == "Super equipped":
            df.loc[index,"Fully equipped kitchen"]=2

        elif df.loc[index,"Fully equipped kitchen"] == "Partially equipped":
            df.loc[index,"Fully equipped kitchen"]=1

        elif df.loc[index,"Fully equipped kitchen"] == "Not equipped":
            df.loc[index,"Fully equipped kitchen"]=0

        else:
            print(f"Qualification of kitchen out of scale at {index}")

    ## Create scale for Fully equipped kitchen
    if pd.notna(df.loc[index, "State of the building"]):
        if df.loc[index,"State of the building"] == "New":
            df.loc[index,"State of the building"]=4

        elif df.loc[index,"State of the building"] == "Fully renovated":
            df.loc[index,"State of the building"]=3

        elif df.loc[index,"State of the building"] == "Excellent":
            df.loc[index,"State of the building"]=2

        elif df.loc[index,"State of the building"] == "Normal":
            df.loc[index,"State of the building"]=1

        elif df.loc[index,"State of the building"] == "To renovate" or "To be renovated":
            df.loc[index,"State of the building"]=0

        else:
            print(f"Qualification of renovation out of scale at {index}")

# Convert df values into Int64 (float -> int, keeping NaN)

df = df.convert_dtypes()

# Drop Locality column
df=df.drop("Locality",axis=1)

# Create dictionnaries with scales (kitchen and renovation)
kitchen_scale={0:"Not equipped",1:"Partially equipped",2:"Super equipped",3:"Fully equipped"}
renovation_scale={0:["To renovate","To be renovated"],1:"Normal",2:"Excellent",3:"Fully renovated",4:"New"}

# Store result into csv
df.to_csv("../data/immo_eliza_final_dataset_cleaned.csv")
