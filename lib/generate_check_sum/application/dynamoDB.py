import os

import boto3

from domain.entities.itemDynamo import ItemUploadedFile
from domain.IDynamoDB import IDynamoDB


class DynamoDB(IDynamoDB):
    def __init__(self):
        self.__table_name = os.environ.get("DYNAMO_TABLE_NAME", None)
        self.__dynamo = boto3.resource("dynamodb")
        self.__table = self.__dynamo.Table(self.__table_name)

    def create_item(self, item: ItemUploadedFile):
        self.__table.put_item(
            Item = item.model_dump()
        )
