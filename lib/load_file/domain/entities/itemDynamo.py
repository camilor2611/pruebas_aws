from decimal import Decimal
from typing import List

from pydantic import BaseModel


class ItemUploadedFile(BaseModel):
    file_id: str
    path_s3: str
    version: int


class ItemGetFile(BaseModel):
    file_id: str
    path_s3: str
    version: Decimal


class ItemGetFiles(BaseModel):
    items: List[ItemGetFile]