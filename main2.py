# import sys
# import cv2
# import pyaudio
# import wave
# import speech_recognition as sr
# import pyttsx3
# from gtts import gTTS
# import os
# from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5 import uic
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import QTimer, QThread, pyqtSignal
# import model
# # Set parameters for recording
# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# RECORD_SECONDS = 5
# OUTPUT_FILENAME = "output.wav"
#
# class SpeechRecognitionThread(QThread):
#     recognized_text = pyqtSignal(str)  # Signal to send recognized text to the main UI
#
#     def __init__(self):
#         super().__init__()
#         self.recognizer = sr.Recognizer()
#
#     def run(self):
#         # Initialize PyAudio
#         p = pyaudio.PyAudio()
#         stream = p.open(format=FORMAT,
#                         channels=CHANNELS,
#                         rate=RATE,
#                         input=True,
#                         frames_per_buffer=CHUNK)
#
#         print("Listening...")
#         frames = []
#
#         # Record audio for a fixed duration
#         for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#             data = stream.read(CHUNK)
#             frames.append(data)
#
#         print("Listening finished.")
#
#         # Stop and close the stream
#         stream.stop_stream()
#         stream.close()
#         p.terminate()
#
#         # Save the recorded data as a .wav file
#         with wave.open(OUTPUT_FILENAME, 'wb') as wf:
#             wf.setnchannels(CHANNELS)
#             wf.setsampwidth(p.get_sample_size(FORMAT))
#             wf.setframerate(RATE)
#             wf.writeframes(b''.join(frames))
#
#         # Use the saved audio file for ASR
#         with sr.AudioFile(OUTPUT_FILENAME) as source:
#             audio = self.recognizer.record(source)
#
#         try:
#             # Recognize speech using Google's ASR
#             text = self.recognizer.recognize_google(audio)
#             print("Recognized Speech:", text)
#
#             # Process the recognized text with your model
#             output = model.start(text)
#             print("Model Output:", output)
#
#             # Emit the recognized and processed text
#             self.recognized_text.emit(output)
#         except sr.UnknownValueError:
#             print("Google ASR could not understand audio")
#             self.recognized_text.emit("Could not understand the audio")
#         except sr.RequestError as e:
#             print(f"Could not request results from Google ASR service; {e}")
#             self.recognized_text.emit(f"Could not request results from Google ASR service; {e}")
#
# class RobotFace(QMainWindow):
#     def __init__(self):
#         super(RobotFace, self).__init__()
#         uic.loadUi('front_end.ui', self)
#
#         # Initialize TTS engine
#         self.tts_engine = pyttsx3.init()
#
#         # Load the video
#         self.cap = cv2.VideoCapture('effects/green_eye.mp4')
#
#         # Timer to update the label with the next frame
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(30)  # Adjust the interval based on the video FPS
#
#         # Speech recognition thread
#         self.speech_thread = SpeechRecognitionThread()
#         self.speech_thread.recognized_text.connect(self.handle_speech)
#         self.speech_thread.start()
#
#     def update_frame(self):
#         ret, frame = self.cap.read()
#         if ret:
#             # Resize the frame to fit the QLabel's dimensions
#             label_width = self.face_lbl.width()
#             label_height = self.face_lbl.height()
#             resized_frame = cv2.resize(frame, (label_width, label_height), interpolation=cv2.INTER_AREA)
#
#             # Convert the frame to RGB format
#             rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
#
#             # Get the frame size and convert to QImage
#             h, w, ch = rgb_frame.shape
#             bytes_per_line = ch * w
#             qimg = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
#
#             # Set the QPixmap from QImage and display it on the label
#             self.face_lbl.setPixmap(QPixmap.fromImage(qimg))
#         else:
#             # If the video ended, restart it
#             self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#
#     def handle_speech(self, text):
#         # Respond based on recognized speech
#         if "exit" in text.lower():
#             self.speak("Goodbye!")
#             sys.exit(0)
#         else:
#             self.speak(text)  # Speak the recognized output from the model
#
#     def speak(self, text):
#         # Text-to-Speech response using gTTS
#         tts = gTTS(text=text, lang='en')
#         tts.save("response.mp3")
#         os.system("mpg123 response.mp3")  # Use an appropriate player for your OS
#         print(f"Robot says: {text}")
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = RobotFace()
#     window.show()
#     sys.exit(app.exec_())



import sys
import cv2
import pyaudio
import wave
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import model

# Set parameters for recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILENAME = "output.wav"
wake_word = "hey mister bot"
class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)  # Signal to send recognized text to the main UI

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()

    def run(self):
        self.start_recording()

    def start_recording(self):
        os.system("mpg123 audios/ok.mp3")
        # Initialize PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Listening...")
        frames = []

        # Record audio for a fixed duration
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Listening finished.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded data as a .wav file
        with wave.open(OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        # Use the saved audio file for ASR
        with sr.AudioFile(OUTPUT_FILENAME) as source:
            audio = self.recognizer.record(source)

        try:
            # Recognize speech using Google's ASR
            text = self.recognizer.recognize_google(audio)
            print("Recognized Speech:", text)

            # Emit the recognized text to the UI
            self.recognized_text.emit(text)

        except sr.UnknownValueError:
            print("Google ASR could not understand audio")
            pass
            self.recognized_text.emit("my version is 1.1.0")
        except sr.RequestError as e:
            print(f"Could not request results from Google ASR service; {e}")
            pass
            self.recognized_text.emit(f"Could not request results from Google ASR service; {e}")

class TextToSpeechThread(QThread):
    tts_finished = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        self.speak_text(self.text)

    def speak_text(self, text):
        # Text-to-Speech response using gTTS
        tts = gTTS(text=text, lang='en')
        tts.save("audios/response.mp3")
        os.system("mpg123 audios/response.mp3")  # Use an appropriate player for your OS
        print(f"Robot says: {text}")

        # Emit a signal when TTS finishes playing
        self.tts_finished.emit()


class RobotFace(QMainWindow):
    def __init__(self):
        super(RobotFace, self).__init__()
        uic.loadUi('front_end.ui', self)

        # Load the video
        self.cap = cv2.VideoCapture('effects/green_eye.mp4')

        # Timer to update the label with the next frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Adjust the interval based on the video FPS

        # Speech recognition thread
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognized_text.connect(self.handle_speech)

        # Start the initial recording
        self.speech_thread.start()
        self.speak("hello, I am Mister Bot how may i help you")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Resize the frame to fit the QLabel's dimensions
            label_width = self.face_lbl.width()
            label_height = self.face_lbl.height()
            resized_frame = cv2.resize(frame, (label_width, label_height), interpolation=cv2.INTER_AREA)

            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

            # Get the frame size and convert to QImage
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Set the QPixmap from QImage and display it on the label
            self.face_lbl.setPixmap(QPixmap.fromImage(qimg))
        else:
            # If the video ended, restart it
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def handle_speech(self, text):
        # Respond based on recognized speech
        if "exit" in text.lower():
            self.speak("Goodbye")
            sys.exit(0)
        if "my version is 1.1.0" in text.lower():
            print("testing   ", text)
            print("not good audio for me")
            self.speak("yup")

        else:
            print("########################  ",text)
            # Speak the recognized text or output from model
            output = model.distilgpt2_model(text)  # Assuming model.start generates the chatbot response
            self.speak(output)

    def speak(self, text):
        # Start the TTS thread
        self.tts_thread = TextToSpeechThread(text)
        self.tts_thread.tts_finished.connect(self.start_next_recording)
        self.tts_thread.start()

    def start_next_recording(self):
        # Restart the speech recognition after the TTS finishes
        print("Starting next recording...")
        self.speech_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotFace()
    window.show()
    sys.exit(app.exec_())