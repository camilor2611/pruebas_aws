from abc import ABC, abstractmethod

from domain.entities.itemDynamo import ItemGetFiles


class IDynamoDB(ABC):
    @abstractmethod
    def get_items_by_file_id(self, file_id: str) -> ItemGetFiles:
        """
        Este método busca en DYnamoDB mediante el file_id
        
        :param file_id: ID del archivo que se quiere encontrar
        :type file_id: str

        :return: Retorna los Items encontrados
        :rtype: ItemGetFiles
        """
        pass
