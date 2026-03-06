import pandas as pd

from analyse.data_cleaning import remove_rows_with_nan_values, rename_columns, add_index_column, \
    define_region_column, convert_categorical_columns, convert_columns_data_type, get_non_null_values_percentage, \
    get_correlation_matrix

# ________________________________________________________________________________________
path = './data/cleaned_properties_dataset_2026-03-04_10h12.csv'
df = pd.read_csv(path)
# ________________________________________________________________________________________

# ________________________________________________________________________________________

rename_columns(df)
df = add_index_column(df)
df = define_region_column(df)

# ________________________________________________________________________________________

# ________________________________________________________________________________________

remove_rows_with_nan_values(df, 'price')
remove_rows_with_nan_values(df, 'living_area')

# ________________________________________________________________________________________

# ________________________________________________________________________________________
df = convert_categorical_columns(df, 'region', 'region')
df = convert_categorical_columns(df, 'type_of_property', 'property_type')
df = convert_categorical_columns(df, 'subtype_of_property', 'property_subtype')
df = convert_categorical_columns(df, 'type_of_sale', 'sale_type')
# df = convert_categorical_columns(df, 'city', 'city')
# ________________________________________________________________________________________

# ________________________________________________________________________________________
# convert_columns_data_type(df, 'zip_code', str)

convert_columns_data_type(df, 'number_of_rooms', 'Int64')
convert_columns_data_type(df, 'fully_equipped_kitchen', 'Int64')
convert_columns_data_type(df, 'number_of_facades', 'Int64')
convert_columns_data_type(df, 'state_of_the_building', 'Int64')

convert_columns_data_type(df, 'furnished', bool)
convert_columns_data_type(df, 'open_fire', bool)
convert_columns_data_type(df, 'terrace', bool)
convert_columns_data_type(df, 'garden', bool)
convert_columns_data_type(df, 'swimming_pool', bool)
# ________________________________________________________________________________________

print(df.info())

get_non_null_values_percentage(df)

get_correlation_matrix(df,'price')
get_correlation_matrix(df, 'living_area')
get_correlation_matrix(df, 'region_Wallonia')
