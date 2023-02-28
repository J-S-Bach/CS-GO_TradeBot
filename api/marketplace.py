from abc import ABC, abstractmethod
from typing import List


class Item:
    name: str
    assetId: str
    price: float

    def __init__(self, name, itemId, price):
        self.name = name
        self.id = itemId
        self.price = price


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
