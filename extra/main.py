import sys
import cv2
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal

class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)  # Signal to send recognized text to the main UI

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index=YOUR_MIC_INDEX)  # Set your mic index here

    def run(self):
        while True:
            with self.mic as source:
                print("Listening...")
                audio = self.recognizer.listen(source)
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"Recognized: {text}")
                    self.recognized_text.emit(text)  # Emit the recognized text
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                except sr.RequestError:
                    print("Speech Recognition service error")
# Thread class for handling speech recognition asynchronously
class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)  # Signal to send recognized text to the main UI

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def run(self):
        while True:
            with self.mic as source:
                print("Listening...")
                audio = self.recognizer.listen(source)

                try:
                    # Recognize speech using Google API
                    text = self.recognizer.recognize_google(audio)
                    print(f"Recognized: {text}")
                    self.recognized_text.emit(text)  # Emit the recognized text
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                except sr.RequestError:
                    print("Speech Recognition service error")


# Main class for the Robot face and interaction
class RobotFace(QMainWindow):
    def __init__(self):
        super(RobotFace, self).__init__()
        uic.loadUi('front_end.ui', self)

        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()

        # Load the video
        self.cap = cv2.VideoCapture('effects/green_eye.mp4')

        # Timer to update the label with the next frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Adjust the interval based on the video FPS

        # Speech recognition thread
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognized_text.connect(self.handle_speech)
        self.speech_thread.start()

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
            self.speak("Goodbye!")
            sys.exit(0)
        else:
            response = f"You said: {text}"
            self.speak(response)

    def speak(self, text):
        # Text-to-Speech response
        print(f"Robot says: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotFace()
    window.show()
    sys.exit(app.exec_())
