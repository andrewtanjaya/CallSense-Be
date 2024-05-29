from enum import Enum


class ErrorCode(str, Enum):
    INVALID_PAYLOAD = "400"
    UNAUTHORIZED = "401"
    FORBIDDEN = "403"
    NOT_FOUND = "404"
    TOO_MANY_REQUESTS = "429"
    INTERNAL_SERVER_ERROR = "500"
