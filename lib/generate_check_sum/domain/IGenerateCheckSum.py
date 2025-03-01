from abc import ABC, abstractmethod

from domain.entities.itemDynamo import ItemUploadedFile


class IGenerateCheckSum(ABC):
    @abstractmethod
    def generate_check_sum(self, path_file: str, version_file: str) -> ItemUploadedFile:
        pass
