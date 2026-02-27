import os
from typing import List, Any

import pandas as pd


def to_csv_file(filepath: str, fieldnames: List[str], data_list: List[Any]) -> None:
    """
    Saves collected data to a CSV file, ensuring the target directory exists.

    This function converts the raw results into a Pandas DataFrame for structured
    storage. It automatically creates any missing parent directories to prevent
    FileNotfound errors.

    Args:
        filepath (str): The full path where the CSV should be saved.
        fieldnames (List[str]): The column headers for the CSV.
        data_list (List[Any]): The actual data rows/items collected.
    """

    # 1. Create the directory if it doesn't exist
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Create the missing directory: {directory}")

    # 2. Convert to DataFrame and save
    try:
        df = pd.DataFrame(data=data_list, columns=fieldnames)
        df.to_csv(filepath, index=False, encoding='utf-8')

        print(f"Mission Success: {len(data_list)} items secured in '{filepath}'")

    except Exception as e:
        print(f"Critical Error saving to CSV: {e}")


def save_to_csv_incremental(data: List[Any], filename: str) -> None:
    """
    Backs up data incrementally to a CSV file to prevent data loss during long runs.

    Args:
        data (List[Any]): The new batch of data to append.
        filename (str): The target file path.
    """
    df = pd.DataFrame(data)
    file_exists = os.path.isfile(filename)

    # Append mode ('a') with header only if the file is being created
    df.to_csv(filename, mode='a', index=False, header=not file_exists, encoding='utf-8')
