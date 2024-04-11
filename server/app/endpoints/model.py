#  pylint: disable=import-error
import asyncio
import subprocess
from typing import List, Optional

from app.db.database import session
from app.models.model import Model
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse

router = APIRouter()

class ModelResponse(BaseModel):
    id : str
    name : str
    parameters : str
    ram_size : Optional[str] = None
    model_size : str
    hugging_face_url : str
    is_downloaded : bool
    install_command : str

    class Config:
        orm_mode = True


@router.get('/models',response_model=List[ModelResponse])
def fetch_models():
    """_summary_

    Returns:
        _type_: _description_
    """

    models = session.query(Model).first()

    if models is None:
        model1 = Model(id=1,name = 'Gemini',parameters = '',ram_size = '',model_size = '',hugging_face_url = 'https://huggingface.co/describeai/gemini', is_downloaded = True,install_command = 'gemini')
        model2 = Model(id=2,name = 'Gpt',parameters = '',ram_size = '',model_size = '',hugging_face_url = 'https://huggingface.co/spaces/ysharma/ChatGPT4', is_downloaded = True,install_command = 'chatgpt')
        model3 = Model(id=3,name = 'Mistral',parameters = '7B',ram_size = '8GB',model_size = '4.1GB',hugging_face_url = 'https://huggingface.co/mistralai/Mistral-7B-v0.1', is_downloaded = True,install_command = 'ollama run mistral')
        model4 = Model(id=4,name = 'Llama 2',parameters = '7B',ram_size = '8GB',model_size = '3.8GB',hugging_face_url='https://huggingface.co/meta-llama/Llama-2-7b-chat-hf',is_downloaded =True,install_command = 'ollama run llama2')
        session.add(model1)
        session.add(model2)
        session.add(model3)
        session.add(model4)
        session.commit()
    
    
    models = session.query(Model).all()

    return models

@router.get("/modeldownload/{model_name}")
async def model_download(model_name: str):
    cmd = f"ollama run {model_name}"

    # Define an async generator to stream the output
    async def stream_command_output(process):
        while True:
            line = await process.stdout.readline()
            print(line.decode())
            if not line:
                break
            yield line.decode()

    # Start the subprocess
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    return StreamingResponse(stream_command_output(process), media_type="text/plain")




