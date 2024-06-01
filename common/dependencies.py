import firebase_admin
from firebase_admin import credentials, firestore,  storage
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from common.config import (
    DATABASE_URL,
    ENGINE_IMPLICIT_RETURNING,
    ENGINE_POOL_PRE_PING,
    ENGINE_POOL_RECYCLE,
    ENGINE_POOL_SIZE,
    ENGINE_POOL_USE_LIFO,
    GOOGLE_APPLICATION_CREDENTIALS,
    FIREBASE_STORAGE_BUCKET
)


class DB:
    def __init__(
        self,
        db_url,
        pool_size,
        implicit_returning,
        pool_pre_ping,
        pool_use_lifo,
        pool_recycle,
    ):
        engine = create_engine(
            db_url,
            pool_size=pool_size,
            implicit_returning=implicit_returning,
            pool_pre_ping=pool_pre_ping,
            pool_use_lifo=pool_use_lifo,
            pool_recycle=pool_recycle,
        )

        self.session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )

    def get_session(self):
        return self.session


db_service = DB(
    DATABASE_URL,
    ENGINE_POOL_SIZE,
    ENGINE_IMPLICIT_RETURNING,
    ENGINE_POOL_PRE_PING,
    ENGINE_POOL_USE_LIFO,
    ENGINE_POOL_RECYCLE,
)


def get_database():
    return db_service

## GOOGLE
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
app = firebase_admin.initialize_app(
    cred, {"storageBucket": FIREBASE_STORAGE_BUCKET}
)

store = firestore.client()


def get_firestore():
    return store


def get_storage():
    return storage.bucket()
