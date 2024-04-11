import base64
import os
import re

from app.db.database import session
from app.models.datasource import DataSource, DataSourceType, UserDataSource
from app.models.github_reader import GitHubDataLoader
from app.models.slackReader import SlackReader
from app.utils.secure_token import decrypt_data
from llama_index.embeddings.google import GooglePaLMEmbedding
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from llama_index.core import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.milvus import MilvusVectorStore
from pymilvus import MilvusClient

router = APIRouter()

@router.get("/fetch-data")
def fetch_data(user_id: str):
    """_summary_

    Args:
        user_id (str): _description_

    Returns:
        _type_: _description_
    """
    client = MilvusClient(uri = os.getenv('URI'), token = os.getenv("MILVUS_TOKEN"))
    client.drop_collection(
    collection_name= "integrations"
    )
    user_data_sources = session.query(UserDataSource).filter_by(user_id = user_id).all()
    # print(f"{user_data_sources=}", type(user_data_sources))
    for user_data_source in user_data_sources:
        # print(f"{user_data_source.data_source.type=}")
        if user_data_source.data_source.type ==DataSourceType.slack:
            # print(f"{user_data_source.credentials=}")
            upload_slack_data(decrypt_data(base64.b64decode(user_data_source.credentials)), collection_name="integrations")
        elif user_data_source.data_source.type == DataSourceType.github:
            upload_github_data(decrypt_data(base64.b64decode(user_data_source.credentials)), collection_name="integrations")


    return JSONResponse(status_code=200, content="Data Pulled Successfully.")


def upload_slack_data(token, collection_name):
    """_summary_

    Args:
        token (_type_): _description_
        collection_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    documents = SlackReader(slack_token=token).load_data()
    collection_name = re.sub(r'[^a-zA-Z0-9]', '', collection_name)
    vector_store = MilvusVectorStore(uri = os.getenv('URI'),token = os.getenv("MILVUS_TOKEN"),collection_name = collection_name, dim= int(os.getenv("EMBEDDING_DIMENSION")))
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # llm = Ollama(model='mixtral', request_timeout=100)
    embed_model = GooglePaLMEmbedding(model_name= "models/embedding-gecko-001", api_key= os.getenv("GEMINI_API_KEY"))
    service_context = ServiceContext.from_defaults(embed_model= embed_model)
    index = VectorStoreIndex.from_vector_store(vector_store,storage_context=storage_context, service_context=service_context)
    # query_engine = index.as_query_engine(streaming=True,service_context=service_context, similarity_top_k=1)

    node_parser = SentenceSplitter(chunk_size=1024)
    base_nodes = node_parser.get_nodes_from_documents(documents)
    print("node info", len(base_nodes), type(base_nodes))
    index.insert_nodes(base_nodes)
    # print(query_engine.get_prompts())
    # print(documents)

    return documents

def upload_github_data(token,collection_name):
    """_summary_

    Args:
        token (_type_): _description_
        collection_name (_type_): _description_
    """
    documents = GitHubDataLoader(token=token).load_data()
    collection_name = re.sub(r'[^a-zA-Z0-9]', '', collection_name)
    vector_store = MilvusVectorStore(uri = os.getenv('URI'),token = os.getenv("MILVUS_TOKEN"),collection_name = collection_name, dim= int(os.getenv("EMBEDDING_DIMENSION")))
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # llm = Ollama(model='mixtral', request_timeout=100)
    embed_model = GooglePaLMEmbedding(model_name= "models/embedding-gecko-001", api_key= os.getenv("GEMINI_API_KEY"))
    service_context = ServiceContext.from_defaults(embed_model= embed_model)
    index = VectorStoreIndex.from_vector_store(vector_store,storage_context=storage_context, service_context=service_context)
    # query_engine = index.as_query_engine(streaming=True,service_context=service_context, similarity_top_k=1)

    node_parser = SentenceSplitter(chunk_size=1024)
    base_nodes = node_parser.get_nodes_from_documents(documents)

    index.insert_nodes(base_nodes)
    # print(query_engine.get_prompts())
    # print(documents)

    return documents

    






   



