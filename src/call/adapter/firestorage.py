from src.call.domain.interface import FireStorageAbstractExternal


class FireStorageExternal(FireStorageAbstractExternal):
    def __init__(self, bucket) -> None:
        self.bucket = bucket

    def upload(self, file_name: str):
        blob = self.bucket.blob(file_name)
        blob.upload_from_filename(file_name)
