import requests as requests
from api.marketplace import Marketplace, Item
from datetime import timedelta, datetime

csGoAppId = 730


class ItemCSDeals:
    name: str
    id: str

    def __init__(self, name, id):
        self.id = id
        self.name = name


class CSDealsMarketplace(Marketplace):
    lowestPrices = None
    last_lowest_price_request = None

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
                return Item(item["marketname"], None, item["lowest_price"])
        else:
            raise Exception("No item found with name " + name)

    def getItemDetail(self, name) -> Item:
        pass
