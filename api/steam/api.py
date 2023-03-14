from javascript import require


class SteamApi:
    def __init__(self):
        CsGoHandler = require("./JSSteamHandler/SteamHandler.js")
        self.csgo_handler = CsGoHandler()

    def get_all_owned_items_in_caskets(self):
        """
        Cost intensive. Use with caution! \n
        returns all owned items, including the ones that are in caskets
        """
        return list(self.csgo_handler.getAllOwnedItemsInCaskets())

    # TODO: Test
    def move_from_casket(self, item_asset_id, casket_asset_id):
        self.csgo_handler.moveFromCasket(item_asset_id, casket_asset_id)

    # TODO: Test
    def move_to_casket(self, item_asset_id, casket_asset_id):
        self.csgo_handler.moveToCasket(item_asset_id, casket_asset_id)

    # # Do we need it like this? If yes, we should instead save it to the Database,
    # # but i believe we need all tradeable items in inventory which we can filter.
    # def check_if_item_tradeable(self, asset_id):
    #     return self.csgo_handler.checkIfItemTradeable(asset_id)

    def get_all_owned_items_in_inventory(self):
        return list(self.csgo_handler.getAllOwnedItemsInInventory())

    def get_casket_content(self, asset_id):
        return list(self.csgo_handler.getCasketContent(asset_id))
