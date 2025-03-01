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

    @abstractmethod
    def get_item_by_file_id_version(self, file_id: str, version: str) -> ItemGetFiles:
        """
        Este método busca en DynamoDB mediante el file_id y la version
        
        :param file_id: ID del archivo que se quiere encontrar
        :param version: Version del archivo
        :type file_id: str

        :return: Retorna los Items encontrados
        :rtype: ItemGetFiles
        """
        pass