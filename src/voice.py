import pyttsx3
import speech_recognition as sr
from src.queueSpeak import QueueSpeak
import time

engine = pyttsx3.init()

class Voice:
    def __init__(self, configs, sysGlobals, queueSpeak:QueueSpeak) -> None:
        self.sysGlobals = sysGlobals
        self.configs = configs
        self.queueSpeak = queueSpeak
        self.rec = sr.Recognizer()

        for voice in engine.getProperty('voices'):
            if "portuguese" in voice.languages:
                self.setVoice(voice)
                break

    def start(self) -> None:
        self.queueSpeak.queue.put(f"Olá, meu nome é {self.configs.NAME}.")

        while True:
            time.sleep(0.8)

            try:
                data = self.queueSpeak.queue.get()
            except Exception:
                pass
            else:
                self.speak_text(data)
                
    def setVoice(voice):
        engine.setProperty('voice', voice)
        print("Voz em português definida!")

    def speak_text(self, text) -> None:
        if text:
            self.sysGlobals["isSpeaking"].set()
            engine.say(text)
            engine.runAndWait()
            self.sysGlobals["isSpeaking"].clear()