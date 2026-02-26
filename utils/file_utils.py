# SAVING RESULTS IN CSV
import csv
import os

import pandas as pd
from numpy.ma.core import empty


def to_csv_file(filepath: str, fieldnames: list, data_list: list) -> None:
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()

        writer = csv.writer(f)
        for data in data_list:
            writer.writerow([data])
    print(f"Total lots collected: {len(data_list)}")
    print(f"CSV file '{filepath}' created successfully.")


def save_to_csv(data, filename):
    """Backs up data incrementally"""
    df = pd.DataFrame(data)
    # If the file does not exist, write the header; otherwise, append to the end.
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)
