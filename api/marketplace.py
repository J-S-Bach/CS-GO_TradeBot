from abc import ABC, abstractmethod
from typing import List


class TradeableItems:
    name: str
    buffId: str

    def __init__(self, name, buffId):
        self.buffId = buffId
        self.name = name


tradeableItems = [
    TradeableItems("Glove Case", "35086"),
    TradeableItems("Operation Breakout Weapon Case", "35883"),
    TradeableItems("Gamma 2 Case", "34987"),
    TradeableItems("Chroma 3 Case", "33820"),
    TradeableItems("Spectrum 2 Case", "38148"),
    #TradeableItems("Operation Phoenix Weapon Case", "35890"),
    #TradeableItems("Operation Broken Fang Case", "835343"),
    #TradeableItems("Chroma 2 Case", "34369"),
    #TradeableItems("Spectrum Case", "38150"),
    #TradeableItems("Gamma Case", "34989"),
    #TradeableItems("eSports 2013 Winter Case", "42346"),
    #TradeableItems("eSports 2014 Summer Case", "42347"),
    #TradeableItems("Shattered Web Case", "774681"),
    TradeableItems("CS:GO Weapon Case", "34273"),
    #TradeableItems("CS:GO Weapon Case 2", "34274"),
    #TradeableItems("CS:GO Weapon Case 3", "34275"),
    #TradeableItems("Prisma Case", "769121"),
    #TradeableItems("Prisma Case 2", "779175"),
    #TradeableItems("Danger Zone Case", "763236"),
]


class Item:
    """
    Price in USD
    """
    name: str
    assetId: str
    price: float
    on_market: str

    def __init__(self, name, item_id, price, on_market):
        self.name = name
        self.assetId = item_id
        self.price = price
        self.on_market = on_market


class Marketplace(ABC):
    @abstractmethod
    def getItemDetail(self, name: str) -> Item:
        pass

    @abstractmethod
    def getItemDetailForItemList(self, name: List[str]):
        pass

    @abstractmethod
    def getLowestPrice(self, name: str) -> Item:
        pass

    @abstractmethod
    def getLowestPriceForItemList(self, names: List[str]) -> List[Item]:
        pass

    @abstractmethod
    def get_all_offers_lowest_price(self) -> List[Item]:
        pass

    @abstractmethod
    def get_balance(self) -> float:
        pass

    @abstractmethod
    def buy_items(self, item: Item, amount: int = 1):
        pass
