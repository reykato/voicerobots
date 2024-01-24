import speech_recognition as sr

with sr.Microphone() as source:
    audio = sr.Recognizer().listen(source)

with open("microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())