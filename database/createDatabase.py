import os
import sqlite3

csgoDB = sqlite3.connect("CSGO.db")
csgo_cur = csgoDB.cursor()


buy = '''CREATE TABLE IF NOT EXISTS buy
            (internal_id, buy_id, buy_id_3p,buyPrice, buyPlatform, buytime)'''
sell = '''CREATE TABLE IF NOT EXISTS sell
            (internal_id, sell_id, sellPrice, sellPlatform, selltime)'''
owned_items = '''CREATE TABLE IF NOT EXISTS owned_items
            (internal_id, itemPlace, asset_id_steam, asset_id_3p, def_index)'''
item_basis = '''CREATE TABLE IF NOT EXISTS item_basis
            (def_index, itemName,class_id, buff_goods_id, item_class)'''

def createDatabase():
    csgo_cur.execute('''DROP TABLE IF EXISTS owned_items''')
    csgo_cur.execute(owned_items)
    csgo_cur.execute('''DROP TABLE IF EXISTS buy''')
    csgo_cur.execute(buy)
    csgo_cur.execute('''DROP TABLE IF EXISTS sell''')
    csgo_cur.execute(sell)
    csgo_cur.execute('''DROP TABLE IF EXISTS item_basis''')
    csgo_cur.execute(item_basis)
    csgo_cur.execute(item_basis)
    list = [
        [4288, "Glove Case", "2066632015", "35086", None],
        [4236, "Gamma Case", "1797256701", "34989", None],
        [4281, "Gamma 2 Case", "1923037342", "34987", None],
        [4089, "Chroma 2 Case", "926978479", "34369", None],
        [4233, "Chroma 3 Case", "1690096482", "33820", None],
        [4351, "Spectrum Case", "2209581061", "38150", None],
        [4403, "Spectrum 2 Case", "2521767801", "38148", None],
        [4011, "Operation Phoenix Weapon Case", "384801319", "35890", None],
        #[None, "Operation Broken Fang Case", "4114525951", "835343", None],
        [4018, "Operation Breakout Weapon Case", "5288787014", "35883", None],
        [4005, "eSports 2013 Winter Case", "384801283", "42346", None],
        #[None, "eSports 2014 Summer Case", "5290283501", "42347", None],
        #[None, "Shattered Web Case", "3600645128", "774681", None],
        [4001, "CS:GO Weapon Case", None, "34273", None],
        [4004, "CS:GO Weapon Case 2", None, "34274", None],
        [4010, "CS:GO Weapon Case 3", None, "34275", None],
        #[None, "Prisma Case", "3213411179", "769121", None],
        #[None, "Prisma Case 2", "3761545285", "779175", None],
        [4548, "Danger Zone Case", "5291853350", "763236", None],
        [4138, "Shadow Case", "1293508920", "37510", None],
        [4186, "Revolver Case", "1432174707", "36354", None],
        [4187, "Operation Wildfire Case", "1544067968", "35895", None],
        [4471, "Clutch Case", "2727227113", "45237", None],
    ]
    csgo_cur.executemany('''INSERT OR IGNORE INTO item_basis VALUES (?,?,?,?,?)''', list)
    csgoDB.commit()