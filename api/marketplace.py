from abc import ABC, abstractmethod


class Item:
    name: str
    assetId: str
    price: float

    def __init__(self, name, itemId, price):
        self.name = name
        self.id = itemId
        self.price = price


class Marketplace(ABC):
    rateLimit: int

    @abstractmethod
    def getItemDetail(self, name) -> Item:
        pass
