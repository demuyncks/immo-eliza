import pandas as pd


def rename_columns(df):
    df.columns = [col.replace(' ', '_').lower() for col in df.columns]
    df.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
    print(df.columns.tolist())


# ________________________________________________________________________________________

def add_index_column(df):
    df["unique_id"] = df.index
    return reposting_column(df, "unique_id", 0)


# ________________________________________________________________________________________


def get_region(zip_code):
    try:
        # Convert to string, then to int to handle potential float/string issues
        z = int(float(zip_code))

        if 1000 <= z <= 1299:
            return "Brussels"
        elif (1300 <= z <= 1499) or (4000 <= z <= 7999):
            return "Wallonia"
        elif (1500 <= z <= 3999) or (8000 <= z <= 9999):
            return "Flanders"
        else:
            return "Unknown"
    except (ValueError, TypeError):
        return None


def define_region_column(df):
    df['region'] = df['zip_code'].apply(get_region)
    df = reposting_column(df, 'region', 4)
    df['region'].value_counts(normalize=True) * 100
    return df


# ________________________________________________________________________________________

def remove_rows_with_nan_values(df, column_name):
    print(f"Total Rows: {df.shape[0]}")

    # 1. Remove rows where column_name is NaN (Not a Number)
    df.dropna(subset=[column_name], inplace=True)

    # 2. Reset the index
    # (Important after dropping rows so your index stays 0, 1, 2...)
    df.reset_index(drop=True, inplace=True)

    # 3. Verify the result
    print(f"Remaining properties in dataset: {len(df)}")


# ________________________________________________________________________________________

def reposting_column(df, column_name, index):
    cols = df.columns.tolist()
    cols.insert(index, cols.pop(cols.index(column_name)))
    return df[cols]


# ________________________________________________________________________________________

def convert_categorical_columns(df, column_name, prefix):
    # Convert the 'Subtype of property' column into binary columns
    column_dummies = pd.get_dummies(df[column_name], prefix=prefix)

    # Join these new columns back to your original dataframe
    return pd.concat([df, column_dummies], axis=1)


def convert_columns_data_type(df, column_name, data_type):
    if data_type == bool:
        # Fill empty cells with 0, then convert to boolean
        df[column_name] = df[column_name].fillna(0).astype(bool)
    df[column_name] = df[column_name].astype(data_type)


def get_non_null_values_percentage(df):
    print("Non null values per column:")
    print(100 - ((df.isnull().sum() / df.shape[0]) * 100).round(2))

def get_correlation_matrix(df, column_name):
    # Calculate correlation only for numeric columns (integers and floats)
    correlations = df.corr(numeric_only=True)[column_name].sort_values(ascending=False)

    print('*' * 50)
    print(f"Correlation with {column_name}:")
    print(correlations)