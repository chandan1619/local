
import logging
import os
import re
from pathlib import Path

from app.models.slackReader import SlackReader
from dotenv import load_dotenv
from fastapi import HTTPException
from llama_index.core import (
    ServiceContext,
    StorageContext,
    SummaryIndex,
    VectorStoreIndex,
    download_loader,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.readers.jira import JiraReader
from llama_index.vector_stores.milvus import MilvusVectorStore
from pymilvus import connections

load_dotenv()
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# connections.connect(alias="default", host=os.getenv("MILVUS_HOST"), port=os.getenv("MILVUS_PORT"),)
connections.connect(alias="default", uri = os.getenv('URI'), token = os.getenv("MILVUS_TOKEN"))


embedding_dim = int(os.getenv("EMBEDDING_DIMENSION"))


def upload_embeddind(pdf_file_path, collection_name):
    """_summary_

    Args:
        pdf_file_path (_type_): _description_
        collection_name (_type_): _description_

    Returns:
        _type_: _description_
    """

    try:
        collection_name = re.sub(r'[^a-zA-Z0-9]', '', collection_name)
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(file=Path(pdf_file_path))
        vector_store = MilvusVectorStore(uri =os.getenv('URI'),token = os.getenv("MILVUS_TOKEN"), collection_name = collection_name, dim=embedding_dim)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        llm = Ollama(model="mistral", request_timeout=300)
        service_context = ServiceContext.from_defaults(llm=llm, embed_model="local")
        node_parser = SentenceSplitter(chunk_size=1024)
        base_nodes = node_parser.get_nodes_from_documents(documents)
        index = VectorStoreIndex(base_nodes,
                                            service_context=service_context, storage_context=storage_context)


        chunk_ids = []
        for _, node in enumerate(base_nodes):
            chunk_ids.append(node.id_)
        

        return chunk_ids

    except Exception as e:
        # Log the exception with a custom message
        print(e)
        logging.error(f"Failed to upload embedding for {pdf_file_path} to collection {collection_name}: {e}", exc_info=True)
        # Optionally, re-raise the exception to handle it further up the call stack
        raise HTTPException(status_code=500, detail="Failed to process embedding.") from e


def return_query_engine(collection_name, model_name):
    """_summary_

    Args:
        collection_name (_type_): _description_
    """
    
    collection_name = re.sub(r'[^a-zA-Z0-9]', '', collection_name)
    vector_store = MilvusVectorStore(uri = os.getenv('URI'),token = os.getenv("MILVUS_TOKEN"),collection_name = collection_name, dim=embedding_dim)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    llm = Ollama(model=model_name, request_timeout=100)
    service_context = ServiceContext.from_defaults(llm=llm, embed_model="local")
    index = VectorStoreIndex.from_vector_store(vector_store,service_context=service_context, storage_context=storage_context)
    query_engine = index.as_query_engine(streaming=True,service_context=service_context, similarity_top_k=1)

    # print(query_engine.get_prompts())
    return query_engine



