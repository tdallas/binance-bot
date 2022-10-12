import json

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

regex_for_pairs = "([A-Z]+/[A-Z]+){1}"


def scrapp():
    pairs = []
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
        date = str(datetime.fromisoformat(text.split("at ")[-1].split(" (")[0]))
        # print(pairs)
        # print(date)
        pairs_models = []
        for pair in pairs:
            pairs_models.append({'pair': pair, 'date': date})
        print({'content': pairs_models})
        r = requests.post("http://localhost:8000/pairs", data=json.dumps({'content': pairs_models}))
        print(r.json())


if __name__ == "__main__":
    scrapp()
