from typing import List, Optional
from uuid import UUID

import google.cloud

from common.orm.recording import RecordingSQL
from src.call.domain.entity import Recording
from src.call.domain.interface import FireStoreAbstractExternal


class FirestoreExternal(FireStoreAbstractExternal):
    def __init__(self, store) -> None:
        self.store = store

    def get_collections(self):
        doc_ref = self.store.collection("users").limit(2)

        try:
            docs = doc_ref.get()
            for doc in docs:
                print("Doc Data:{}".format(doc.to_dict()))
        except google.cloud.exceptions.NotFound:
            print("Missing data")
