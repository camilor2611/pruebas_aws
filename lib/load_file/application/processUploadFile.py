from datetime import datetime
import base64
import hashlib
import logging
import uuid

from domain.IStorage import IStorage
from domain.entities.eventLoadFile import EventLoadFile, ResponseLoadFile
from domain.IProcessUploadFile import IUploadFile
from domain.IDynamoDB import IDynamoDB
from domain.entities.itemDynamo import ItemUploadedFile


class UploadFile(IUploadFile):
    def __init__(self, storage: IStorage, dynamo: IDynamoDB):
        self.__storage = storage
        self.__dynamo = dynamo
        
    def run_process(self, event: EventLoadFile) -> ResponseLoadFile:
        file_content_base64 = event.content
        content_type = event.content_type
        file_content = base64.b64decode(file_content_base64)
        file_hash_id = hashlib.sha256(file_content).hexdigest()
        results_items = self.__dynamo.get_items_by_file_id(file_hash_id)  # validar si existe en Dynamo DB
        
        # subir archivo si no existe o si se desea crear otra version
        if len(results_items.items) == 0 or event.create_new_version:
            format_file = event.format_file
            name_file = str(uuid.uuid4())
            timestamp_version  = int(datetime.timestamp(datetime.now()))
            file_path = f"files/{str(timestamp_version)}_{name_file}.{format_file}"
            # new_item = ItemUploadedFile(
            #     file_id=file_hash_id,
            #     path_s3=file_path,
            #     version=timestamp_version,
            # )
            # self.__dynamo.create_item(new_item)
            self.__storage.upload_file(file_path, file_content, content_type)
            response = ResponseLoadFile(
                file_id=file_hash_id,
                version=timestamp_version,
                path_s3=file_path,
                status="PROCESSING" 
            )
        else:
            data_file = results_items.items[-1]
            response = ResponseLoadFile(
                file_id=data_file.file_id,
                version=int(data_file.version),
                path_s3=data_file.path_s3,
                status="READY"
            )
            print("No se creo nueva version")

        return response
