from typing import List

import requests
from api.marketplace import Marketplace, Item, tradeableItems
from datetime import timedelta, datetime

csGoAppId = 730


class CSDealsMarketplace(Marketplace):
    lowestPrices = None
    last_lowest_price_request = None
    marketplace_name = "CSDEALS"

    def getLowestPrice(self, name):
        if not self.lowestPrices \
                or self.last_lowest_price_request < datetime.utcnow() + timedelta(minutes=-5):

            try:
                t = requests.get("https://cs.deals/API/IPricing/GetLowestPrices/v1", headers={
                    "content-type": "application/json"
                }, json={"appid": csGoAppId}).json()

                self.lowestPrices = t
                self.last_lowest_price_request = datetime.utcfromtimestamp(int(t["response"]["time_updated"]))
            except Exception as e:
                raise Exception("getLowestPrice request failed with error " + str(e))

        for item in self.lowestPrices["response"]["items"]:
            if item["marketname"] == name:
                return Item(item["marketname"], None, item["lowest_price"], self.marketplace_name)
        else:
            raise Exception("No item found with name " + name)

    def getItemDetail(self, name) -> Item:
        pass

    def getLowestPriceForItemList(self, names: List[str]) -> List[Item]:
        pass

    def get_all_offers_lowest_price(self):
        payload = {"appid": "730"}
        headers = {
            "content-type": "application/json"
        }
        answer = requests.get("https://cs.deals/API/IPricing/GetLowestPrices/v1", headers=headers, json=payload).json()

        cs_deal_items = []

        for offeredItem in answer["response"]["items"]:
            for tradeableItem in tradeableItems:
                if tradeableItem.name == offeredItem["marketname"]:
                    cs_deal_items.append(
                        Item(offeredItem["marketname"], None, float(offeredItem["lowest_price"]), self.marketplace_name))

        return cs_deal_items

    def getItemDetailForItemList(self, name: List[str]):
        pass
