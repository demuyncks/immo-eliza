import time
from time import perf_counter

import pandas as pd

from scraper.parser import run_optimized_scraping

print("_________________________________SCRAPING______________________________________")
start_time = perf_counter()

url = "https://immovlan.be/en"

final_filename = "data/immo_eliza_final_dataset.csv"

list_urls = pd.read_csv("data/all_properties_urls_without_projects.csv")["property_url"].tolist()

run_optimized_scraping(list_urls, final_filename)

print("______________________________________________________________________________")
print(f"Ended in {(time.perf_counter() - start_time) / 60:.1f} minutes.")
print(f"Total number of properties collected : {len(list_urls)}")
