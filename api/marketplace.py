from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class TradableItem:
    name: str
    buffId: str
    def_index: str

    def __init__(self, name, buff_id, def_index):
        self.buffId = buff_id
        self.name = name
        self.def_index = def_index


tradeable_items = [
    TradableItem("Shadow Case", "37510", "4138"),
    TradableItem("Revolver Case", "36354", "4186"),
    TradableItem("Operation Wildfire Case", "35895", "4187"),
    TradableItem("Clutch Case", "45237", "4471"),
    TradableItem("Danger Zone Case", "763236", None),
    TradableItem("Prisma Case 2", "779175", None),
    TradableItem("Glove Case", "35086", "4288"),
    TradableItem("Gamma 2 Case", "34987", "4281"),
    TradableItem("Operation Breakout Weapon Case", "35883", "4018"),
    TradableItem("Chroma 3 Case", "33820", "4233"),
    TradableItem("Spectrum 2 Case", "38148", "4403"),
    TradableItem("Operation Phoenix Weapon Case", "35890", "4011"),
    TradableItem("Operation Broken Fang Case", "835343", None),
    TradableItem("Chroma 2 Case", "34369", "4089"),
    TradableItem("Spectrum Case", "38150", "4351"),
    TradableItem("Gamma Case", "34989", "4236"),
    TradableItem("eSports 2013 Winter Case", "42346", "4005"),
    TradableItem("eSports 2014 Summer Case", "42347", None),
    TradableItem("Shattered Web Case", "774681", None),
    TradableItem("CS:GO Weapon Case", "34273", "4001"),
    TradableItem("CS:GO Weapon Case 2", "34274", "4004"),
    TradableItem("CS:GO Weapon Case 3", "34275", "4010"),
    TradableItem("Prisma Case", "769121", None),
    TradableItem("Prisma Case 2", "779175", None),
    TradableItem("Danger Zone Case", "763236", "4548"),
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


class BuyOffer(Item):
    offer_id: str

    def __init__(self, name, item_id, price, on_market, offer_id):
        super().__init__(name, item_id, price, on_market)
        self.offer_id = offer_id


class ItemNotAvailable(Exception):
    """"Raised when we try to access an item in an api, but the item cannot be found."""
    pass


class ItemsNotBought(Exception):
    """Raised when one or more items failed to get bought. Takes the amount of not bought items"""
    amount: int

    def __init__(self, amount):
        self.amount = amount
        super().__init__(f"{amount} items have not been bought.")


class Marketplace(ABC):
    @property
    @abstractmethod
    def marketplace_name(self):
        pass

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
    def sell_item(self, item: Item, amount=1) -> None:
        pass

    @abstractmethod
    def buy_item(self, item: Item, amount=1) -> None:
        pass

    @abstractmethod
    def create_buy_offer(self, item: Item) -> None:
        pass

    @abstractmethod
    def delete_buy_offer(self, buy_offer_id: str) -> None:
        pass

    @abstractmethod
    def get_buy_offers(self) -> Item:
        pass

    @abstractmethod
    def get_balance(self) -> float:
        pass
