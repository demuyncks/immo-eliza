import sys

import pandas as pd

from scraper.cleaning import run_cleaner
from scraper.crawler import run_optimized_crawling
from scraper.parser import run_optimized_scraping
from utils.interface_utils import start_mission_control, execute_mission


def main():
    while True:
        # Retrieve the agent's selection from the CLI menu
        choice = start_mission_control()

        # Dispatch the mission based on user input
        if choice == 1:
            # Launch the URL collection process
            execute_mission("CRAWLING", run_optimized_crawling, "data/properties_urls.csv")

        elif choice == 2:
            # Launch the data extraction process

            urls = pd.read_csv("data/properties_urls.csv")["property_url"].tolist()
            execute_mission("SCRAPING", run_optimized_scraping, urls, "data/properties_dataset.csv")

        elif choice == 3:
            execute_mission("CLEANING", run_cleaner, "data/properties_dataset.csv", "data/final_properties_dataset.csv")

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
