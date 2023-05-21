import base64
import hashlib
import hmac
import struct
import time
from typing import List

import requests
from api.marketplace import Marketplace, Item, tradeable_items, MARKETPLACE
from datetime import timedelta, datetime

from helper.request_with_retry import request_with_retry


class CSDealsMarketplace(Marketplace):
    recent_answer = None
    last_lowest_price_request = None
    marketplace_name = MARKETPLACE.CSDEALS

    def __authenticate_at_google(self):
        # I have 0 idea how this function is doing what its doing
        cs_deals_secret = 'NNMDC5ZXIJMVQNDX'

        key = base64.b32decode(cs_deals_secret + '===='[:3 - ((len(cs_deals_secret) - 1) % 4)], True)
        msg = struct.pack(">Q", (int(time.time() + 3) // 30))
        token = hmac.new(key, msg, hashlib.sha1).digest()
        o = token[19] & 15
        token = (struct.unpack(">I", token[o:o + 4])[0] & 0x7fffffff) % 1000000

        if len(str(token)) < 6:
            for x in range(6 - len(str(token))):
                token = str(0) + str(token)

        return token

    def __get_all_offers(self):
        if not self.recent_answer \
                or self.last_lowest_price_request < datetime.utcnow() + timedelta(minutes=-5):

            try:
                answer = requests.get("https://cs.deals/API/IPricing/GetLowestPrices/v1", headers={
                    "content-type": "application/json"
                }, json={"appid": "730"}).json()

                self.recent_answer = answer
                self.last_lowest_price_request = datetime.utcfromtimestamp(int(answer["response"]["time_updated"]))
            except Exception as e:
                raise Exception("getLowestPrice request failed with error " + str(e))

        return self.recent_answer

    def get_best_offer_for_item(self, name):
        for item in self.__get_all_offers()["response"]["items"]:
            if item["marketname"] == name:
                return Item(item["marketname"], None, item["lowest_price"], self.marketplace_name)
        else:
            raise Exception("No item found with name " + name)

    def get_best_offers(self):
        cs_deal_items = []

        for offeredItem in self.__get_all_offers()["response"]["items"]:
            for tradable_item in tradeable_items:
                if tradable_item.name == offeredItem["marketname"]:
                    cs_deal_items.append(
                        Item(offeredItem["marketname"], None, float(offeredItem["lowest_price"]),
                             self.marketplace_name))

        return cs_deal_items

    def get_best_offer_for_item_list(self, names: List[str]) -> List[Item]:
        return_offers: List[Item] = []

        for offer in self.__get_all_offers()["response"]["items"]:
            for name in names:
                if offer["marketname"] == name:
                    return_offers.append(Item(offer["marketname"], None, offer["lowest_price"], self.marketplace_name))

        return return_offers

    def sell_item(self, item: Item, amount=1):
        raise NotImplemented()
        payload = {"2fa": str(self.__authenticate_at_google()),
                   "steam": item.name,  # TODO: previous: items, idk if item.name is correct, other than that: can qw put the same item twice in it, so we can specify the amount.. probably
                   "include_trade_item_id": 0}  # toDo idk if correct
        headers = {
            "content-type": "application/json",
            "Authorization": "Basic RmliM1JRY1RlVFBIWUhVUXlKakFaU3dJOg=="
        }

        request_with_retry(
            lambda request:
            not request['success']
            or request.status_code != 200
            or request.json()['error'] == 'Invalid 2FA code'
            or request.json()['error'] == 'Unable to make the trade',
            60,
            lambda: requests.post("https://cs.deals/API/ISales/ListItems/v1", headers=headers, json=payload),
            2
        )

    def buy_item(self, item: Item, amount=1):
        raise NotImplemented()
        headers = {
            "content-type": "application/json",
            "Authorization": "Basic RmliM1JRY1RlVFBIWUhVUXlKakFaU3dJOg=="
        }
        token = self.__authenticate_at_google()



        for i in range(amount):
            # TODO: What was in idlist?, item.assset_id correct?
            payload = {"2fa": str(token), "ids": str(item.asset_id), "total": str(item.price)}

            request_with_retry(
                lambda request: not request.json()["success"] or request.status_code != 200,
                30,
                lambda: requests.post("https://cs.deals/API/ITrades/MarketplacePurchase/v1", headers=headers,
                                      json=payload),
                2
            )

    def create_buy_offer(self, item: Item):
        raise NotImplemented()

    def delete_buy_offer(self, buy_offer_id: str):
        raise NotImplemented()

    def get_buy_offers(self):
        raise NotImplemented()

    def get_closed_buy_offers(self):
        raise NotImplemented()
