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
    df = transform_attributes(df)

    # Store result into csv
    df.to_csv(result_path, index=False)


def transform_attributes(df: pd.DataFrame) -> pd.DataFrame:
    """
        Standardizes the property dataset by extracting geographical data,
        mapping categorical features to numerical scales, and optimizing data types.

        Args:
            df (pd.DataFrame): The raw DataFrame containing scraped property data.

        Returns:
            pd.DataFrame: A cleaned DataFrame with numerical scales and optimized types.
        """
    ## Add City column & arrange order
    df['City'] = ''
    df = df.loc[:, ['URL', 'Zip code', 'City', 'Locality', 'Type of property', 'Subtype of property', 'Price',
                    'Type of sale', 'Number of rooms', 'Living Area',
                    'Fully equipped kitchen', 'Furnished', 'Open fire', 'Terrace',
                    'Terrace area', 'Garden', 'Garden area', 'Surface of the land',
                    'Number of facades', 'Swimming pool', 'State of the building',
                    ]]

    ## City - Keep only name (from Locality column)
    set_city(df)

    ## Create scale for Fully equipped kitchen
    set_equipped_kitchen(df)

    ## Create scale for State of the building
    set_building_state(df)

    # Convert df values into Int64 (float -> int, keeping NaN)
    df = df.convert_dtypes()

    # Drop Locality column
    df = df.drop("Locality", axis=1)

    return df


def set_city(df):
    """
    Extracts the city name from the 'Locality' column.

    Uses a regular expression to capture the first group of letters
    (including accents and hyphens) and saves it in a new 'City' column.
    """
    df['City'] = df['Locality'].str.extract(r'([A-Za-zÀ-ÿ-]+)')


def set_equipped_kitchen(df):
    """
    Converts the kitchen description into a numerical scale from 0 to 3.

    Mapping:
    - Not equipped: 0
    - Partially equipped: 1
    - Super equipped: 2
    - Fully equipped: 3
    """
    kitchen_scale = {
        'Not equipped': 0,
        'Partially equipped': 1,
        'Super equipped': 2,
        'Fully equipped': 3
    }
    df["Fully equipped kitchen"] = df["Fully equipped kitchen"].map(kitchen_scale)


def set_building_state(df):
    """
    Transforms the building's state into an ordinal scale from 0 to 4.

    Groups 'To renovate' and 'To be renovated' under the value 0 to
    standardize properties requiring work.
    """
    building_scale = {
        'New': 4,
        'Fully renovated': 3,
        'Excellent': 2,
        'Normal': 1,
        'To renovate': 0,
        'To be renovated': 0
    }
    df["State of the building"] = df["State of the building"].map(building_scale)
