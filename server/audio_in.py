import speech_recognition as sr

recognizer = sr.Recognizer()


def take_audio_input():
    """_summary_
    """
    
    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source)

        try:
            # Listen for speech and convert it to text
            audio = recognizer.listen(source)

            # Recognize the speech using the Google Web Speech API
            text = recognizer.recognize_google(audio)

            if not text.strip():
                print("No valid input received.")
                return
            
            return text

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as exe:
            print(f"Error with the service; {exe}")
