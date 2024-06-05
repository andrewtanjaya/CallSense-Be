import logging
from datetime import timedelta

from google.cloud.storage import Bucket

from src.call.domain.interface import FireStorageAbstractExternal


class FireStorageExternal(FireStorageAbstractExternal):
    def __init__(self, bucket: Bucket) -> None:
        self.bucket = bucket

    def upload(self, file_name: str) -> str:
        blob = self.bucket.blob(f"{file_name[2:]}")

        try:
            # Upload the file to Firebase Storage
            blob.upload_from_filename(file_name, content_type="audio/wav")
        except Exception as e:
            # Log any exceptions that occur during the upload process
            logging.error(f"Error uploading file: {e}")
            return None

        return blob.public_url

    def get_storage_url(self, object_name: str, expiration=3600) -> str:
        blob = self.bucket.blob(object_name)
        return blob.public_url
