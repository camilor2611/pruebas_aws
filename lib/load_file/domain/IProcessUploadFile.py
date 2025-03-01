from abc import ABC, abstractmethod
from domain.entities.eventLoadFile import EventLoadFile, ResponseLoadFile


class IUploadFile(ABC):
    @abstractmethod
    def run_process(self, event: EventLoadFile) -> ResponseLoadFile:
        """
        Este metodo se encarga de la lógica para subir el archivo a S3

        :param event: Es el evento que contiene la informacion del archivo que se va a subir

        :type event: EventLoadFile
        :return: Retorna un objeto con información del archivo que se subió
        :rtype: ResponseLoadFile
        """
        pass
