from pydantic import BaseModel


class GetCheckSum(BaseModel):
    file_id: str
    version: int | None = None
