import time
from datetime import timedelta, datetime
from enum import Enum
from typing import Callable

import requests
from requests import Response

from helper.request_with_retry import request_with_retry

cached_exchange_rates = {}


class CURRENCY(Enum):
    EUR = "EUR"
    CNY = "CNY"
    USD = "USD"


def get_exchange_rate(from_currency: CURRENCY, to_currency: CURRENCY) -> float:
    global cached_exchange_rates

    if cached_exchange_rates.get(from_currency.name) is None:
        cached_exchange_rates[from_currency.name] = {
            to_currency.name: {
                "exchange_rate": calculate_exchange_rate_from_api(from_currency, to_currency),
                "timestamp": datetime.utcnow()
            }
        }
    elif cached_exchange_rates[from_currency.name].get(to_currency.name) is None:
        cached_exchange_rates[from_currency.name][to_currency.name] = {
            "exchange_rate": calculate_exchange_rate_from_api(from_currency, to_currency),
            "timestamp": datetime.utcnow()
        }
    elif cached_exchange_rates[from_currency.name][to_currency.name]["timestamp"] < datetime.utcnow() + timedelta(
            minutes=-5):
        cached_exchange_rates[from_currency.name][to_currency.name] = {
            "exchange_rate": calculate_exchange_rate_from_api(from_currency, to_currency),
            "timestamp": datetime.utcnow()
        }

    return cached_exchange_rates[from_currency.name][to_currency.name]["exchange_rate"]


def calculate_exchange_rate_from_api(from_currency: CURRENCY, to_currency: CURRENCY) -> float:
    print("Calling Skinport API to calculate exchange rate of", from_currency.name, "to", to_currency.name)
    try:
        raw_from_currency_prices = request_with_retry(
            lambda response: (
                    response.status_code != 200 and response.json()["errors"][0]["id"] == "rate_limit_exceeded"),
            5,
            lambda: requests.get(
                "https://api.skinport.com/v1/sales/history", params={
                    "app_id": "252490",
                    "currency": from_currency.name,
                }),
            10)

        raw_to_currency_prices = request_with_retry(
            lambda response: (
                    response.status_code != 200 and response.json()["errors"][0]["id"] == "rate_limit_exceeded"),
            300,
            lambda: requests.get(
                "https://api.skinport.com/v1/sales/history", params={
                    "app_id": "252490",
                    "currency": to_currency.name,
                }),
            1)

        to_currency_prices = raw_to_currency_prices.json()
        from_currency_prices = raw_from_currency_prices.json()

        if raw_from_currency_prices.status_code != 200:
            raise Exception(
                from_currency_prices["errors"][0]["id"] + ": " + from_currency_prices["errors"][0]["message"])
        elif raw_to_currency_prices.status_code != 200:
            raise Exception(to_currency_prices["errors"][0]["id"] + ": " + to_currency_prices["errors"][0]["message"])

        for to_currency_price in to_currency_prices:
            for from_currency_price in from_currency_prices:
                if to_currency_price["market_hash_name"] == from_currency_price["market_hash_name"] \
                        and from_currency_price["last_24_hours"]["max"] is not None \
                        and to_currency_price["last_24_hours"]["max"] is not None:
                    return round(
                        to_currency_price["last_24_hours"]["max"] / from_currency_price["last_24_hours"]["max"],
                        6)
        else:
            raise Exception("No fitting item to calculate found")

    except Exception as e:
        print(f"Could not calculate currency with error: {str(e)}")
        raise e
