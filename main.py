from api.buff import api as buffApi
from api.csDeals import api as csDealsApi
from api.dMarket import api as dMarketApi
from api.steam import api


def main():

    #TODO: get all items we possess

    buff = buffApi.BuffMarketplace()
    cs_deals = csDealsApi.CSDealsMarketplace()
    d_market = dMarketApi.DMarketMarketplace()

    # get all offers
    buffOffers = buff.get_all_offers_lowest_price()
    csDealsOffers = cs_deals.get_all_offers_lowest_price()
    dmarketOffers = d_market.get_all_offers_lowest_price()







if __name__ == '__main__':
    main()
