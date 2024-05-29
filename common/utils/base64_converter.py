from base64 import b64decode, b64encode
from json import dumps as json_dumps
from json import loads as json_loads


def convert_json_to_base64(value: str) -> str:
    return b64encode(json_dumps(json_loads(value)).encode()).decode()


def convert_base64_to_json(value: str) -> dict:
    return json_loads(b64decode(value).decode())
