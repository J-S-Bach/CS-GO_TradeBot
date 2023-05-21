import time

from api.marketplace import Item
from api.dMarket import api as dMarketApi
from database.createDatabase import csgo_cur, csgoDB

last_offer_id: str


def update_buy_offers():
    global last_offer_id
    closed_buy_offers = dMarketApi.DMarketMarketplace().get_closed_buy_offers()

    time1 = round(time.time(), 1)
    for buy_offer in closed_buy_offers:
        t = csgo_cur.execute(
            'SELECT COUNT(*) FROM buy WHERE buy_id_3p ="' + buy_offer.offer_id + '"').fetchone()[0]
        if t == 0:
            def_index = \
            csgo_cur.execute('SELECT def_index FROM item_basis WHERE itemName="' + buy_offer.name + '"').fetchone()[0]
            print(def_index)
            csgo_cur.execute('INSERT INTO owned_items VALUES (NULL,?,?,?,?)',
                             (buy_offer.on_market.name, None, buy_offer.asset_id, def_index))

            internal_id = csgo_cur.execute('SELECT internal_id FROM owned_items ORDER BY internal_id desc').fetchone()[
                0]

            csgo_cur.execute('INSERT INTO buy VALUES (?,NULL,?,?,?,?)',
                             (internal_id, buy_offer.offer_id, buy_offer.price, buy_offer.on_market.name, time1))
    csgoDB.commit()
