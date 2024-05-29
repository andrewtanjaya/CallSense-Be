from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


class ListDataBaseResponseModel(BaseModel):
    message: Optional[str] = None
    data: Optional[List] = []

    class Config:
        schema_extra = {
            "example": {
                "data": [],
                "message": "Get data successful",
            }
        }


class ListDataCursorBaseResponseModel(ListDataBaseResponseModel):
    is_last: Optional[bool] = False
    last_id: Optional[UUID]
    total_records: Optional[int] = 0

    def __init__(self, **data) -> None:
        super().__init__(data=data.get("data"))
        self._set_attributes(data)

    def _set_attributes(self, data: Dict) -> None:
        self.is_last = data.get("is_last")
        self.total_records = data.get("total_records")
        self.last_id = self.data[-1].id if not data.get("is_last") else None

    class Config:
        schema_extra = {
            "example": {
                "data": [],
                "is_last": True,
                "last_id": None,
                "total_records": 0,
            }
        }
