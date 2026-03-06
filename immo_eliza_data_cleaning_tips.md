# Immo Eliza - data cleaning tips

### **Cleaning tips**

Track provenance of your data and traceability

- Good practice: keep a “raw” dataset and a “cleaned” dataset.
- Build your notebook (develop your cleaning steps) to make it easily reproductible. In other words; if you rerun your notebook cell by cell you’ll always have the same output.

Variable types:

- float variables → for continuous variables (eg: price)
- integers → for categorical variables (ex: nb of rooms) or dummy variables (true/false → 1/0)
- strings → for text variables (ex: address, postal code)
- dates → for dates in “date time” format
- Be carefull with “missing values” at this stage. Ex:  `"N/A"`, `"-"`, `"—"`, `"unknown"`, or empty strings. Replace these with actual “missing values”.

Variable names:

- ensure consistent name of variables (using snake_case is good practice)

Look for (and delete) duplicated listings. Scraped sites often repeat listings across pages.

- based on URL
- based on address
- …

Check missing values:

Check for each **variables** the % of missing values. Prioritize analysis on variables with the least missing values.

If the variable is a critical variable. Eg: there is no price for that listing. 

- Drop the row (delete the house, if it becomes useless for your analysis → depends on your objectives)
- Keep them in the dataset but add a flag like `missing_price = 1` and exclude via filtering when calculating metrics.

You can also check the **number if missing values per row** and decide to flag or delete houses for which you have > x% of missing variables. 

Detect outliers:

Validate with simple consistency checks - try to catch errors. 

Examples:

- bedrooms should typically >= 0
- bathrooms <= bedrooms + some margin (not always true, but catches errors)
- price > 0 € (or even greater than x€)

What to do with outliers? Your own decison! 

1. Check if the value is a real value: is it a real house, or is it most probably a mistake?
    1. If a mistake you can decide to delete it. 
    2. If not a mistake but just an outlier ( eg. a reaaaally expensive house, but a true one) you can keep it. In this case you may decide to create an additional variable (`outliers_flag`) with a “True/False” value whether you believe some variables in this house could bias your analysis because of the outliers. 
    3. Or you can create outliers_flag for each critical variables. Example `price_outliers_flag`, `m2_outliers_flag` …
    
    | url | price | m2 | flag_outliers |
    | --- | --- | --- | --- |
    | https://…. | 630.000 | 250 | 0 |
    | https://…. | 550.000 | 175 | 0 |
    | https://…. | **25.000.000** | 500 | 1 |
    | https://… | 150.000 | **1000** | 1 |

This flag enables you to keep the house in your dataset, but easily remove it from your future analysis as needed. Ex: calculate average price if not an outlier `avg_price = df.loc[df["outliers_flag"] == 0, "price"].mean()`

At this stage, for this kind of exercice, it’s a good practice to familiarize yourself with your dataset and have a look at these outliers. However, in another scenario, when you have huuuuge dataset, it might take too much time, or sometimes it is just impossible to verify (no access to the urls). Then, you might want to adopt a deterministic rule to flag by default all house prices > X € for instance.

### **Statistics reminder**

Correlation measures how strongly two variables move together.

- Positive correlation: as X increases, Y tends to increase.
- Negative correlation: as X increases, Y tends to decrease.
- Near zero: no strong *linear* relationship (there still could be a non-linear one).

Difference between a correlation and a causality:

- **Correlation**: “X and Y vary together.”
- **Causality**: “Changing X produces a change in Y.”

Correlation does **not** imply causation. **Use correlation to find patterns and hypotheses, not to claim causes.**