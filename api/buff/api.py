import time
from typing import List

import requests as requests

from api.CurrencyExchange.currencyExchange import get_exchange_rate, CURRENCY
from api.marketplace import Marketplace, Item, tradeableItems, MARKETPLACE


class BuffMarketplace(Marketplace):
    marketplace_name = MARKETPLACE.BUFF
    fee = 0.975

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

    def sell_item(self, item):
        pass

    def get_balance(self) -> float:
        None
