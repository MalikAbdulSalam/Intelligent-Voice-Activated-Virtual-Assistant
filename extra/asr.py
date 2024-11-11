import pyaudio
import wave
import speech_recognition as sr
from gtts import gTTS
import os

from tts import speak_text

# Set parameters for recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Listening")

# Store the frames
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("listening finished")

# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()

# Save the recorded data as a .wav file
wf = wave.open(OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"Audio saved to {OUTPUT_FILENAME}")

# Initialize the recognizer
recognizer = sr.Recognizer()

# Use the saved audio file for ASR
with sr.AudioFile(OUTPUT_FILENAME) as source:
    audio = recognizer.record(source)

try:
    # Recognize the speech using Google's ASR (you can use others as well)
    text = recognizer.recognize_google(audio)
    print("Recognized Speech:", text)
    speak_text(text)
except sr.UnknownValueError:
    print("Google ASR could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google ASR service; {e}")


def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")  # Use an appropriate player for your OS