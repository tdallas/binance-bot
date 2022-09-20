import json

import requests
from bs4 import BeautifulSoup


def scrapp():
    url = 'https://www.binance.com/en/support/announcement/c-48'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.findChild('script', attrs={"id": "__APP_DATA"})
    listings = json.loads(listings.text)
    listings = list(
        map(lambda x: {'id': x['id'], 'title': x['title']}, listings['routeProps']['b723']['catalogs'][0]['articles']))
    listings = list(filter(lambda x: x['title'].find("Trading Pairs") != -1, listings))
    # Make request with this body (listings)


if __name__ == "__main__":
    scrapp()
