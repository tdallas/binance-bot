import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode


def get_timestamp():
    return int(time.time() * 1000)

class BinanceClient:
    TESTNET_URL = "https://testnet.binance.vision/"
    LIVE_URL = "https://api.binance.com/"

    API_KEY = "BA78qWSHvDLYkM3RmGkQYdlvWSvdDsiJTtqzn75pDy4YxD6rulKmJ0l1tMOViG9m"
    API_SECRET = "rZowaFkLorQ5AhIefdmBYOaYNW6Jpfvk6SPxEScv8lbO7AUW9VWdzRpJPGvgZvXT"

    TESTNET_API_KEY = "Wmkm0HyHnrFZARJc1Xj2VaSLIBZXRwOUFgJviAdfPXIzL9Ybkn9o1QFd9mjG6DWv"
    TESTNET_API_SECRET = "HR0b5s9BvD3m5d0UqvysXGClW91LddlZ7moHGwzUTEDow0CHbFyAf6GfIDljlM07"

    RET_EXPECTED = 1.05

    def get_base_url(self, testnet: bool):
        return self.TESTNET_URL if testnet else self.LIVE_URL

    def __init__(self, testnet: bool):
        self.testnet = testnet
        # self.base_url = self.get_base_url(self.testnet)
        self.base_url = self.TESTNET_URL

    def get_header(self):
        return {
            "X-MBX-APIKEY": self.get_api_key()
        }

    def get_api_key(self):
        return self.TESTNET_API_KEY if self.testnet else self.API_KEY

    def get_secret_key(self):
        return self.TESTNET_API_SECRET if self.testnet else self.API_SECRET

    def hashing(self, query_string):
        return hmac.new(self.get_secret_key().encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def dispatch_request(self, http_method):
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'X-MBX-APIKEY': self.get_api_key()
        })
        return {
            'GET': session.get,
            'DELETE': session.delete,
            'PUT': session.put,
            'POST': session.post,
        }.get(http_method, 'GET')

    # used for sending request requires the signature
    def send_signed_request(self, http_method, url_path, payload={}):
        query_string = urlencode(payload)
        # replace single quote to double quote
        query_string = query_string.replace('%27', '%22')
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, get_timestamp())
        else:
            query_string = 'timestamp={}'.format(get_timestamp())

        url = self.base_url + url_path + '?' + query_string + '&signature=' + self.hashing(query_string)
        print("{} {}".format(http_method, url))
        params = {'url': url, 'params': {}}
        response = self.dispatch_request(http_method)(**params)
        return response.json()

    def send_buy_order(self, symbol: str, quantity):
        body = {
            "symbol": symbol.replace("/", ""),
            "side": "BUY",
            "type": "MARKET",
            "quantity": quantity,
        }
        return self.send_signed_request("POST", "api/v3/order", body)

    def get_order_status(self, symbol, orderId):
        body = {
            "symbol": symbol.replace("/", ""),
            "orderId": orderId
        }
        return self.send_signed_request("GET", "api/v3/order", body)

    def send_sell_order(self, symbol, quantity, price):
        body = {
            "symbol": symbol.replace("/", ""),
            "side": "SELL",
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": "GTC"
        }
        return self.send_signed_request("POST", "api/v3/order", body)
