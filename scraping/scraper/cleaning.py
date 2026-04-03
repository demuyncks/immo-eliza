import numpy as np
import pandas as pd


def run_cleaner(dataset_filename: str, result_path: str):
    """
    Loads a raw real estate dataset, applies transformations, and saves the cleaned version.

    Args:
        dataset_filename (str): The path to the raw CSV file containing scraped property data.
        result_path (str): The destination path where the cleaned CSV will be saved.

    Returns:
        None
    """
    # 01 - Load csv into a df
    df = pd.read_csv(dataset_filename)

    # Apply data transformations (City extraction, scaling, etc.)
    df = data_cleaning_process(df)

    # Store result into csv
    df.to_csv(result_path, index=False)


def data_cleaning_process(df: pd.DataFrame) -> pd.DataFrame:
    """
        Standardizes the property dataset through a sequence of cleaning and
        feature engineering steps focused on the Belgian real estate market.

        The pipeline handles data integrity, ordinal encoding, geographical
        mapping, and type optimization in a specific logical order.

        Args:
            df (pd.DataFrame): The raw DataFrame containing scraped property data
                with columns such as 'price', 'living_area', and 'locality'.

  Returns:
        pd.DataFrame: A cleaned and optimized DataFrame ready for
            statistical analysis and machine learning models.
    """

    # 1. Basic Structural Cleaning
    df = rename_columns(df)
    df = drop_duplicate_rows(df)
    df = strip_string_columns(df)

    # 2. Attribute Synchronization
    df = synchronize_garden_attributes(df)
    df = synchronize_terrace_attributes(df)

    # 3. Categorical Encoding (Ordinal Scales)
    df = encode_kitchen_quality(df)
    df = encode_building_condition(df)

    # 4. Geographical Data Extraction
    df = extract_city_from_locality(df)
    df = assign_belgian_provinces(df)  # Moves province column to index 3
    df = assign_belgian_region(df)  # Moves region column to index 4

    # 5. Data Type Optimization
    # Ensures existing columns are in nullable Int64 or bool early on
    df = optimize_dataframe_types(df)

    # 6. Missing Value Handling & Filtering
    # Remove rows missing target price first
    df = drop_missing_values(df, 'price')
    # Filter out extreme outliers in living area
    df = filter_minimum_living_area(df, min_area=10)

    # 7. Feature Engineering
    # price_sqm is calculated and moved to index 7
    df = calculate_price_per_sqm(df)

    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes DataFrame column names for easier programmatic access.

    The transformation includes:
    1. Removing leading and trailing whitespace.
    2. Replacing internal spaces with underscores.
    3. Converting all characters to lowercase.

    Args:
        df (pd.DataFrame): The original DataFrame with raw column names.

    Returns:
        pd.DataFrame: The DataFrame with standardized column names.
    """
    # Use the .str accessor for efficient string manipulation on the index (columns)
    # strip() removes outer spaces, replace() handles inner spaces, lower() sets the case
    df.columns = (
        df.columns.str.strip()
        .str.replace(' ', '_')
        .str.lower()
    )

    return df


def drop_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies and removes duplicate rows from the DataFrame.

    This step ensures the dataset meets the 'minimum 10,000 unique inputs'
    requirement for the ImmoEliza project.

    Args:
        df (pd.DataFrame): The DataFrame containing raw property data.

    Returns:
        pd.DataFrame: A cleaned DataFrame with unique rows and a reset index.
    """
    # Count the number of duplicate entries before removal
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        print(f"🔍 Found {duplicate_count} duplicate rows. Removing them...")
        # Remove duplicates and reset the index to keep it continuous
        df_cleaned = df.drop_duplicates().reset_index(drop=True)
        print("✅ Duplicates removed successfully.")
        return df_cleaned

    print("✨ No duplicates found in the dataset.")
    return df


def strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes leading and trailing whitespace from all string/object columns.

    This ensures data consistency as required by the ImmoEliza cleaning
    guidelines (e.g., " I love python " becomes "I love python").

    Args:
        df (pd.DataFrame): The DataFrame to be cleaned.

    Returns:
        pd.DataFrame: The DataFrame with whitespace removed from string values.
    """
    # Identify columns that contain string-like data (object or string dtypes)
    string_cols = df.select_dtypes(include=['object', 'string']).columns

    # Apply the strip operation to the identified columns
    # We use .str.strip() which is a vectorized pandas operation
    df[string_cols] = df[string_cols].apply(lambda x: x.str.strip())

    print(f"🧹 Cleaned whitespace from {len(string_cols)} columns: {list(string_cols)}")

    return df


def synchronize_garden_attributes(df) -> pd.DataFrame:
    """
    Ensures logical consistency between 'garden' (boolean-like) and 'garden_area' columns.

    Logic:
    1. If area > 0, set 'garden' to 1.
    2. If 'garden' is 1 but area is 0 or NaN, set area to NaN (for later imputation).
    3. If 'garden' is 0, set 'garden_area' to 0.

    Args:
        df (pd.DataFrame): Dataframe containing 'garden' and 'garden_area'.

    Returns:
        pd.DataFrame: Dataframe with synchronized garden attributes.
    """
    # 1. Infer existence: If area is positive, a garden must exist
    df.loc[df['garden_area'] > 0, 'garden'] = 1

    # 2. Prepare for imputation: If garden exists but area is unknown/zero,
    # set to NaN so it doesn't bias the mean/median calculations later.
    missing_area_mask = (df['garden'] == 1) & ((df['garden_area'] == 0) | (df['garden_area'].isna()))
    df.loc[missing_area_mask, 'garden_area'] = np.nan

    # 3. Enforce absence: If no garden exists, the area must be 0
    df.loc[df['garden'] == 0, 'garden_area'] = 0

    return df


def synchronize_terrace_attributes(df) -> pd.DataFrame:
    """
    Standardizes the relationship between 'terrace' (flag) and 'terrace_area' (numeric).

    Logic:
    1. If terrace_area > 0, set 'terrace' to 1.
    2. If 'terrace' is 1 but area is 0 or NaN, set area to NaN for later imputation.
    3. If 'terrace' is 0, explicitly set 'terrace_area' to 0.

    Args:
        df (pd.DataFrame): Input dataframe with terrace-related columns.

    Returns:
        pd.DataFrame: A modified dataframe with consistent terrace data.
    """
    # 1. Flag existence based on area
    df.loc[df['terrace_area'] > 0, 'terrace'] = 1

    # 2. Identify and flag missing measurements for existing terraces
    # This avoids including '0' in future statistical calculations (mean/median)
    missing_area_mask = (df['terrace'] == 1) & (
            (df['terrace_area'] == 0) | (df['terrace_area'].isna())
    )
    df.loc[missing_area_mask, 'terrace_area'] = np.nan

    # 3. Enforce zero area where no terrace exists
    df.loc[df['terrace'] == 0, 'terrace_area'] = 0

    return df


def encode_kitchen_quality(df) -> pd.DataFrame:
    """
    Transforms the 'fully_equipped_kitchen' categorical data into an ordinal scale.

    The mapping reflects the quality/completeness of the kitchen setup.
    Missing values are imputed with 1 (Partially equipped) as a conservative baseline.

    Scale:
    - 0: Not equipped
    - 1: Partially equipped (Default for NaN)
    - 2: Super equipped
    - 3: Fully equipped
    """
    # Define the ordinal hierarchy
    kitchen_scale = {
        'Not equipped': 0,
        'Partially equipped': 1,
        'Super equipped': 2,
        'Fully equipped': 3
    }

    # Map the strings to integers
    df["fully_equipped_kitchen"] = df["fully_equipped_kitchen"].map(kitchen_scale)

    # Impute missing values:
    # Filling with 1 assumes a basic level of equipment if not specified.
    df['fully_equipped_kitchen'] = df['fully_equipped_kitchen'].fillna(1)

    return df


def encode_building_condition(df) -> pd.DataFrame:
    """
    Ordinal encoding for 'state_of_the_building' based on current dataset values.

    Mapping Strategy:
    - 4: New / Under construction
    - 3: Fully renovated / Excellent
    - 2: Normal
    - 1: To renovate / To be renovated / To restore
    - 0: To demolish
    """
    building_scale = {
        'New': 4,
        'Under construction': 4,
        'Fully renovated': 3,
        'Excellent': 3,  # Grouped with fully renovated for high quality
        'Normal': 2,
        'To be renovated': 1,
        'To renovate': 1,
        'To restore': 1,
        'To demolish': 0
    }

    # Map the strings to integers
    df["state_of_the_building"] = df["state_of_the_building"].map(building_scale)

    # Handling the 2,709 null values:
    # Filling with 2 (Normal) is a safe median choice so the rows stay useful.
    df['state_of_the_building'] = df['state_of_the_building'].fillna(2).astype('Int64')

    return df


def extract_city_from_locality(df) -> pd.DataFrame:
    """
    Parses the 'locality' column to extract the primary city name.

    Uses regex to capture the first sequence of alphabetic characters,
    including accented characters and hyphens, while removing postal codes
    or extra strings.

    Args:
        df (pd.DataFrame): Input dataframe with a 'locality' column.

    Returns:
        pd.DataFrame: Dataframe with a new 'city' column and 'locality' removed.
    """

    # Regex breakdown: ([A-Za-zÀ-ÿ-]+)
    # Captures uppercase, lowercase, accented letters, and hyphens.
    df['city'] = df['locality'].str.extract(r'([A-Za-zÀ-ÿ-]+)')

    # Drop the raw locality column as it's now redundant
    df = df.drop("locality", axis=1)

    # Reorder the column to a specific index (2) for better visibility
    df = reorder_column_position(df, "city", 2)

    return df


def optimize_dataframe_types(df) -> pd.DataFrame:
    """
    Standardizes and optimizes data types across the property dataframe.

    Converts features to nullable integers (Int64) for counts and
    standard booleans for flags, ensuring memory efficiency and
    imputation readiness.
    """
    # Automatically infer the best possible types (e.g., objects to strings)
    df = df.convert_dtypes()

    # Integer columns (using nullable Int64 to preserve NaNs)
    int_cols = [
        'number_of_rooms', 'fully_equipped_kitchen',
        'number_of_facades', 'state_of_the_building'
    ]
    for col in int_cols:
        df = cast_column_type(df, col, 'Int64')

    # Boolean columns
    bool_cols = [
        'furnished', 'open_fire', 'terrace',
        'garden', 'swimming_pool'
    ]
    for col in bool_cols:
        df = cast_column_type(df, col, bool)

    return df


def cast_column_type(df, column_name, data_type) -> pd.DataFrame:
    """
    Safely casts a specific column to the target data type.

    Args:
        df (pd.DataFrame): The dataframe to modify.
        column_name (str): The column to cast.
        data_type: The target type (e.g., 'Int64', bool, str).
    """
    if column_name not in df.columns:
        return df

    if data_type == bool:
        # Fill missing flags with False/0 before converting to boolean
        df[column_name] = df[column_name].fillna(0).astype(bool)
    else:
        df[column_name] = df[column_name].astype(data_type)

    return df


def assign_belgian_region(df) -> pd.DataFrame:
    """
    Creates a 'region' column based on postal codes and reorders it for clarity.

    Args:
        df (pd.DataFrame): Dataframe containing 'zip_code'.

    Returns:
        pd.DataFrame: Dataframe with the localized region assigned.
    """
    if 'zip_code' not in df.columns:
        print("Error: 'zip_code' column missing.")
        return df

    # Map postal codes to administrative regions
    df['region'] = df['zip_code'].apply(map_zip_to_region)

    # Shift column to the 4th index for better visual grouping with location data
    df = reorder_column_position(df, 'region', 4)

    return df


def map_zip_to_region(zip_code):
    """
    Categorizes a Belgian postal code into its administrative region.

    Logic:
    - 1000-1299: Brussels-Capital
    - 1300-1499, 4000-7999: Wallonia
    - 1500-3999, 8000-9999: Flanders
    """
    try:
        # Cast to int to handle strings or floats (e.g., 1000.0)
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
        # Returns None for invalid data to facilitate easier cleaning later
        return None


def assign_belgian_provinces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches the dataset with Belgian province names by merging with a lookup table.

    Args:
        df (pd.DataFrame): The main property DataFrame.

    Returns:
        pd.DataFrame: DataFrame with an added 'province' column.
    """
    # Load the lookup table
    provinces_lookup = get_zip_mapping_df()

    # Standardize types to ensure the merge key matches perfectly
    # Using 'Int64' to handle any potential missing zip codes gracefully
    df['zip_code'] = df['zip_code'].astype("Int64")
    provinces_lookup['zip_code'] = provinces_lookup['zip_code'].astype("Int64")

    # Merge the Province data
    # We use a left join to keep all properties, even if the zip isn't in the lookup
    df = df.merge(
        provinces_lookup[['zip_code', 'province']],
        on='zip_code',
        how='left'
    )

    # Position the new 'province' column at index 3 (next to region)
    df = reorder_column_position(df, 'province', 3)

    return df


def get_zip_mapping_df() -> pd.DataFrame:
    """
    Creates a clean lookup table for Zip codes to Provinces in English.
    """
    path_prov = "./data/reference/provinces_zip.csv"

    try:
        df_ref = pd.read_csv(path_prov)
    except FileNotFoundError:
        print(f"Error: Province mapping file not found at {path_prov}")
        return pd.DataFrame(columns=['zip_code', 'province'])

    # Mapping Dutch/French source names to English for consistency in your report
    translation = {
        "Limburg": "Limburg", "Luxemburg": "Luxembourg", "Oost-Vlaanderen": "East Flanders",
        "West-Vlaanderen": "West Flanders", "Vlaams-Brabant": "Flemish Brabant",
        "Antwerpen": "Antwerp", "Luik": "Liege", "Namen": "Namur",
        "Henegouwen": "Hainaut", "Waals-Brabant": "Walloon Brabant", "Brussel": "Brussels"
    }

    # Standardize column names to snake_case to match your main dataframe
    df_ref = df_ref.rename(columns={'zipCode': 'zip_code', 'province': 'province_raw'})

    # Map to English names
    df_ref['province'] = df_ref['province_raw'].map(translation)

    # Remove duplicates to ensure a 1-to-1 mapping for the merge
    mapping_df = df_ref[['zip_code', 'province']].drop_duplicates(subset=['zip_code'])

    return mapping_df


def drop_missing_values(df, column_name) -> pd.DataFrame:
    """
    Removes rows where the specified column contains NaN values.

    This is used for critical features where imputation is not appropriate,
    ensuring the model only trains on verified data points.

    Args:
        df (pd.DataFrame): The dataframe to process.
        column_name (str): The specific column to check for nulls.

    Returns:
        pd.DataFrame: The cleaned dataframe.
    """
    if column_name not in df.columns:
        print(f"Warning: Column '{column_name}' not found. No rows removed.")
        return df

    initial_count = len(df)

    # 1. Remove rows where column_name is NaN
    # We return the result to avoid SettingWithCopy warnings in some contexts
    df = df.dropna(subset=[column_name])

    # 3. Verify and report the result
    removed_count = initial_count - len(df)
    print(f"Cleaning complete for '{column_name}':")
    print(f" - Removed {removed_count} rows.")
    print(f" - Total remaining: {len(df)} rows.")

    return df


def filter_minimum_living_area(df, min_area=10) -> pd.DataFrame:
    """
    Filters out properties with a living area below a specified threshold
    while preserving rows with missing (NaN) values.

    Args:
        df (pd.DataFrame): The input dataframe containing a 'living_area' column.
        min_area (int, optional): The minimum allowed area. Defaults to 10.

    Returns:
        pd.DataFrame: A filtered copy of the original dataframe.
    """
    # Create a boolean mask:
    # 1. Keep values greater than or equal to the threshold
    # 2. Keep null values (NaN) to avoid accidental data loss
    keep_mask = (df['living_area'] >= min_area) | (df['living_area'].isna())

    # Apply the mask to create the cleaned dataframe
    filtered_df = df[keep_mask].copy()

    # Calculate and report processing stats
    removed_count = len(df) - len(filtered_df)
    print(f"Filtering complete. Removed {removed_count} rows with area < {min_area}m².")
    print(f"Rows remaining: {len(filtered_df)}")

    return filtered_df


def calculate_price_per_sqm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates price per square meter and positions the column for analysis.

    Standardizes property value across different sizes and handles
    division-by-zero errors by treating 0m² areas as NaN.

    Args:
        df (pd.DataFrame): Dataframe with 'price' and 'living_area'.

    Returns:
        pd.DataFrame: Dataframe with 'price_sqm' rounded and reindexed.
    """
    # Replace 0 with NaN to avoid 'inf' results during division
    temp_area = df['living_area'].replace(0, np.nan)

    # Calculate engineered feature
    df['price_sqm'] = df['price'] / temp_area

    # Round and cast to nullable Int64 to maintain integer consistency
    df['price_sqm'] = df['price_sqm'].round().astype('Int64')

    # Reorder the column to index 6 for better data visibility
    # We assign the result to df to ensure the new column order persists
    df = reorder_column_position(df, 'price_sqm', 7)

    return df


def reorder_column_position(df, column_name, index):
    """
    Moves a specific column to a new index position within the DataFrame.

    This is a structural utility used to keep related features (like City, Region)
    at the beginning of the DataFrame for better readability during analysis.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        column_name (str): The name of the column to move.
        index (int): The target position (0-based) for the column.

    Returns:
        pd.DataFrame: A new DataFrame with the columns reordered.
    """
    # Extract the current list of columns
    cols = df.columns.tolist()

    try:
        # Remove the column from its current position and insert it at the target index
        cols.insert(index, cols.pop(cols.index(column_name)))
    except ValueError:
        print(f"Error: Column '{column_name}' not found in DataFrame.")
        return df

    return df[cols]


# ________________________________________________________________________________________


def preprocess_categorical_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Orchestrates the encoding for all categorical variables in the ImmoEliza dataset.

    Args:
        df: The cleaned DataFrame containing property data.

    Returns:
        The DataFrame with all categorical features converted to numerical dummies.
    """
    # We apply the encoding to each relevant categorical column
    df = encode_categorical_feature(df, 'region', 'region')
    df = encode_categorical_feature(df, 'type_of_property', 'property_type')
    df = encode_categorical_feature(df, 'subtype_of_property', 'property_subtype')
    df = encode_categorical_feature(df, 'type_of_sale', 'sale_type')

    return df


def encode_categorical_feature(df: pd.DataFrame, column_name: str, prefix: str) -> pd.DataFrame:
    """
    Applies One-Hot Encoding to a specific column and joins it back to the DataFrame.

    Args:
        df: The input pandas DataFrame.
        column_name: The name of the column to transform.
        prefix: String to prepend to the new binary column names.

    Returns:
        A DataFrame with the original column and new binary dummy columns.
    """
    # Create binary (dummy) columns: 1 for presence, 0 for absence
    column_dummies = pd.get_dummies(df[column_name], prefix=prefix)

    # Combine the new columns with the existing data
    return pd.concat([df, column_dummies], axis=1)


def add_price_range_column(df):
    # Group by our previously created 'Price Range'
    financial_analysis = df.groupby('price_range')['price'].agg(['count', 'sum'])

    # Calculate the percentage of total money
    total_money = financial_analysis['sum'].sum()
    financial_analysis['value_percentage'] = (financial_analysis['sum'] / total_money) * 100

    return financial_analysis


def get_non_null_values_percentage(df):
    print("Non null values per column:")
    print(100 - ((df.isnull().sum() / df.shape[0]) * 100).round(2))


def get_correlation_matrix(df, column_name):
    # Calculate correlation only for numeric columns (integers and floats)
    correlations = df.corr(numeric_only=True)[column_name].sort_values(ascending=False)

    print('*' * 50)
    print(f"Correlation with {column_name}:")
    print(correlations)


def add_index_column(df):
    df["unique_id"] = df.index
    return reorder_column_position(df, "unique_id", 0)

# ________________________________________________________________________________________
