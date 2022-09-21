import json

import requests
from bs4 import BeautifulSoup
import re

regex_for_pairs = "([A-Z]+/[A-Z]+){1}"

def scrapp():
    url = 'https://www.binance.com/en/support/announcement/c-48'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.findChild('script', attrs={"id": "__APP_DATA"})
    listings = json.loads(listings.text)
    # print(listings)
    listings = list(
        map(lambda x: {'id': x['id'], 'title': x['title'], 'code': x['code']},
            listings['routeProps']['b723']['catalogs'][0]['articles']))
    listings = list(filter(lambda x: x['title'].find("Trading Pairs") != -1, listings))
    codes = list(map(lambda x: x['code'], listings))
    # Make request with this body (listings)
    for code in codes:
        announcement_url = 'https://www.binance.com/en/support/announcement/' + code
        response = requests.get(announcement_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.text[soup.text.find("Binance will open trading for"):].split(".")[0]
        pairs = re.findall(regex_for_pairs, text)
        print(pairs)
        print(text.split("at ")[-1])



if __name__ == "__main__":
    scrapp()
