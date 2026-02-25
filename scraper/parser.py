import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import pandas as pd

#Get the Html from one website
def get_data(url, session):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        print (url)
        property_dict= {
        "URL": url,
        "Type of property": get_type(url, soup)["property_type"],
        "Type of sale": get_type(url, soup)["type_of_sale"],
        "Price" : get_price (soup),
        "Locality" : get_address(soup)['full_address'],
        "Street" : get_address(soup)['street'],
        "City" : get_address(soup)['city'],
        "State of the property:": get_additional_info(soup).get("State of the property", "N/A"),
        "Number of rooms": get_additional_info(soup).get("Number of bedrooms", "N/A"),
        "Living Area":get_additional_info(soup).get("Livable surface", "N/A"),
        "Fully equiped kitchen":get_additional_info(soup).get("Kitchen equipment", "N/A"),
        "Furnished":get_additional_info(soup).get("Furnished", "N/A"),
        "Terrace":get_additional_info(soup).get("Terrace", "N/A"),
        "Garden":get_additional_info(soup).get("Garden", "N/A"),
        "Surface of the land":get_additional_info(soup).get("Total land surface", "N/A"),
        "Number of facades":get_additional_info(soup).get("Number of facades", "N/A"),
        "Swimming pool":get_additional_info(soup).get("Swimming pool", "N/A"),
        }
        print(property_dict)
    except Exception as e:
        return f"Erreur : {e}"

# Make a function to get the data safely. If there is no data, it will return N/A, not crashing
def safe_get_text(soup_element, default="N/A"):
    """For safely take the value, will return NA if there's no value, avoid crashing"""
    if soup_element:
        return soup_element.get_text(strip=True)
    return default

    #Get price and turn into integer

property_dict= {}
def get_price(soup):
    price_tag = safe_get_text(soup.find('span', class_='detail__header_price_data'))
    if price_tag and price_tag != "N/A":
        numbers_only = re.findall(r'\d+', price_tag) #Have to clean data by eliminating the currency
        clean_price = "".join(numbers_only) #Eliminate the . between numbers
        return int(clean_price)
    else:
         return "N/A"
    
    #Get information of address
def get_address(soup):
    street_tag = safe_get_text(soup.find('span', class_='street-line'))
    city_tag = safe_get_text(soup.find('span', class_='city-line'))
    full_address = f"{street_tag}, {city_tag}"
    return {
        "street": street_tag,
        "city": city_tag,
        "full_address": full_address
    }
def get_additional_info(soup):
    additional_info = {}
    #Find all header with h4, then find value p inside
    additional_information = soup.find('div', class_ = "general-info w-100")
    if additional_information:
    # Find all the header in soup
        all_headers = additional_information.find_all('h4')
    
        for header in all_headers:
            # Take only the text in header
            key = header.get_text(strip=True)
            
            # Find the nearest <p> in header h4
            value_tag = header.find_next('p')
            
            if value_tag:
                value = value_tag.get_text(strip=True)
                additional_info[key] = value  
    return additional_info
    
    # Take data Type of property and Type of sale
def get_type(url,soup):
    parts = url.split('/')
    property_type = parts[5]
    type_of_sale = parts[6].replace('-', ' ')
    return {
        "property_type": property_type,
        "type_of_sale": type_of_sale
    }
