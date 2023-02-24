from api.buff import api as buffApi
from api.csDeals import api as csDealsApi


def main():
    buffMarketplace = buffApi.BuffMarketplace()
    csDealsMarketPlace = csDealsApi.CSDealsMarketplace()

    (csDealsMarketPlace.getLowestPrice("Glove Case"))
    item = csDealsMarketPlace.getLowestPrice("Sticker | Aleksib (Gold) | Rio 2022")

if __name__ == '__main__':
    main()
