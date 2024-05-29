from binascii import Error
from json import JSONDecodeError
from json import loads as json_loads
from typing import Dict, Union

from fastapi import Header
from pybase64 import b64decode

from common.exception import UnauthorizedError
from common.helper.x_user_data import ApplicationData, UserData, XUserData
from common.helper.x_user_data.enum import IssuerType


def get_user_data(
    x_user_data: str = Header(None),
) -> XUserData:
    return decode_x_user_data(x_user_data)


def decode_x_user_data(x_user_data: str) -> Union[ApplicationData, UserData]:
    try:
        decoded_user_data = validate_x_user_data(x_user_data)
        if decoded_user_data.get("application_id"):
            return ApplicationData(**decoded_user_data)
        return UserData(**decoded_user_data)
    except Exception:
        raise ValueError("issuer not found")


def validate_x_user_data(x_user_data: str) -> Dict:
    try:
        return json_loads(b64decode(x_user_data).decode())
    except Error:
        raise UnauthorizedError(message="invalid base64 encoding.")
    except JSONDecodeError:
        raise UnauthorizedError(message="invalid JSON string format.")


def get_issuer_by_instance(user_data: XUserData) -> str:
    if isinstance(user_data, ApplicationData):
        return IssuerType.APP.generate_log(user_data.application_id)
    if isinstance(user_data, UserData):
        return IssuerType.ACCOUNT.generate_log(user_data.account_id)
    raise ValueError("issuer not found")
