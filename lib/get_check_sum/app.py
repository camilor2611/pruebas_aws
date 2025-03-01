from domain.entities.getCheckSum import GetCheckSum
from application.dynamoDB import DynamoDB
from application.checkSum import CheckSum
from application.exceptions.custom import exception_decorator


@exception_decorator
def main(event):
    event_obj = GetCheckSum(**event)
    dynamo = DynamoDB()
    check = CheckSum(dynamo=dynamo)
    response_check_sum = check.validate_check_sum(event_obj)

    response = {"success": False, "data": {}}
    if response_check_sum is not None:
        response["success"] = True
        response["data"] = response_check_sum.model_dump()

    return response


def handler(event, context):
    return main(event)


if __name__ == "__main__":
    response = handler(
        {
            "file_id": "f16e1ab30c2e9ff43352ee0c5a7d966acb8e2fd0026552d3a887135a3254d8d4",
        },
        {}
    )
    print(response)
