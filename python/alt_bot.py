import asyncio
import json

from binance.client import AsyncClient

api_key = "iXLt76af7sUC3TES8Fa10GqT5rrlUnAwhbR7SUTPG12G0FIC4y5whS4LWdLPh6W0"
api_secret = "xKFHB3dvrld1pLTzKyH34fRO9TLikmAOMmhgkKZSC0kJhVvdOWcXIeD8e7lvxA33"

pair = "GLMBUSD"
pair_buy_price = 0.30

ret_expected = 1.05

FILLED_ORDER_STATUS = "FILLED"

async def send_buy_limit_order(client, symbol, quantity, price):
    await client.order_limit_buy(
    symbol=symbol,
    quantity=quantity,
    price=str(price))

async def send_sell_limit_order(client, symbol, quantity, price):
    await client.order_limit_sell(
    symbol=symbol,
    quantity=quantity,
    price=str(price))

def calculate_qty(token_price, amount_in_usd):
    return amount_in_usd / token_price

#  función con websocket que compre, espere a que se compre y cuando se llene la order que dispare automagicamente la de venta

async def get_order_status(client, symbol, orderId):
    json.loads(await client.get_order(symbol=symbol, orderId=orderId))['status']

async def is_order_filled(client, symbol, orderId):
    return get_order_status(client, symbol, orderId) == FILLED_ORDER_STATUS


async def main():
    client = await AsyncClient.create()

    error = True
    while error:
        order = send_buy_limit_order(client, pair, calculate_qty(pair_buy_price, 100))
        error = order.isError
        order_id = order.id
        buy_price = order.price
    order_filled = False
    while not order_filled:
        order_filled = get_order_status(client, pair, order_id)
    while error:
        order = send_sell_limit_order(client, pair, max, ret_expected * buy_price
    return client

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = loop.run_until_complete(main())
    loop.run_forever()
    loop.run_until_complete(client.close_connection())
