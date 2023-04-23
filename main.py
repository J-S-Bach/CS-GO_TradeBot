from api.buff import api as buffApi
from api.csDeals import api as csDealsApi
from api.dMarket import api as dMarketApi
from api.steam import api
from operator import itemgetter

from api.steam.api import SteamApi


def main():

    #TODO: get all items we possess
    steam = SteamApi()
    steamItems = steam.get_all_owned_items_in_caskets()
    for steamItem in steamItems:
        print(steamItem.name)
        breakpoint()

    buff = buffApi.BuffMarketplace()
    cs_deals = csDealsApi.CSDealsMarketplace()
    d_market = dMarketApi.DMarketMarketplace()

    # get all offers
    buffOffers = buff.get_all_offers_lowest_price()
    csDealsOffers = cs_deals.get_all_offers_lowest_price()
    dmarketOffers = d_market.get_all_offers_lowest_price()


    itemList = []
    #find_profitable_trades
    for buffOffer in buffOffers:
        for csDealsOffer in csDealsOffers:
            if buffOffer.name == csDealsOffer.name:
                if csDealsOffer.price < buffOffer.price * buffApi.BuffMarketplace.fee:
                    print(csDealsOffer.name, csDealsOffer.price)
                    profit = round(buffOffer.price / csDealsOffer.price * 100 - 100, 4)
                    itemList.append(dict(zip(["from_item", "to_item", "profit"], [buffOffer, csDealsOffer, profit])))
        for dMarketOffer in dmarketOffers:
            if buffOffer.name == dMarketOffer.name:
                if dMarketOffer.price < buffOffer.price * buffApi.BuffMarketplace.fee:
                    print(dMarketOffer.name, dMarketOffer.price)
                    profit = round(buffOffer.price / dMarketOffer.price * 100 - 100, 4)
                    itemList.append(dict(zip(["from_item", "to_item", "profit"], [buffOffer, dMarketOffer, profit])))
    itemList = sorted(itemList, key=lambda d: d['profit'], reverse=True)
    steamItems = steam.get_all_owned_items_in_caskets()
    for steamItem in steamItems:
        print(steamItem.name)
        breakpoint()

    for item in itemList:
        print(item.values())
        print(item.keys())
    breakpoint()
    print(itemList)

    breakpoint()






if __name__ == '__main__':
    main()
