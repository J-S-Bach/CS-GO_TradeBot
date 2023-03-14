from datetime import timedelta, datetime

import requests

cachedExchangeRates = []


def get_exchange_rate(from_currency, to_currency):
    global cachedExchangeRates

    # TODO: write a timestamp that considers the different currency flows

    from_currency_price = requests.get("https://api.skinport.com/v1/sales/history", params={
        "app_id": "252490",
        "currency": from_currency,
        "market_hash_name": "Fire jacket"
    }).json()[0]["sales"][0]["price"]

    to_currency_price = requests.get("https://api.skinport.com/v1/sales/history", params={
        "app_id": "252490",
        "currency": to_currency,
        "market_hash_name": "Fire jacket"
    }).json()[0]["sales"][0]["price"]

    return round(to_currency_price / from_currency_price, 6)


