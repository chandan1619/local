import io

import pygame
from gtts import gTTS


async def process_sentence(sentence):
    """_summary_

    Args:
        sentence (_type_): _description_
    """
    tts = gTTS(str(sentence))
    with io.BytesIO() as f:
        tts.write_to_fp(f)
        f.seek(0)

        pygame.mixer.init()
        sound = pygame.mixer.Sound(f)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)