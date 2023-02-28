from api.buff import api as buffApi
from api.csDeals import api as csDealsApi
from api.dMarket import api as dMarketApi
from api.steam import api

def main():
    buffMarketplace = buffApi.BuffMarketplace()
    # csDealsMarketPlace = csDealsApi.CSDealsMarketplace()
    #
    # (csDealsMarketPlace.getLowestPrice("Glove Case"))
    # # item = csDealsMarketPlace.getLowestPrice("Sticker | Aleksib (Gold) | Rio 2022")
    #
    # dMarketMarketplace = dMarketApi.DMarketMarketplace()
    # for i in dMarketMarketplace.getLowestPriceForItemList(["Glove Case", "Operation Breakout Case"]):
    #     print(i.name)

    steamAPI = api.SteamApi()

if __name__ == '__main__':
    main()
