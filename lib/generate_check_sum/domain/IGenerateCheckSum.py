from abc import ABC, abstractmethod

from domain.entities.itemDynamo import ItemUploadedFile


class IGenerateCheckSum(ABC):
    @abstractmethod
    def generate_check_sum(self, path_file: str, version_file: str) -> ItemUploadedFile:
        """
        Este metodo descarga de S3 y genera el hash256 del contenido y sube el nuevo Item en DynamoDB

        :param path_file: Ubicacion del archivo en S3
        :param version: Versión del archivo

        :type path_file: str
        :type version_file: str

        :return: Retorna el Item registrado en Dynamo
        :rtype: ItemUploadedFile
        """
        pass
