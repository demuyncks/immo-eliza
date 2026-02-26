import re
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import requests
from bs4 import BeautifulSoup

from utils.file_utils import save_to_csv


def run_optimized_scraping(urls, final_filename, batch_size=100):
    total_urls = len(urls)

    # First estimation
    print(f"Start scraping {total_urls} URLs.")
    start_time = time.perf_counter()

    with requests.Session() as session:
        fetch_func = partial(get_data_from_url, session=session)
        # We divide the list into batches to save regularly.
        for i in range(0, total_urls, batch_size):
            print(
                f"______________________________Batch: {i}______________________________"
            )

            batch_urls = urls[i : i + batch_size]

            with ThreadPoolExecutor(max_workers=20) as executor:
                batch_results = list(executor.map(fetch_func, batch_urls))
            # FILTER: Only valid dictionaries are kept (not None and not empty)
            filtered_results = [res for res in batch_results if res]
            # Immediate backup of the batch_results
            save_to_csv(filtered_results, final_filename)
            # Progress calculation and estimation
            elapsed = time.perf_counter() - start_time
            processed = i + len(batch_urls)
            speed = processed / elapsed  # items per second
            remaining = (total_urls - processed) / speed

            print(
                "_______________________________________________________________________"
            )
            print(
                f"{processed} Finished in {(time.perf_counter() - start_time) / 60: .1f} minutes"
            )
            print(f"[{processed}/{total_urls}] - {speed:.2f} req/s")
            print(f"Estimated time remaining: {remaining / 60:.1f} minutes")
            print(
                "_______________________________________________________________________"
            )


def get_data_from_url(url, session):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = session.get(url, headers=headers, timeout=10)
        #  If an error occurs (e.g., 404, 403, 500)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "lxml")

        property_dict = get_property_data(url, soup)
        return property_dict
    except (requests.exceptions.RequestException, Exception) as e:
        # If there is a timeout, connection problem, or other issue, we just display a message.
        print(f"\n[SKIP] Error on  {url} : {e}")
        return None  # Will be filtered by [res for res in batch_results if res]


def get_property_data(url, soup):
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
    return {
        "URL": url,
        "Locality": None,
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


def set_property_locality(soup, property_dict):
    property_dict["Locality"] = safe_get_text(soup.find("span", class_="city-line"), "")
    property_dict["Zip code"] = clean_numeric(property_dict["Locality"])


def set_property_type(property_dict, url):
    parts = url.split("/")
    if len(parts) >= 6:
        property_dict["Type of property"] = (
            "House"
            if parts[5] in ["Residence", "Mixed building", "Master house", "Villa"]
            else "Apartment"
        )
        property_dict["Subtype of property"] = parts[5]
        property_dict["Type of sale"] = parts[6].replace("-", " ") if (parts[6]) else ""


def set_property_price(property_dict, soup):
    price = safe_get_text(soup.find("span", class_="detail__header_price_data"), "")
    property_dict["Price"] = clean_numeric(price)


def set_property_general_infos(soup, property_dict):
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


def safe_get_text(soup_element, default=None):
    """For safely take the value, will return NA if there's no value, avoid crashing"""
    if soup_element:
        return soup_element.get_text(strip=True)
    return default


def clean_numeric(text):
    if not text:
        return None
    numbers = "".join(re.findall(r"\d+", text))
    return int(numbers) if numbers else None
