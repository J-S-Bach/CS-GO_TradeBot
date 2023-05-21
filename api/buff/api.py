import time
from typing import List

import requests as requests

from api.CurrencyExchange.currencyExchange import get_exchange_rate, CURRENCY
from api.marketplace import Marketplace, Item, tradeable_items, MARKETPLACE, ItemNotAvailable


class BuffMarketplace(Marketplace):
    marketplace_name = MARKETPLACE.BUFF
    fee = 1 - 0.975

    def get_best_offer_for_item(self, name) -> Item:
        for item in tradeable_items:
            if item.name == name:
                answer = requests.get(
                    f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={item.buffId}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_={int(time.time())}").json()
                buy_price = answer['data']['items'][0]['price']
                return Item(item.name, None, float(buy_price) * get_exchange_rate(CURRENCY.CNY, CURRENCY.USD),
                            on_market=self.marketplace_name)
        else:
            raise Exception("No valid ItemName given")

    def get_best_offers(self) -> List[Item]:
        buff_items = []

        for item in tradeable_items:
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
            'Device-Id': 'l40vB6x92paqjkhfYVqc',
            'Locale-Supported': 'en',
            'session': '1-1xRYWCTSO4oCdoh_2Iux2L9n7Ymajsniy8CTzgIhM31c2032647117',
            'game': 'csgo',
            'csrf_token': 'ImZiZWUxY2I0ZDkyZTU5ZGYzMmY3N2U2ZTkwZjY0YjE1NWI4Y2U1Yzgi.F0to5A.ej3puC3GTHTOHNXGAIfus7L7wnU',
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

    def buy_item(self, item: Item, amount=1):
        raise NotImplemented()

    def create_buy_offer(self, item: Item):
        raise NotImplemented()

    def delete_buy_offer(self, buy_offer_id: str):
        raise NotImplemented()

    def get_buy_offers(self):
        raise NotImplemented()

    def accept_sell_offer(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,af;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': 'Device-Id=l40vB6x92paqjkhfYVqc; Locale-Supported=en; session=1-1xRYWCTSO4oCdoh_2Iux2L9n7Ymajsniy8CTzgIhM31c2032647117; game=csgo; csrf_token=ImZiZWUxY2I0ZDkyZTU5ZGYzMmY3N2U2ZTkwZjY0YjE1NWI4Y2U1Yzgi.F0tooA.69xp-N3PpOFuGTOMyRd_lOs7InY',
            'Pragma': 'no-cache',
            'Referer': 'https://buff.163.com/market/sell_order/to_deliver?game=csgo',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        params = {
            '_': str(int(time.time() * 1000)),
        }
        response = requests.get('https://buff.163.com/api/market/steam_trade', params=params, cookies=self.create_cookies(),
                                headers=headers).json()
        dataBody = []
        for x in response['data']:
            assetList = []
            for y in x['items_to_trade']:
                assetList.append(y['assetid'])
            goodsID = x['items_to_trade'][0]['goods_id']
            #ToDo Here TradeOffer akzeptieren
            print("Offer here: https://steamcommunity.com/tradeoffer/" + str(x['tradeofferid']))
            keys = ["tradeofferid", "Item", "amount", 'assets', "status"]
            values = [x['tradeofferid'], x['goods_infos'][str(goodsID)]['market_hash_name'], len(x['items_to_trade']),
                      assetList, "offer  accepted - check if trade succeed"]
            dataBody.append(dict(zip(keys, values)))
        
        return dataBody

    def get_closed_buy_offers(self):
        raise NotImplemented()


