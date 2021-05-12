import speech_recognition as sr

print(sr.__version__)

r = sr.Recognizer()

# obtain audio fromthe microphone
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Say the move!")
    audio = r.listen(source)

    #r.recognize_sphinx(audio,language="chess-EN", grammar="chess.gram")# return a result of recognition
    r.recognize_sphinx(audio)

# write audio to a WAV file
with open("microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())    

print('Ok')
