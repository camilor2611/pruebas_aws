import os

import boto3
from boto3.dynamodb.conditions import Key

from domain.entities.itemDynamo import ItemGetFiles, ItemUploadedFile
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

    def get_items_by_file_id(self, file_id: str) -> ItemGetFiles:
        response = self.__table.query(
            KeyConditionExpression=Key("file_id").eq(file_id)
        )
        items = ItemGetFiles(items=response.get("Items", []) )
        return items
