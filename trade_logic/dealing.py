from api.buff import api as buffApi
from api.csDeals import api as csDealsApi
from api.dMarket import api as dMarketApi
from api.marketplace import Item, MARKETPLACE
from api.steam.api import SteamApi

steam = SteamApi()
buff = buffApi.BuffMarketplace()
cs_deals = csDealsApi.CSDealsMarketplace()
d_market = dMarketApi.DMarketMarketplace()


class ProfitableOffer:
    sell_item: Item
    buy_item: Item
    profit: float

    def __init__(self, sell_item, buy_item, profit):
        self.sell_item = sell_item
        self.buy_item = buy_item
        self.profit = profit

    def __lt__(self, other):
        return self.profit < other.profit


def get_profitable_offers() -> list[ProfitableOffer]:
    # get all offers
    buff_offers = buff.get_best_offers()
    cs_deals_offers = cs_deals.get_best_offers()
    dmarket_offers = d_market.get_best_offers()

    offer_list: list[ProfitableOffer] = []

    # find profitable trades
    # TODO: Once we want it: implement it in a way that every market is compared with every other market.
    for buffOffer in buff_offers:

        for csDealsOffer in cs_deals_offers:
            if buffOffer.name == csDealsOffer.name:
                if csDealsOffer.price < buffOffer.price * buffApi.BuffMarketplace.fee:
                    # TODO: I doubt the next line is correct. because: percentage? and fee missing
                    profit = round(buffOffer.price / csDealsOffer.price * 100 - 100, 4)
                    offer_list.append(ProfitableOffer(buffOffer, csDealsOffer, profit))

        for dMarketOffer in dmarket_offers:
            if buffOffer.name == dMarketOffer.name:
                if dMarketOffer.price < buffOffer.price * buffApi.BuffMarketplace.fee:
                    # TODO: I doubt the next line is correct. because: percentage? and fee missing
                    profit = round(buffOffer.price / dMarketOffer.price * 100 - 100, 4)
                    offer_list.append(ProfitableOffer(buffOffer, dMarketOffer, profit))

    # sort offers by percentual profit
    offer_list.sort(reverse=True)

    # TODO: Check if item exists in steam inventory (works with defindex) AND is currently sellable

    return offer_list


def buy_items(offer_list: list[ProfitableOffer]):
    for offer in offer_list:
        if offer.buy_item.on_market == MARKETPLACE.DMARKET:
            pass

        if offer.buy_item.on_market == MARKETPLACE.BUFF:
            pass

        if offer.buy_item.on_market == MARKETPLACE.CSDEALS:
            pass
