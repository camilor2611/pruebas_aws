from decimal import Decimal
from typing import List

from pydantic import BaseModel, field_serializer


class ItemGetFile(BaseModel):
    file_id: str
    path_s3: str
    version: Decimal

    @field_serializer("version")
    def serialize_version(self, value: Decimal) -> int:
        return int(value)

class ItemGetFiles(BaseModel):
    items: List[ItemGetFile]