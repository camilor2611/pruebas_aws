from typing import Any

from application.storage import Storage
from application.processUploadFile import UploadFile
from application.dynamoDB import DynamoDB
from application.exceptions.custom import exception_decorator

from domain.entities.eventLoadFile import EventLoadFile


@exception_decorator
def main(event):
    event_obj = EventLoadFile(**event)
    storage_s3 = Storage()
    dynamo = DynamoDB()
    process_upload_file = UploadFile(
        storage=storage_s3,
        dynamo=dynamo
    )
    response = process_upload_file.run_process(event_obj)
    return {"success": True, "data": response.model_dump() }


def handler(event: Any, context: Any):
    return main(event)


if __name__ == "__main__":
    response = handler(
        {
            "content": "RVNUTyBFUyBVTiBBUkNISVZPIERFIFBSVUVCQQ==",
            "content_type": "text/plain",
            "format_file": "txt",
            "create_new_version": False
        },
        {}
    )
    print(response)
