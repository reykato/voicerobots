import speech_recognition as sr
import whisper
import pyttsx3
import os

with sr.Microphone() as source:
    print("Listening:")
    audio = sr.Recognizer().listen(source)

with open("app/src/results.wav", "wb") as f:
    f.write(audio.get_wav_data())

model = whisper.load_model("tiny.en")
result = model.transcribe("app/src/results.wav", fp16 = False)
print(result["text"])

engine = pyttsx3.init()
engine.say(result["text"])
engine.runAndWait()

os.remove("app/src/results.wav")
