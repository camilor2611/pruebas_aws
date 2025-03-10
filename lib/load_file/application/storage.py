import os
import boto3
from domain.IStorage import IStorage


class Storage(IStorage):
    def __init__(self) -> None:
        self.__bucket = os.environ.get("BUCKET_NAME", None)
        self.__s3_client = boto3.client('s3')

    def upload_file(self, path: str, body: bytes, content_type: str):
        self.__s3_client.put_object(
            Bucket=self.__bucket,
            Key=path,
            Body=body,
            ContentType=content_type
        )
