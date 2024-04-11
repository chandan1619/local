# pylint: disable=import-error
import re

from app.db.database import session
from app.models.llm import return_query_engine
from app.models.model import Model
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/stream")
async def stream_data(q: str, project_id : str , model_id : str):
    """_summary_

    Args:
        q (str): _description_
    """
    
    model = session.query(Model).filter_by(id = model_id.strip()).first()
    
    model_name = model.install_command.split(" ")[-1]

    project_name : str = ""
    if project_id == "integrations":
        project_name = project_id
    else:
        project_name = f"project{project_id}"

    

    def generate_data(query):
    
        try:
            sentence_buffer = ''
            
            query_engine = return_query_engine(project_name,model_name)

            response = query_engine.query(query)


            for chunk in response.response_gen:
                sentence_buffer += chunk
                sentences = re.split(r'(?<=[.!?])\s+', sentence_buffer)
                sentence_buffer = sentences.pop() if sentences else ''
                for sentence in sentences:
                    if sentence:
                        print(sentence)
                        yield sentence
            print(sentence_buffer)
            yield sentence_buffer
        
        except Exception as exc:
            print(exc)
    return StreamingResponse(generate_data(q), media_type="text/event-stream")


@router.get("/streamc")
async def stream_datac(q: str, project_id : str , model_id : str):
    """_summary_

    Args:
        q (str): _description_
    """
    model = session.query(Model).filter_by(id = model_id.strip()).first()
    
    model_name = model.install_command.split(" ")[-1]
    
    def generate_data(query):
    
        try:
        
            query_engine = return_query_engine(f"project{project_id}", model_name=model_name)

            response = query_engine.query(query)

            for chunk in response.response_gen:
                yield chunk
           
        
        except Exception as exc:
            print(exc)
    return StreamingResponse(generate_data(q), media_type="text/event-stream")