from abc import ABC, abstractmethod


class Item:
    name: str
    assetId: str
    price: float


class Marketplace(ABC):
    rateLimit: int

    @abstractmethod
    def getItemDetail(self, name) -> Item:
        pass
