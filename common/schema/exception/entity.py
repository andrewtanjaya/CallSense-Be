from pydantic import BaseModel

# Reference:
# https://handbook.internal.verihubs.com/doc/error-response-6t8Fht4RsE


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
