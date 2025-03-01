from abc import ABC, abstractmethod

from domain.entities.itemDynamo import ItemGetFiles, ItemGetFile


class IDynamoDB(ABC):
    @abstractmethod
    def get_items_by_file_id(self, file_id: str) -> ItemGetFiles:
        pass

    @abstractmethod
    def get_item_by_file_id_version(self, file_id: str, version: str) -> ItemGetFiles:
        pass