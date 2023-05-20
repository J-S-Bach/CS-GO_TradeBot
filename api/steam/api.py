from javascript import require
import subprocess

class SteamApi:
    def __init__(self):
        # TODO: install packages with npm (silently?)
        # subprocess.check_call('cd ./JSSteamHandler && npm i', shell=True)

        CsGoHandler = require("./JSSteamHandler/SteamHandler.js")
        self.csgo_handler = CsGoHandler()

    def get_all_owned_items_in_caskets(self):
        """
        Cost intensive. Use with caution! \n
        returns all owned items, including the ones that are in caskets
        """
        return list(self.csgo_handler.getAllOwnedItemsInCaskets())

    def move_from_casket(self, item_asset_id, casket_asset_id):
        self.csgo_handler.moveFromCasket(item_asset_id, casket_asset_id)

    def move_to_casket(self, item_asset_id, casket_asset_id):
        self.csgo_handler.moveToCasket(item_asset_id, casket_asset_id)

    def get_all_owned_items_in_inventory(self):
        return list(self.csgo_handler.getAllOwnedItemsInInventory())

    def get_casket_content(self, asset_id):
        return list(self.csgo_handler.getCasketContent(asset_id))
