import os
import boto3
from domain.IStorage import IStorage


class Storage(IStorage):
    def __init__(self) -> None:
        self.__bucket = os.environ.get("BUCKET_NAME", None)
        self.__s3_client = boto3.client('s3')

    def download_file(self, file_path: str) -> bytes:
        response = self.__s3_client.get_object(Bucket=self.__bucket, Key=file_path)
        document = response['Body'].read()
        return document
