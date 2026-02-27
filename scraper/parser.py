import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Optional, Dict, Any

import requests
from bs4 import BeautifulSoup

from utils.file_utils import save_to_csv_incremental
from utils.helpers import clean_numeric, safe_get_text


def run_optimized_scraping(urls, dataset_filename, batch_size=100):
    """
        Executes a high-performance scraping mission using concurrent threads and batch processing.

        This function processes URLs in chunks (batches) to manage memory efficiently and
        ensure data is saved incrementally. It provides real-time progress tracking,
        request speed metrics, and estimated time of completion (ETC).

        Args:
            urls (List[str]): The complete list of property URLs to scrape.
            dataset_filename (str): The destination CSV file path.
            batch_size (int): The number of URLs to process before performing a disk write.

        Returns:
            int: The total number of items successfully processed.
        """
    total_urls = len(urls)

    print(f"Mission Started: Scraping {total_urls} target URLs.")
    start_time = time.perf_counter()

    with requests.Session() as session:
        # Create a partial function to pre-configure the session for the thread pool
        fetch_func = partial(get_data_from_url, session=session)

        # Batch processing loop for incremental saving and memory management.
        for i in range(0, total_urls, batch_size):
            print(f"\n{'—' * 20} Processing Batch: {i} {'—' * 20}")

            batch_urls = urls[i: i + batch_size]

            # Multithreading: 20 workers provide a great balance between speed and reliability
            with ThreadPoolExecutor(max_workers=20) as executor:
                batch_results = list(executor.map(fetch_func, batch_urls))

            # Data Validation: Only keep successful extractions (None/Empty filtered out)
            filtered_results = [res for res in batch_results if res]

            # Incremental Backup: Save the batch immediately to prevent data loss
            save_to_csv_incremental(filtered_results, dataset_filename)

            # Progress Metrics Calculation
            elapsed = time.perf_counter() - start_time
            processed = i + len(batch_urls)
            speed = processed / elapsed  # items per second
            remaining = (total_urls - processed) / speed

            # Dashboard Display
            print("_" * 56)
            print(f"Progress: {processed} Finished in {elapsed / 60: .1f} minutes")
            print(f"URLs processed: ({(processed / total_urls) * 100:.1f}%) - Speed: {speed:.2f} items/sec")
            print(f"Estimated time remaining: {remaining / 60:.1f} minutes")
            print("_" * 56)

    return total_urls


def get_data_from_url(url: str, session: requests.Session) -> Optional[Dict[str, Any]]:
    """
    Fetches and parses a single property page to extract structured data.

    This function acts as a safety wrapper for the network request. It handles
    HTTP errors and timeouts gracefully to ensure the multithreaded scraper
    doesn't crash on a single faulty URL.

    Args:
        url (str): The specific property listing URL to scrape.
        session (requests.Session): The persistent session for HTTP requests.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing property details if successful,
                                  otherwise None.
    """
    try:
        # Rotation of User-Agents is recommended to avoid detection, but a
        # stable modern one works for standard volumes.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        # Perform the request with a strict timeout to prevent thread hanging
        response = session.get(url, headers=headers, timeout=10)

        # Handle non-successful status codes (404, 403, 500, etc.)
        if response.status_code != 200:
            return None

        # Parse the HTML content using the fast LXML parser
        soup = BeautifulSoup(response.text, "lxml")

        # Delegate the actual field extraction to the helper function
        property_dict = get_property_data(url, soup)
        return property_dict

    except (requests.exceptions.RequestException, Exception) as e:
        # If there is a timeout, connection problem, or other issue
        print(f"\n[SKIP] Network/Parsing error on {url}: {e}")
        return None  # Filtered out by the parent batch process


def get_property_data(url: str, soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    """
    Orchestrates the extraction of specific features from a property's HTML tree.

    This function filters out invalid listing types (like annuities) and coordinates
    various specialized sub-extractors to populate a comprehensive property data
    dictionary.

    Args:
        url (str): The source URL of the property (used for type identification).
        soup (BeautifulSoup): The parsed HTML content of the listing page.

    Returns:
        Optional[Dict[str, Any]]: A populated property dictionary, or None if the
                                  listing is an annuity.
    """
    # 1. Financial Filter: Skip annuities to keep the dataset clean for regression
    financial_details = soup.find("div", class_="financial w-100")
    if financial_details and "annuity" in financial_details.get_text().lower():
        return None

    property_dict = initialize_property_dict(url)
    set_property_locality(soup, property_dict)
    set_property_type(property_dict, url)
    set_property_price(property_dict, soup)
    set_property_general_infos(soup, property_dict)

    return property_dict


def initialize_property_dict(url):
    """
        Initializes a structured dictionary with a predefined schema for property data.

        This ensures that every listing processed by the scraper has a consistent set
        of keys, facilitating smooth conversion into a Pandas DataFrame and
        subsequent CSV export.

        Args:
            url (str): The direct URL of the property listing.

        Returns:
            Dict[str, Any]: A dictionary containing all required fields initialized to None.
        """
    return {
        "URL": url,
        "Locality": None,
        "Zip code": None,
        "Type of property": None,
        "Subtype of property": None,
        "Price": None,
        "Type of sale": None,
        "Number of rooms": None,
        "Living Area": None,
        "Fully equipped kitchen": None,
        "Furnished": None,
        "Open fire": None,
        "Terrace": None,
        "Terrace area": None,
        "Garden": None,
        "Garden area": None,
        "Surface of the land": None,
        "Number of facades": None,
        "Swimming pool": None,
        "State of the building": None,
    }


def set_property_locality(soup: BeautifulSoup, property_dict: Dict[str, Any]) -> None:
    """
    Extracts geographical data from the listing.
    Uses the 'city-line' class to identify the city and parses the Zip Code.
    """
    property_dict["Locality"] = safe_get_text(soup.find("span", class_="city-line"), "")
    # clean_numeric isolates the 4-digit zip code from the locality string
    property_dict["Zip code"] = clean_numeric(property_dict["Locality"])


def set_property_type(property_dict: Dict[str, Any], url: str) -> None:
    """Determines the property category and subtype by analyzing the URL structure."""
    parts = url.split("/")
    if len(parts) >= 6:
        subtype = parts[5]
        property_dict["Type of property"] = (
            "House"
            if subtype in ["residence", "mixed-building", "master-house", "villa"]
            else "Apartment"
        )
        property_dict["Subtype of property"] = subtype

        # Extracts the transaction type (e.g., 'for-sale') from the URL
        if len(parts) > 6:
            property_dict["Type of sale"] = parts[6].replace("-", " ")


def set_property_price(property_dict: Dict[str, Any], soup: BeautifulSoup) -> None:
    """Extracts the listing price and converts it to a clean integer."""
    price = safe_get_text(soup.find("span", class_="detail__header_price_data"), "")
    property_dict["Price"] = clean_numeric(price)


def set_property_general_infos(soup: BeautifulSoup, property_dict: Dict[str, Any]) -> None:
    """
    Parses the 'general-info' technical table.
    Normalizes categorical data (Yes/No) into binary (1/0) for machine learning readiness.
    """
    # Map for converting categorical text into numerical data for regression models
    binary_map = {
        "Yes": 1,
        "No": 0,
        "0": 0,
        "Fully equipped": 1,
        "Super equipped": 1,
        "Partially equipped": 0,
        None: None,
    }

    info_div = soup.find("div", class_="general-info w-100")
    if info_div:
        headers = info_div.find_all("h4")
        for h in headers:
            key = h.get_text(strip=True)
            value_tag = h.find_next("p")
            if value_tag:
                val = value_tag.get_text(strip=True)

                if key == "State of the property":
                    property_dict["State of the building"] = val
                elif key == "Number of bedrooms":
                    property_dict["Number of rooms"] = clean_numeric(val)
                elif key == "Livable surface":
                    property_dict["Living Area"] = clean_numeric(val)
                elif key == "Kitchen equipment":
                    property_dict["Fully equipped kitchen"] = val
                elif key == "Furnished":
                    property_dict["Furnished"] = binary_map.get(val, 0)
                elif key == "Fireplace":
                    property_dict["Open fire"] = binary_map.get(val, 0)
                elif key == "Terrace":
                    property_dict["Terrace"] = binary_map.get(val, 0)
                elif key == "Terrace Area":
                    property_dict["Terrace area"] = clean_numeric(val)
                elif key == "Garden":
                    property_dict["Garden"] = binary_map.get(val, 0)
                elif key == "Surface garden":
                    property_dict["Garden area"] = clean_numeric(val)
                elif key == "Total land surface":
                    property_dict["Surface of the land"] = clean_numeric(val)
                elif key == "Number of facades":
                    property_dict["Number of facades"] = clean_numeric(val)
                elif key == "Swimming pool":
                    property_dict["Swimming pool"] = binary_map.get(val, 0)
