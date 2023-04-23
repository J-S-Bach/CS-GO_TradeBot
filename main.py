from api.buff.api import BuffMarketplace
from api.marketplace import tradeableItems, Item
from api.dMarket import api as dmarket
from trade_logic.dealing import get_profitable_offers


def main():
    asd = dmarket.DMarketMarketplace()

    print(asd.buy_item(Item("Clutch Case", "", 3, "")))


if __name__ == '__main__':
    main()
