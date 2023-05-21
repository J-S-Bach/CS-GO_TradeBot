from typing import List

import requests
from api.marketplace import Marketplace, Item, tradeable_items, MARKETPLACE
from datetime import timedelta, datetime


class CSDealsMarketplace(Marketplace):
    recent_answer = None
    last_lowest_price_request = None
    marketplace_name = MARKETPLACE.CSDEALS

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

    def buy_item(self, items: Item, amount=1):
        raise NotImplemented()

    def create_buy_offer(self, item: Item):
        raise NotImplemented()

    def delete_buy_offer(self, buy_offer_id: str):
        raise NotImplemented()

    def get_buy_offers(self):
        raise NotImplemented()

    def get_closed_buy_offers(self):
        raise NotImplemented()

