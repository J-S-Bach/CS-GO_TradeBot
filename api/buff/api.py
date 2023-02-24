import time

import requests as requests
from api.marketplace import Marketplace, Item


class ItemBuff:
    name: str
    id: str

    def __init__(self, name, id):
        self.id = id
        self.name = name


items = [
    ItemBuff("Glove Case", 35086),
    ItemBuff("Operation Breakout Weapon Case", 35883)
]


class BuffMarketplace(Marketplace):
    def getItemDetail(self, name) -> Item:
        for item in items:
            if item.name == name:
                answer = requests.get(
                    f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item.id}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_={int(time.time())}").json()
                buy_price = answer['data']['items'][0]['price']
                return Item(item.name, None, buy_price)
        else:
            raise Exception("No valid ItemName given")
