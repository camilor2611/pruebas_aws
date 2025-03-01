from abc import ABC, abstractmethod

from domain.entities.itemDynamo import ItemUploadedFile


class IDynamoDB(ABC):
    @abstractmethod
    def create_item(self, item: ItemUploadedFile):
        pass
