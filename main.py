import datetime
import sys

import pandas as pd

from scraper.cleaning import run_cleaner
from scraper.crawler import run_optimized_crawling
from scraper.parser import run_optimized_scraping
from utils.interface_utils import start_mission_control, execute_mission


def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%Hh%M")
    urls_list_path = f"data/properties_urls_{timestamp}.csv"
    dataset_path = f"data/properties_dataset_{timestamp}.csv"
    cleand_dataset_path = f"data/cleaned_properties_dataset_{timestamp}.csv"

    while True:
        # Retrieve the agent's selection from the CLI menu
        choice = start_mission_control()

        # Dispatch the mission based on user input
        if choice == 1:
            # Launch the URL collection process
            execute_mission("CRAWLING", run_optimized_crawling, urls_list_path)

        elif choice == 2:
            # Launch the data extraction process
            execute_mission("SCRAPING", run_optimized_scraping, urls_list_path, dataset_path)

        elif choice == 3:
            # Launch the data cleaning process
            execute_mission("CLEANING", run_cleaner, dataset_path, cleand_dataset_path)

        elif choice == 0:
            print("\n👋 Deactivating Agency systems... Standby for shutdown.")
            sys.exit(0)
        # Provide visual feedback before restarting the loop
        print("\n" + "." * 50)
        print("Mission accomplished. Returning to Mission Control...")
        print("." * 50 + "\n")


# THIS IS THE GUARD:
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Agent logout. Agency closing...")
        sys.exit()
