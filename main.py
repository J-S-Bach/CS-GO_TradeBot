import os

from api.buff import api as buffApi
from api.csDeals import api as csDealsApi
from api.dMarket import api as dMarketApi
from api.steam import api
from operator import itemgetter

from api.steam.api import SteamApi
from database import createDatabase
from database.createDatabase import csgo_cur


def main():
    if not os.path.isfile("CSGO.db") or bool(os.getenv('DATABASE_RESET')):
        createDatabase.createDatabase()


if __name__ == '__main__':
    main()
