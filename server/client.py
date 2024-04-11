import asyncio
import random

import httpx
from audio_in import take_audio_input
from audio_out import process_sentence


async def consume_stream(query):
    """_summary_

    Args:
        query (_type_): _description_
    """
    qr = random.randint(0,10000)
    url = f'http://127.0.0.1:8000/chat/stream?q={query}&project_id="32b25702-5ea0-4a8f-929f-f0dc27795959&"&qr = {qr}'

    with httpx.stream('GET', url, timeout=200) as r:
        for chunk in r.iter_raw():
            print(chunk.decode('utf-8'))
            await process_sentence(chunk.decode('utf-8'))


while True:
    query = input("Query ...")
    # query = take_audio_input()
    # print(query)

    if not query:
        continue

    asyncio.run(consume_stream(query))
