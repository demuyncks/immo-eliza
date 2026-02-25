import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import pandas as pd

#Get the Html from one website
url = "https://immovlan.be/en/detail/apartment/for-sale/1030/schaarbeek/vbd88427"
headers =  {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
req = requests.get(url, headers=headers, timeout = 10)
content = req.text 
soup = BeautifulSoup(content, "html.parser")

# Make a function to get the data safely. If there is no data, it will return N/A, not crashing
def safe_get_text(soup_element, default="N/A"):
    """For safely take the value, will return NA if there's no value, avoid crashing"""
    if soup_element:
        return soup_element.get_text(strip=True)
    return default

property_dict = {}
#Get price and turn into integer
price_tag = safe_get_text(soup.find('span', class_='detail__header_price_data'))
if price_tag:
    print(price_tag)

numbers_only = re.findall(r'\d+', price_tag) #Have to clean data by eliminating the currency
clean_price = "".join(numbers_only) #Eliminate the . between numbers

if clean_price:
    final_price = int(clean_price)
    print(final_price)
else:
        print("None")

#Get information of address
street_tag = safe_get_text(soup.find('span', class_='street-line'))
city_tag = safe_get_text(soup.find('span', class_='city-line'))

full_address = f"{street_tag}, {city_tag}"

print(street_tag) 
print(city_tag)
print(full_address)

#Find all header with h4, then find value p inside
additional_info = {}
additional_information = soup.find('div', class_ = "general-info w-100") #Do not use find_all here as find_all return a list. Then, we cannot use command find() or find_all() anymore
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
else:
    print ("N/A")
# Take data Type of property and Type of sale
parts = url.split('/')
property_type = parts[5]
type_of_sale = parts[6].replace('-', ' ')

#Put everything in a dictionary
property_dict= {
    "URL": url,
    "Type of property": property_type,
    "Type of sale": type_of_sale,
    "Price" : final_price,
    "Locality" : full_address,
    "Street" : street_tag,
    "City" : city_tag,
    "State of the property:": additional_info.get("State of the property", "N/A"),
    "Number of rooms": additional_info.get("Number of bedrooms", "N/A"),
    "Living Area":additional_info.get("Livable surface", "N/A"),
    "Fully equiped kitchen":additional_info.get("Kitchen equipment", "N/A"),
    "Furnished":additional_info.get("Furnished", "N/A"),
    "Terrace":additional_info.get("Terrace", "N/A"),
    "Garden":additional_info.get("Garden", "N/A"),
    "Surface of the land":additional_info.get("Total land surface", "N/A"),
    "Number of facades":additional_info.get("Number of facades", "N/A"),
    "Swimming pool":additional_info.get("Swimming pool", "N/A"),
    }
print(property_dict)