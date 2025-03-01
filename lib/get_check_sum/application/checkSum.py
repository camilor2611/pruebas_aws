from domain.IDynamoDB import IDynamoDB
from domain.entities.getCheckSum import GetCheckSum
from domain.entities.itemDynamo import ItemGetFile
from domain.ICheckSum import ICheckSum


class CheckSum(ICheckSum):
    def __init__(self, dynamo: IDynamoDB):
        self.__dynamo = dynamo

    def validate_check_sum(self, request: GetCheckSum) -> ItemGetFile | None:
        if request.version is None:
            result = self.__dynamo.get_items_by_file_id(request.file_id)
        else:
            result = self.__dynamo.get_item_by_file_id_version(
                request.file_id,
                request.version
            )

        if len(result.items) > 0:
            return result.items[0]
        