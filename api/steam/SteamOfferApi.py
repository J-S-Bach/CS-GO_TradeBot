import os

from javascript import require
import subprocess


class CsGoCasketApi:
    def __init__(self):
        os.system('cmd /c "cd ./api/steam/JSSteamHandler && npm i"')

        SteamOfferHandler = require("./JSSteamHandler/TradeOfferHandler.js")
        self.steam_offer_handler = SteamOfferHandler()

#     TODO: implement functions
