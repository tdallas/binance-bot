import asyncio
import json

from binance.client import AsyncClient

# from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient

api_key = "iXLt76af7sUC3TES8Fa10GqT5rrlUnAwhbR7SUTPG12G0FIC4y5whS4LWdLPh6W0"
api_secret = "xKFHB3dvrld1pLTzKyH34fRO9TLikmAOMmhgkKZSC0kJhVvdOWcXIeD8e7lvxA33"

SYMBOL = "BTCBUSD"
BINANCE_PUBLIC_URL = "https://api1.binance.com/api/v3/ticker/price?symbol=" + SYMBOL

RET_EXPECTED = 0.005
QTY_TO_BUY = 0  # Amount of sell / current_btc_price
QTY_TO_SELL = 0

pair = ""
pair_buy_price = 1

async def send_buy_limit_order(client: AsyncClient, symbol, quantity, price):
    await client.order_limit_buy(
        symbol=symbol,
        quantity=quantity,
        price=str(price))


async def send_sell_limit_order(client, symbol, quantity, price):
    await client.order_limit_sell(
        symbol=symbol,
        quantity=quantity,
        price=str(price))

amount_of_data = 120 * 40

MIN_AMOUNT_OF_BTC = 0.001
FILLED_ORDER_STATUS = "FILLED"

# prices = []
# async def listen_price():
#     i = 0
#     async with httpx.AsyncClient() as client:
#         while i < amount_of_data:
#                 r = await client.get(BINANCE_PUBLIC_URL)
#                 json_response = json.loads(r.text)
#                 print("Response: ", json_response['price'])
#                 prices.append(json_response['price'])
#                 i += 1
#                 time.sleep(15)
#     pd.DataFrame(prices).to_csv(
#         "prices.csv", sep='\t', index=None, header=None)
#     return

async def get_order_status(client, symbol, orderId):
    json.loads(await client.get_order(symbol=symbol, orderId=orderId))['status']

async def is_order_filled(client, symbol, orderId):
    return get_order_status(client, symbol, orderId) == FILLED_ORDER_STATUS

def calculate_qty(token_price, amount_in_usd):
    return amount_in_usd / token_price


async def main():
    client = await AsyncClient.create(testnet=True)

    # buy
    error = True
    while error:
        order = send_buy_limit_order(client, pair, calculate_qty(pair_buy_price, 100))
        error = order.isError
        order_id = order.id
        buy_price = order.price
        buy_qty = order.qty

    # wait for buy order to fill
    order_filled = False
    while not order_filled:
        order_filled = get_order_status(client, pair, order_id)

    # sell
    while error:
        order = send_sell_limit_order(client, pair, buy_qty, RET_EXPECTED * buy_price)
    return client

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = loop.run_until_complete(main())
    # loop.run_forever()
    loop.run_until_complete(client.close_connection())
    print("TRADE DONE")
