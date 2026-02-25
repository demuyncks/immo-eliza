# Remove the "project properties" from all_properties_urls.csv

import pandas as pd
import re

## Load the csv
df=pd.read_csv("../data/all_properties_urls.csv")

## If "project" in the url and remove the row
pattern="/projectdetail/"
compiled=re.compile(pattern)
for index in df.index:
    if compiled.search(df.loc[index,"property_url"]):
        df.drop(index,inplace=True)

df.to_csv("../data/all_properties_urls_without_projects.csv",index=False)

# ...
