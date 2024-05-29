from enum import IntEnum

# Reference:
# https://handbook.internal.verihubs.com/doc/error-response-6t8Fht4RsE


class ErrorCode(IntEnum):
    INVALID_PAYLOAD = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_CONTENT = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
