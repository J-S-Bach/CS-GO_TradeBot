import time

from database.createDatabase import csgo_cur, csgoDB


def insertBuy():
    time1 = round(time.time(), 1)
    itemPlace = "dMarket"
    asset_id_steam = None
    asset_id_3p = None
    def_index = "TODO"
    csgo_cur.execute('INSERT INTO owned_items VALUES (NULL,?,?,?,?,?)',
                                 (itemPlace, asset_id_steam, asset_id_steam, asset_id_3p, def_index))
    highest_id = csgo_cur.execute('SELECT internal_id FROM owned_items DESC').fetchone()
    print(highest_id)
    breakpoint()

    internal_id = "TODO"
    buyPrice = 2
    internal_id = "TODO"
    csgo_cur.execute('INSERT INTO buy VALUES (?,NULL,?,?,?)',
                                 (internal_id, buyPrice, itemPlace, time1))
    csgoDB.commit()
def insertSell():
    print("TEST")