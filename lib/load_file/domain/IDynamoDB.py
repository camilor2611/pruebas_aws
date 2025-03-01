from abc import ABC, abstractmethod

from domain.entities.itemDynamo import ItemGetFiles


class IDynamoDB(ABC):
    @abstractmethod
    def get_items_by_file_id(self, file_id: str) -> ItemGetFiles:
        pass
