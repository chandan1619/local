
import logging
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException
from llama_index.core import (
    ServiceContext,
    StorageContext,
    VectorStoreIndex,
    download_loader,
)
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.embeddings.google import GooglePaLMEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.milvus import MilvusVectorStore
from pymilvus import connections

load_dotenv()
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# connections.connect(alias="default", host=os.getenv("MILVUS_HOST"), port=os.getenv("MILVUS_PORT"),)
connections.connect(alias="default", uri = os.getenv('URI'), token = os.getenv("MILVUS_TOKEN"))


embedding_dim = int(os.getenv("EMBEDDING_DIMENSION"))

def llm_model(model_name):
    """_summary_

    Args:
        model_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    if model_name == "gemini":
        return Gemini(api_key= os.getenv("GEMINI_API_KEY"))
    elif model_name == "chatgpt":
        return OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
    else:
        return Ollama(model = model_name,request_timeout=100)



def upload_embeddind(pdf_file_path, collection_name):
    """_summary_

    Args:
        pdf_file_path (_type_): _description_
        collection_name (_type_): _description_

    Returns:
        _type_: _description_
    """

    try:
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(file=Path(pdf_file_path))
        collection_name = re.sub(r'[^a-zA-Z0-9]', '', collection_name)
        vector_store = MilvusVectorStore(uri = os.getenv('URI'),token = os.getenv("MILVUS_TOKEN"),collection_name = collection_name, dim= int(os.getenv("EMBEDDING_DIMENSION")))

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        embed_model = GooglePaLMEmbedding(model_name= "models/embedding-gecko-001", api_key= os.getenv("GEMINI_API_KEY"))

        service_context = ServiceContext.from_defaults(embed_model= embed_model)

        # create the sentence window node parser w/ default settings
        node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text",
        )

        nodes = node_parser.get_nodes_from_documents(documents)
        index = VectorStoreIndex(
        nodes,
        storage_context = storage_context,
        service_context= service_context
        )

    
    
        chunk_ids = []
        for _, node in enumerate(nodes):
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
    llm = llm_model(model_name)
    embed_model = GooglePaLMEmbedding(model_name= "models/embedding-gecko-001", api_key= os.getenv("GEMINI_API_KEY"))
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    index = VectorStoreIndex.from_vector_store(vector_store,service_context=service_context, storage_context=storage_context)

    

    # The target key defaults to `window` to match the node_parser's default
    postproc = MetadataReplacementPostProcessor(
        target_metadata_key="window"
    )
    query_engine = index.as_query_engine(streaming=True,service_context=service_context,node_postprocessors = [postproc],
    alpha=0.5, similarity_top_k=10)

    # print(query_engine.get_prompts())
    return query_engine




