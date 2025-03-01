import os

import boto3
from boto3.dynamodb.conditions import Key

from domain.entities.itemDynamo import ItemGetFile, ItemGetFiles
from domain.IDynamoDB import IDynamoDB


class DynamoDB(IDynamoDB):
    def __init__(self):
        self.__table_name = os.environ.get("DYNAMO_TABLE_NAME", None)
        self.__dynamo = boto3.resource("dynamodb")
        self.__table = self.__dynamo.Table(self.__table_name)

    def get_items_by_file_id(self, file_id: str) -> ItemGetFiles:
        response = self.__table.query(
            KeyConditionExpression=Key("file_id").eq(file_id)
        )
        items = ItemGetFiles(items=response.get("Items", []) )
        return items

    def get_item_by_file_id_version(self, file_id: str, version: str) -> ItemGetFiles:
        response = self.__table.get_item(
            Key={
                "file_id": file_id,
                "version": version
            }
        )
        result = response.get("Item", {})
        return ItemGetFiles(
            items=[ItemGetFile(**result)]) if len(result) > 0 else ItemGetFiles(items=[]
        )
