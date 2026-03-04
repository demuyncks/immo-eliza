from concurrent.futures import ThreadPoolExecutor
from typing import List

from bs4 import BeautifulSoup
from requests import Session

from utils.file_utils import to_csv_file


def run_optimized_crawling(filename: str) -> int:
    """
    Orchestrates the discovery of property URLs using multi-threading.

    This function fetches base search URLs, generates the full list of
    paginated URLs, and utilizes a ThreadPoolExecutor to concurrently
    extract individual property links. The final list is de-duplicated
    and saved to a CSV file.

    Args:
        filename (str): The destination path for the output CSV file.

    Returns:
        int: The total count of unique property URLs successfully collected.
    """

    # 1. Generate the queue of all search result pages
    pages_urls = generate_pages_urls(get_base_urls())

    results = []
    # 2. Use a Session object for connection pooling and 10 workers for speed
    with Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = [executor.submit(fetch_properties_urls, url, session) for url in pages_urls]
            for future in future_to_url:
                results.extend(future.result())

    # 3. Ensure data quality by removing duplicates
    unique_results = list(set(results))

    # 4. Persistence layer: save to CSV
    to_csv_file(filename, ["property_url"], unique_results)

    return len(unique_results)


def generate_pages_urls(base_urls: List[str]) -> List[str]:
    """
    Constructs a complete list of paginated search URLs for all provided regions.

    This function iterates through base location URLs, determines the total
    number of result pages available for each, and generates the specific
    URLs required for the multithreaded scraper.

    Args:
        base_urls (List[str]): A list of starting URLs for different locations
                               or categories.

    Returns:
        List[str]: A full queue of paginated URLs ready for processing.
    """
    properties_urls = []

    with Session() as session:
        for url in base_urls:
            # Determine the maximum number of pages for this specific search
            max_p = fetch_page_limit(url, session)

            # Generate the specific URL for every page found
            for i in range(1, max_p):
                properties_urls.append(f"{url}&page={i}")

    return properties_urls


def fetch_page_limit(base_url: str, session: Session) -> int:
    """
    Identifies the total number of result pages for a given search URL.

    This function parses the pagination component of the target website to find
    the highest page number. It includes a safety buffer to ensure maximum
    coverage of available listings.

    Args:
        base_url (str): The search results page to analyze.
        session (Session): An active requests session for network efficiency.

    Returns:
        int: The last page number found, plus a safety margin of 10.
    """
    last_page_number = 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        response = session.get(base_url, headers=headers, timeout=10)
        # We use lxml for faster parsing speed in large-scale scraping
        soup = BeautifulSoup(response.text, "lxml")

        # Select all pagination links that contain a page value
        last_page_tag = soup.select("ul.pagination a.page-link[data-value-page]")

        if last_page_tag:
            # Extract the page number from the last element in the list
            last_page_number = last_page_tag[-1].get("data-value-page")

        # We return an integer with a small buffer to account for new listings
        return int(last_page_number) + 10

    except Exception as e:
        print(f"Warning: Could not determine page limit for {base_url}. Error: {e}")
        return last_page_number


def fetch_properties_urls(page_url: str, session: Session) -> List[str]:
    """
    Extracts individual property listing URLs from a single search results page.

    This function parses the HTML of a result page, identifies property links
    while filtering out multi-unit projects (projectdetail), and returns
    a list of direct property URLs.

    Args:
        page_url (str): The URL of the specific search results page to scrape.
        session (Session): The active HTTP session used for the request.

    Returns:
        List[str]: A list of validated property URLs found on the page.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/119.0.0.0 Safari/537.36"
    }

    properties_urls = []
    try:
        response = session.get(page_url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")

            # Target listing titles which contain the direct links
            for a in soup.select("h2 a[href]"):
                href = a.get("href")
                if "/projectdetail/" not in href:  # Ignore the "project properties"
                    properties_urls.append(href)

            print(f"[+] Page Processed: {len(properties_urls)} properties added\n")

    except Exception as e:
        print(f"Error processing {page_url}: {e}")

    return properties_urls


def get_base_urls() -> List[str]:
    """
    Defines the initial search parameters and generates base URLs for scraping.

    This function targets all Belgian provinces and specific Brussels municipalities.
    It applies filters for transaction types (sale) and property types (houses
    and apartments) to ensure the collected data is relevant for real estate analysis.

    Returns:
        List[str]: A list of comprehensive search URLs to be used as starting points.
    """

    # Coverage of all 10 Belgian provinces
    provinces = ["namur", "liege", "hainaut", "luxembourg", "brabant-wallon", "east-flanders", "west-flanders",
                 "antwerp", "limburg", "vlaams-brabant"]

    # Detailed coverage of the Brussels-Capital Region
    bx_municipalities = ["1000-brussels", "1020-laken", "1030-schaarbeek", "1040-etterbeek", "1050-elsene",
                         "1060-sint-gillis", "1070-anderlecht", "1080-sint-jans-molenbeek", "1090-jette",
                         "1120-neder-over-heembeek", "1130-haren", "1140-evere", "1150-sint-pieters-woluwe",
                         "1160-oudergem", "1170-watermaal-bosvoorde", "1180-ukkel", "1190-vorst",
                         "1200-sint-lambrechts-woluwe", "1210-sint-joost-ten-node"]

    # Global search parameters to filter relevant listings
    params = (
        "&transactiontypes=for-sale,in-public-sale,"
        "&propertytypes=house,apartment"
        "&propertysubtypes=residence,villa,mixed-building,master-house,cottage,"
        "bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex"
        "&noindex=1"
    )

    # Building URLs for provinces
    base_urls = [f"https://immovlan.be/en/real-estate?provinces={p}{params}" for p in provinces]

    # Building URLs for Brussels municipalities
    base_urls += [f"https://immovlan.be/en/real-estate?towns={m}{params}" for m in bx_municipalities]

    return base_urls
