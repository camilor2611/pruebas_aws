import time
from typing import Dict, List
import logging
logging.basicConfig(level=logging.INFO)

from application.generateCheckSum import GenerateCheckSum
from application.storage import Storage
from application.dynamoDB import DynamoDB


def handler(event: Dict, context):
    records: List = event.get("Records", [])
    if len(records) == 0:
        return {"success": False, "data": []}
    
    record: Dict = records[0]
    data_s3: Dict  = record.get("s3", {})
    object_s3: Dict  = data_s3.get("object", {})
    path_file: str = object_s3.get("key", None)

    if path_file is None:
        return {"success": False, "data": []}

    name_file = path_file.split("/")[-1]
    version_file = name_file.split("_")[0]

    storage = Storage()
    dynamo = DynamoDB()
    generate_check_sum = GenerateCheckSum(storage=storage, dynamo=dynamo)
    time.sleep(10)
    generate_check_sum.generate_check_sum(path_file, version_file)

    return {"success": True, "data": []}


if __name__ == "__main__":
    response = handler(
        {
            "Records": [
                {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "2025-03-01T01:55:36.436Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "AZDCV9NQRUYS9"
                },
                "requestParameters": {
                    "sourceIPAddress": "181.134.30.139"
                },
                "responseElements": {
                    "x-amz-request-id": "JC86AKZADQJEVQ5V",
                    "x-amz-id-2": "a7InRKdqHYuuGBPEOKNsg4Yj15sQpNeXtDNWyiOKjAeLP5ZNC6BMTe0j2ErCjQIFcipUnhk9HLUCApxvoJ6XTmNTngNx0N5M"
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "arn:aws:cloudformation:us-east-1:820242922903:stack/devStackLambdas/66d30c50-f618-11ef-93f8-127ef0c14fc3-4081018904954888891",
                    "bucket": {
                    "name": "bcrcpreciaco",
                    "ownerIdentity": {
                        "principalId": "AZDCV9NQRUYS9"
                    },
                    "arn": "arn:aws:s3:::bcrcpreciaco"
                    },
                    "object": {
                    "key": "files/1740796142_86d4fa40-325d-403b-8c66-a36fab999791.txt",
                    "size": 28,
                    "eTag": "0f756559aaf1a1b8668de70cda0b1a2b",
                    "sequencer": "0067C2691867CC2F4A"
                    }
                }
                }
            ]
            },
        {}
    )
    logging.info(response)
