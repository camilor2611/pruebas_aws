from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def upload_file(self, path: str, body: bytes, content_type: str):
        """Método que permite subir archivos a un bucket de S3.
        
        :param file: El archivo que se desea subir
        :param filename: Nombre del archivo y su extensión
        
        :type file: bytes
        :type filename: str
        """
        pass
    
    @abstractmethod
    def download_file(self, file_path: str) -> bytes:
        """Método que permite descagar archivos a un bucket de S3.
        
        :param file_path: El archivo que se desea descagar        

        :type file_path: str

        :return: Retorna el archivo descargado en bytes
        :rtype: bytes
        """
        pass