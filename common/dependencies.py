import logging

import firebase_admin
from firebase_admin import credentials, firestore, storage
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceEndpoint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain_community.document_loaders import PyPDFDirectoryLoader
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from common.config import (
    DATABASE_URL,
    ENGINE_IMPLICIT_RETURNING,
    ENGINE_POOL_PRE_PING,
    ENGINE_POOL_RECYCLE,
    ENGINE_POOL_SIZE,
    ENGINE_POOL_USE_LIFO,
    FIREBASE_STORAGE_BUCKET,
    GOOGLE_APPLICATION_CREDENTIALS,
    HUGGINGFACE_HUB_API_TOKEN,
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


# LLM

repo_id = "google/gemma-2b-it"
# Create an instance of the HuggingFaceEndpoint class with specified parameters
llm = HuggingFaceEndpoint(
    repo_id=repo_id,  # ID of the Hugging Face model repository
    max_length=264,  # Maximum length of generated text
    temperature=0.5,  # Sampling temperature for text generation
    huggingfacehub_api_token=HUGGINGFACE_HUB_API_TOKEN,
)


# Instantiate a PyPDFDirectoryLoader object with the specified directory path
loader = PyPDFDirectoryLoader("assets/docs")
docs = loader.load()

# Print the number of loaded documents
logging.info(
    f"number of loaded documents: {len(docs)}",
)

# Instantiate an HuggingFaceEmbeddings object with specified parameters
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",  # Name of the Sentence Transformers model
    # model_kwargs={"device": "cuda"}  # Additional keyword arguments for the model
)
logging.info(
    f"Finish load embedding model: {embeddings}",
)
# Instantiate a RecursiveCharacterTextSplitter object with specified parameters
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600, chunk_overlap=100
)

# Split documents into chunks using the RecursiveCharacterTextSplitter
all_splits = text_splitter.split_documents(docs)
# Create a Qdrant collection from the document splits

qdrant_collection = Qdrant.from_documents(
    all_splits,  # List of document splits
    embeddings,  # HuggingFaceEmbeddings object for generating embeddings
    location=":memory:",
    # path="./",
    # Location to store the collection (in memory)
    collection_name="all_documents",  # Name of the Qdrant collection
)
logging.info("Finish load qdrant_collections")

retriever = qdrant_collection.as_retriever()


def get_retriever():
    return retriever


def get_llm():
    return llm
