from gtts import gTTS
import os

def speak_text(response_text):
    tts = gTTS(text=response_text, lang='en')
    tts.save("start.mp3")
    os.system("mpg123 start.mp3")  # Use an appropriate player for your OS

# Example usage
response_text = "ok"
speak_text(response_text)


