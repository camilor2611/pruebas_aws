from abc import ABC, abstractmethod

from boto3.dynamodb.conditions import Key

from domain.entities.itemDynamo import ItemGetFiles, ItemUploadedFile


class IDynamoDB(ABC):
    @abstractmethod
    def create_item(self, item: ItemUploadedFile):
        pass

    @abstractmethod
    def get_items_by_file_id(self, file_id: str) -> ItemGetFiles:
        pass
