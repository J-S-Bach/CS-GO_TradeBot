from api.CurrencyExchange.currencyExchange import get_exchange_rate, CURRENCY
from api.buff.api import BuffMarketplace
from api.dMarket.api import DMarketMarketplace as dmarket
from api.csDeals.api import CSDealsMarketplace
from api.marketplace import Item
from trade_logic.buy_offer_management import check_buy_offer_dmarket, compare_buy_offers


def main():
    compare_buy_offers()



if __name__ == '__main__':
    main()
