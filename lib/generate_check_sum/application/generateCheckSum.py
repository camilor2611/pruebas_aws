import hashlib
from domain.IStorage import IStorage
from domain.IDynamoDB import IDynamoDB
from domain.entities.itemDynamo import ItemUploadedFile
from domain.IGenerateCheckSum import IGenerateCheckSum


class GenerateCheckSum(IGenerateCheckSum):
    def __init__(
            self,
            storage: IStorage,
            dynamo: IDynamoDB
        ):
        self.__storage = storage
        self.__dynamo = dynamo

    def generate_check_sum(self, path_file: str, version_file: str) -> ItemUploadedFile:
        file_content = self.__storage.download_file(path_file)
        file_hash_id = hashlib.sha256(file_content).hexdigest()
        new_check_sum = ItemUploadedFile(
            file_id=file_hash_id,
            path_s3=path_file,
            version=version_file
        )
        self.__dynamo.create_item(new_check_sum)
        return new_check_sum