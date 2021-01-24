# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import requests as rq
import csv
import json


logging.basicConfig()

STATE = {"value": 0}
    
USERS = set()
data_market_lis_users = set()

def get_mock_data_market():
  while True:
    with open('Evolucion_index_20201217.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
          try:
            eachRow = {'IndiceBTCMtR': row[0], 'LiquidezMedida': row[1], 'CostofTrade': row[2], 'time': row[3]}
            yield eachRow
          except StopIteration:
            pass


mock_data_generator = get_mock_data_market()


def get_btc_usd_price_bitfinex():
    return rq.get("https://api.bitfinex.com/v1/pubticker/btcusd").json()


def get_btc_usd_price():
    return json.dumps({"type":"btcusd","md":get_btc_usd_price_bitfinex()})

def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_price():
    if USERS:  
        message = json.dumps(next(mock_data_generator))
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_state()
            elif data["action"] == "suscribe":
                data_market_lis_users.add(websocket)
                if len (USERS) == 1:
                  while True:
                    await notify_price()
                    await asyncio.sleep(10)
            else:
                await unregister(websocket)
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(counter, "0.0.0.0", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

