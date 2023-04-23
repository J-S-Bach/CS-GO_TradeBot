from datetime import datetime

import os

from dotenv import load_dotenv
import requests
import urllib
from nacl.bindings import crypto_sign

from api.marketplace import Marketplace, Item, tradeableItems
from typing import List

public_key = "beba1de26545d9ebfc6c2fb7f5530b3426ea48a4fa55bdd25bb59cd400e29817"
load_dotenv()


def create_dmarket_header(method: str, api_url_path: str, body=""):
    current_time = str(round(datetime.now().timestamp()))
    signature_prefix = "dmar ed25519 "
    headers = {
        "X-Api-Key": public_key,
        "X-Request-Sign":
            signature_prefix +
            crypto_sign(
                (method + api_url_path + current_time + body).encode('utf-8'),
                bytes.fromhex(os.getenv('DMARKET_SECRET_KEY')))[:64].hex(),
        "X-Sign-Date": current_time
    }

    return headers


class DMarketMarketplace(Marketplace):
    marketplace_name = "DMARKET"

    def getLowestPrice(self, name):
        route = f"/price-aggregator/v1/aggregated-prices?Titles={urllib.parse.quote(name)}&Limit=100"
        a = requests.get("https://api.dmarket.com" + route, headers=create_dmarket_header("GET", route)).json()[
            "AggregatedTitles"][0]

        if len(a["AggregatedTitles"] > 0):
            json_item = a["AggregatedTitles"][0]
        else:
            raise Exception("No item found with name " + name)

        return Item(json_item["MarketHashName"], None, json_item["Offers"]["BestPrice"], self.marketplace_name)

    def getItemDetail(self, name) -> Item:
        pass

    def getLowestPriceForItemList(self, names: List[str]) -> List[Item]:
        titles = ""
        for title in names:
            titles += "Titles=" + urllib.parse.quote(title) + "&"
        route = f"/price-aggregator/v1/aggregated-prices?{titles}Limit=100"

        items = []
        for item in requests.get("https://api.dmarket.com" + route, headers=create_dmarket_header("GET", route)).json()[
            "AggregatedTitles"]:
            items.append(Item(item["MarketHashName"], None, item["Offers"]["BestPrice"]))

        return items

    def getItemDetailForItemList(self, name: List[str]):
        pass

    def get_all_offers_lowest_price(self) -> List[Item]:
        titles = ""
        for tradeableItem in tradeableItems:
            titles += "Titles=" + urllib.parse.quote(tradeableItem.name) + "&"
        route = f"/price-aggregator/v1/aggregated-prices?{titles}Limit=100"

        items = []
        for item in requests.get("https://api.dmarket.com" + route, headers=create_dmarket_header("GET", route)).json()[
            "AggregatedTitles"]:
            items.append(Item(item["MarketHashName"], None, float(item["Offers"]["BestPrice"]), self.marketplace_name))

        return items

    def get_balance(self):
        route = "/account/v1/balance"
        balance = requests.get("https://api.dmarket.com" + route, headers=create_dmarket_header("GET", route)).json()
        balanceUSD = round(int(balance['usd']) / 100, 2)
        return balanceUSD
