
def get_general_urls():
# List of provinces and municipalities URLs (returned in general_urls)

## Base Url (with filters) and lists of locations
    provinces=["namur","liege","hainaut","luxembourg","brabant-wallon","east-flanders","west-flanders","antwerp","limburg","vlaams-brabant"]
    bx_municipalities=["1000-brussels","1020-laken","1030-schaarbeek","1040-etterbeek","1050-elsene","1060-sint-gillis","1070-anderlecht","1080-sint-jans-molenbeek","1090-jette","1120-neder-over-heembeek","1130-haren","1140-evere","1150-sint-pieters-woluwe","1160-oudergem","1170-watermaal-bosvoorde","1180-ukkel","1190-vorst","1200-sint-lambrechts-woluwe","1210-sint-joost-ten-node"]

## Store urls into list
    general_urls=[]
    for province in provinces:
        url_province=f"https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&provinces={province}&noindex=1"
        general_urls.append(url_province)

    for municipality in bx_municipalities:
        url_municipality=f"https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&towns={municipality}&noindex=1"
        general_urls.append(url_municipality)

    return general_urls

def get_property_urls(general_urls):
# List of all properties URLs by scraping all webpages related to every location (returned in property_urls)

    from requests import Session
    from bs4 import BeautifulSoup

## Open a Session for speed
    session=Session()
    headers={"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"}

## Get all pages for every location >> stored in list page_urls
    page_urls=[]
    for general_url in general_urls:
        for i in range(1,51):
            page_urls.append(general_url+f"&page={i}")

## Scrape every property URL from every page
    property_urls=[]
    for page_url in page_urls:
        r=session.get(page_url,headers=headers)
        html=r.text
        soup=BeautifulSoup(html,"html.parser")
        for h2 in soup.find_all("h2"):
            for a in h2.find_all("a",href=True):
                property_urls.append(a["href"])

    print(f"Number of URLs : {len(property_urls)}")

    return property_urls
