from enum import Enum

# Reference:
# https://handbook.internal.verihubs.com/doc/error-response-6t8Fht4RsE


class ErrorCode(str, Enum):
    INVALID_PAYLOAD = "400"
    UNAUTHORIZED = "401"
    FORBIDDEN = "403"
    NOT_FOUND = "404"
    TOO_MANY_REQUESTS = "429"
    INTERNAL_SERVER_ERROR = "500"
