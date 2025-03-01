from typing import Optional
from pydantic import BaseModel, constr


class EventLoadFile(BaseModel):
    content: str
    content_type: str
    format_file: constr(pattern = r"^[a-zA-Z0-9]+$")
    create_new_version: Optional[bool] = False


class ResponseLoadFile(BaseModel):
    file_id: str
    path_s3: str
    version: int
    status: str