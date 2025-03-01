from abc import ABC, abstractmethod

from domain.entities.itemDynamo import ItemUploadedFile


class IDynamoDB(ABC):
    @abstractmethod
    def create_item(self, item: ItemUploadedFile):
        """Método que permite crear un item en DynamoDB
        
        :param item: Esquema del nuevo Item        
        :type item: ItemUploadedFile
        """
        pass
