from pydantic import BaseModel


class ErrorField(BaseModel):
    field: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "field": "email",
                "message": "email is required",
            }
        }
