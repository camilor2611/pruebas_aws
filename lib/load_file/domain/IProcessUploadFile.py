from abc import ABC, abstractmethod
from domain.entities.eventLoadFile import EventLoadFile, ResponseLoadFile


class IUploadFile(ABC):
    @abstractmethod
    def run_process(self, event: EventLoadFile) -> ResponseLoadFile:
        pass
