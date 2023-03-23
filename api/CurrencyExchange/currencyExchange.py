from datetime import timedelta, datetime
from enum import Enum

import requests

cachedExchangeRates = []


class CURRENCY(Enum):
    EUR = "EUR"
    CNY = "CNY"
    USD = "USD"


def get_exchange_rate(from_currency: CURRENCY, to_currency: CURRENCY) -> float:
    global cachedExchangeRates

    # TODO: write a timestamp that considers the different currency flows

    try:
        from_currency_price = requests.get("https://api.skinport.com/v1/sales/history", params={
            "app_id": "252490",
            "currency": from_currency.name,
            "market_hash_name": "Fire jacket"
        }).json()

        to_currency_price = requests.get("https://api.skinport.com/v1/sales/history", params={
            "app_id": "252490",
            "currency": to_currency.name,
            "market_hash_name": "Fire jacket"
        }).json()

        if from_currency_price["errors"]:
            raise Exception(from_currency_price["errors"][0]["id"] + ": " + from_currency_price["errors"][0]["message"])
        elif to_currency_price["errors"]:
            raise Exception(to_currency_price["errors"][0]["id"] + ": " + to_currency_price["errors"][0]["message"])

        return round(to_currency_price[0]["sales"][0]["price"] / from_currency_price[0]["sales"][0]["price"], 6)

    except Exception as e:
        print(f"Could not calculate currency with error: {str(e)}")
        return 1
