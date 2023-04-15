from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class TradableItem:
    name: str
    buffId: str

    def __init__(self, name, buff_id):
        self.buffId = buff_id
        self.name = name


tradeableItems = [
    TradableItem("Glove Case", "35086"),
    TradableItem("Operation Breakout Weapon Case", "35883"),
    TradableItem("Gamma 2 Case", "34987"),
    TradableItem("Chroma 3 Case", "33820"),
    TradableItem("Spectrum 2 Case", "38148"),
    # TradeableItems("Operation Phoenix Weapon Case", "35890"),
    # TradeableItems("Operation Broken Fang Case", "835343"),
    # TradeableItems("Chroma 2 Case", "34369"),
    # TradeableItems("Spectrum Case", "38150"),
    # TradeableItems("Gamma Case", "34989"),
    # TradeableItems("eSports 2013 Winter Case", "42346"),
    # TradeableItems("eSports 2014 Summer Case", "42347"),
    # TradeableItems("Shattered Web Case", "774681"),
    TradableItem("CS:GO Weapon Case", "34273"),
    # TradeableItems("CS:GO Weapon Case 2", "34274"),
    # TradeableItems("CS:GO Weapon Case 3", "34275"),
    # TradeableItems("Prisma Case", "769121"),
    # TradeableItems("Prisma Case 2", "779175"),
    # TradeableItems("Danger Zone Case", "763236"),
]


class MARKETPLACE(Enum):
    BUFF = "BUFF"
    DMARKET = "DMARKET"
    CSDEALS = "CSDEALS"


class Item:
    """
    Price in USD
    """
    name: str
    assetId: str
    price: float
    on_market: MARKETPLACE

    def __init__(self, name, item_id, price, on_market):
        self.name = name
        self.assetId = item_id
        self.price = price
        self.on_market = on_market


class ItemNotAvailable(Exception):
    """"Raised when we try to access an item in an api, but the item cannot be found."""
    pass


class Marketplace(ABC):
    @abstractmethod
    def get_best_offer_for_item(self, name: str) -> Item:
        pass

    @abstractmethod
    def get_best_offer_for_item_list(self, names: List[str]) -> List[Item]:
        pass

    @abstractmethod
    def get_best_offers(self) -> List[Item]:
        pass

    @abstractmethod
    def sell_items(self, item: Item):
        pass
