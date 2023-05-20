from api.buff.api import BuffMarketplace
from api.dMarket.api import DMarketMarketplace
from api.marketplace import ItemNotAvailable, Item, tradeable_items, MARKETPLACE
from api.steam.api import SteamApi
from datetime import datetime
from dateutil import parser


def check_buy_offer_dmarket(item: Item, amount=100):
    dmarket = DMarketMarketplace()

    # Check if market has a better price to offer and buy it if so
    try:
        best_offer_on_market = dmarket.get_best_offer_for_item(item.name)
        if best_offer_on_market.price <= item.price:
            dmarket.buy_item(best_offer_on_market)
            return
    except ItemNotAvailable:
        pass

    # Check if we have a current buy_offer for the same item but with different place or none and replace if so
    current_buy_offers = dmarket.get_buy_offers(item.name)

    for current_buy_offer in current_buy_offers:
        if current_buy_offer.name == item.name:
            if current_buy_offer.price != item.price:
                dmarket.delete_buy_offer(current_buy_offer.offer_id)
                dmarket.create_buy_offer(item, amount)
            break
    else:
        dmarket.create_buy_offer(item)


# TODO: Rename
def compare_buy_offers():
    buff = BuffMarketplace()
    steam = SteamApi()

    all_items_in_caskets = steam.get_all_owned_items_in_caskets()

    marge = 0.08

    for tradable_item in tradeable_items:
        available_items = 0

        # check if item is available in steam inventory AND if item is currently sellable
        for item_in_casket in all_items_in_caskets:
            if str(item_in_casket["def_index"]) == tradable_item.def_index \
                    and tradable_item.def_index is not None \
                    and item_in_casket["tradable_after"] is not None:
                tradable_after = parser.parse(str(item_in_casket["tradable_after"]))
                if tradable_after < datetime.now(tradable_after.tzinfo):
                    available_items += 1

        best_offer = buff.get_best_offer_for_item(tradable_item.name)

        if available_items >= 100:
            print("targetting", tradable_item.name, "for 100 times for",
                  float(best_offer.price) * (1.00 - marge))

            check_buy_offer_dmarket(
                Item(tradable_item.name, "", round(float(best_offer.price) * (1.00 - marge), 2), MARKETPLACE.DMARKET))
