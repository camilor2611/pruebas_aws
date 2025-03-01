from abc import ABC, abstractmethod
from domain.entities.getCheckSum import GetCheckSum
from domain.entities.itemDynamo import ItemGetFile


class ICheckSum(ABC):
    @abstractmethod
    def validate_check_sum(self, request: GetCheckSum) -> ItemGetFile | None:
        """
        Valida que el archivo ya este registrado en Dynamo DB

        :param request: Esquema del request, contiene informacion de id y version
        :type request: GetCheckSum

        :return: Retorna un esquema tipo ItemGetFile
        :rtype: ItemGetFile
        """
        pass
