from scraper.parser import get_data
import requests
URLS = ["https://immovlan.be/fr/detail/appartement/a-vendre/1030/schaerbeek/vbd88427",
        "https://immovlan.be/fr/detail/immeuble-mixte/a-vendre/1030/schaerbeek/vbd31200",
        "https://immovlan.be/fr/projectdetail/2573463-7554937",
        "https://immovlan.be/fr/detail/surface-industrielle/a-vendre/1030/schaerbeek/vbd89703",
        "https://immovlan.be/fr/detail/immeuble-mixte/a-vendre/1030/schaerbeek/vbd89569"]
with requests.Session() as session:
    for url in URLS:
        print(get_data(url,session=session))