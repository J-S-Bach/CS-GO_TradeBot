import time
from typing import List

import requests as requests

from api.CurrencyExchange.currencyExchange import get_exchange_rate, CURRENCY
from api.marketplace import Marketplace, Item, tradeableItems, MARKETPLACE, ItemNotAvailable


class BuffMarketplace(Marketplace):
    marketplace_name = MARKETPLACE.BUFF
    fee = 1 - 0.975

    def get_best_offer_for_item(self, name) -> Item:
        for item in tradeableItems:
            if item.name == name:
                answer = requests.get(
                    f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item.id}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_={int(time.time())}").json()
                buy_price = answer['data']['items'][0]['price']
                return Item(item.name, None, buy_price * get_exchange_rate(CURRENCY.CNY, CURRENCY.USD),
                            on_market=self.marketplace_name)
        else:
            raise Exception("No valid ItemName given")

    def get_best_offers(self) -> List[Item]:
        buff_items = []

        for item in tradeableItems:
            answer = requests.get(
                f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item.buffId}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_={int(time.time())}")

            while int(answer.status_code) == 429:
                print("waiting for buff api")
                time.sleep(2)
                answer = requests.get(
                    f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item.buffId}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_={int(time.time())}")
            answer = answer.json()
            buy_price = answer['data']['items'][0]['price']
            buff_items.append(Item(item.name, None, float(buy_price) * get_exchange_rate(CURRENCY.CNY, CURRENCY.USD),
                                   on_market=self.marketplace_name))

        return buff_items

    def get_best_offer_for_item_list(self, names: List[str]) -> List[Item]:
        pass

    def create_cookies(self):
        # TODO: Replace with custom loading cookies since these need to be replaced regularly
        return {
            "Device-Id": "ZXeO6pQgFmJ2w1aryQf7",
            'Locale-Supported': 'en',
            'game': 'csgo',
            'session': '1-hUgTR7Fip4NKzLmvl-GbdCehT4T6_3SQBb5CJs1IPqzZ2032647117',
            'client_id': 'xgl9XGnPqh1x7-gdtmaxGg',
            'display_appids': '"[730\\054 570]"'
        }

    def get_items_from_buff(self, item: Item):
        response = \
            requests.get('https://buff.163.com/api/market/steam_inventory', params={
                'game': 'csgo',
                'page_size': '50',
                'search': item.name,
                'state': 'cansell',
                '_': time.time() * 1000
            }, cookies=self.create_cookies()).json()

        if not (response.get('error') is None):
            raise Exception("Could not get items from Buff with error:", response["error"])

        return response["data"]["items"]

    def sell_item(self, item: Item, amount: int = 1):
        # TODO: Error Handling
        buff_items = self.get_items_from_buff(item)

        if len(buff_items) < amount:
            raise ItemNotAvailable()

        assets = []
        for i in range(amount):
            assets.append(
                {"game": buff_items[i]['game'],
                 "market_hash_name": buff_items[i]['name'],
                 "contextid": buff_items[i]['asset_info']['contextid'],
                 "assetid": buff_items[i]['asset_info']['assetid'],
                 "classid": buff_items[i]['asset_info']['classid'],
                 "instanceid": buff_items[i]['asset_info']['instanceid'],
                 "goods_id": buff_items[i]['goods_id'],
                 "price": item.price,
                 "income": (item.price - item.price * self.fee),
                 "has_market_min_price": False,
                 "cskey_id": ""})

        response = requests.post(
            'https://buff.163.com/api/market/sell_order/create/manual_plus',
            cookies=self.create_cookies(),
            json={"game": "csgo", "assets": assets},
        ).json()

        if not (response.get('error') is None):
            raise Exception("Could not sell items from Buff with error:", response["code"], response["error"])

        print(response)

    def buy_item(self, item: Item, amount=1):
        pass
