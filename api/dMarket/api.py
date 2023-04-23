import json
from datetime import datetime, time
import time

import os

from dotenv import load_dotenv
import requests
import urllib
from nacl.bindings import crypto_sign

from api.marketplace import Marketplace, Item, tradeableItems, MARKETPLACE, ItemNotAvailable, ItemsNotBought
from typing import List

public_key = "beba1de26545d9ebfc6c2fb7f5530b3426ea48a4fa55bdd25bb59cd400e29817"
load_dotenv()


class BuffOffer():
    price: int
    offer_id: str

    def __init__(self, price, offer_id):
        self.price = price
        self.offer_id = offer_id

    def __lt__(self, other):
        return self.price < other.price


def create_dmarket_header(method: str, api_url_path: str, body=""):
    current_time = str(round(datetime.now().timestamp()))
    signature_prefix = "dmar ed25519 "
    headers = {
        "X-Api-Key": public_key,
        "X-Request-Sign":
            signature_prefix +
            crypto_sign(
                (method + api_url_path + body + current_time).encode('utf-8'),
                bytes.fromhex(os.getenv('DMARKET_SECRET_KEY')))[:64].hex(),
        "X-Sign-Date": current_time
    }

    return headers


class DMarketMarketplace(Marketplace):
    marketplace_name = MARKETPLACE.DMARKET
    _base_url = "https://api.dmarket.com"

    def get_best_offer_for_item(self, name):
        route = f"/price-aggregator/v1/aggregated-prices?Titles={urllib.parse.quote(name)}&Limit=100"
        a = requests.get(self._base_url + route, headers=create_dmarket_header("GET", route)).json()[
            "AggregatedTitles"][0]

        if len(a["AggregatedTitles"] > 0):
            json_item = a["AggregatedTitles"][0]
        else:
            raise Exception("No item found with name " + name)

        return Item(json_item["MarketHashName"], None, json_item["Offers"]["BestPrice"], self.marketplace_name)

    def get_best_offer_for_item_list(self, names: List[str]) -> List[Item]:
        titles = ""
        for title in names:
            titles += "Titles=" + urllib.parse.quote(title) + "&"
        route = f"/price-aggregator/v1/aggregated-prices?{titles}Limit=100"

        items = []
        for item in requests.get(self._base_url + route, headers=create_dmarket_header("GET", route)).json()[
            "AggregatedTitles"]:
            items.append(Item(item["MarketHashName"], None, item["Offers"]["BestPrice"]))

        return items

    def get_best_offers(self) -> List[Item]:
        titles = ""
        for tradeableItem in tradeableItems:
            titles += "Titles=" + urllib.parse.quote(tradeableItem.name) + "&"
        route = f"/price-aggregator/v1/aggregated-prices?{titles}Limit=100"

        items = []
        for item in \
                requests.get(self._base_url + route, headers=create_dmarket_header("GET", route)).json()[
                    "AggregatedTitles"]:
            items.append(Item(item["MarketHashName"], None, float(item["Offers"]["BestPrice"]), self.marketplace_name))

        return items

    def sell_item(self, item: Item, amount=1):
        pass

    def buy_item(self, item: Item, amount=1):
        """
        Buys wanted item with specific amount. Can raise custom errors. \n
        - ItemNotAvailable: item is not available at wanted amount \n
        - ItemsNotBought: not all items could be bought due to errors
        """
        # TODO: TEST THIS FUNCTION!
        offer_route = "/exchange/v1/offers-by-title?Title= " + item.name + F"&Limit=100000"
        buy_route = "/exchange/v1/offers-buy"
        response = requests.get(self._base_url + offer_route,
                                headers=create_dmarket_header("GET", offer_route)).json()
        items_to_buy: List[BuffOffer] = []
        price = int(item.price * 100)

        for response_item in response['objects']:
            if response_item['title'] == item.name:
                if price >= int(response_item['price']['USD']):
                    items_to_buy.append(
                        BuffOffer(int(response_item['price']['USD']), response_item['extra']['offerId']))

        # Sort ascending by price
        items_to_buy.sort()

        if len(items_to_buy) <= amount:
            raise ItemNotAvailable()

        items_not_bought_counter = 0
        for i in range(amount):
            body = {
                "offers": [
                    {
                        "offerId": items_to_buy[i].offer_id,
                        "price": {
                            "amount": str(items_to_buy[i].price),
                            "currency": "USD"
                        },
                        "type": "dmarket"
                    }
                ]
            }

            response = requests.patch(self._base_url + buy_route,
                                      headers=create_dmarket_header("PATCH", buy_route, json.dumps(body)),
                                      json=body).json()

            if not (response.get('message') is None):
                raise Exception(response["code"] + response["message"])

            if response['status'] != 'TxSuccess':
                items_not_bought_counter += 1

            # TODO: Write into DB once its there
            if i != amount:
                time.sleep(0.4)

        if items_not_bought_counter < 0:
            raise ItemsNotBought(items_not_bought_counter)
