import speech_recognition as sr

print(sr.__version__)

r = sr.Recognizer()

# obtain audio fromthe microphone
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Say the move!")
    audio = r.listen(source)

    #r.recognize_sphinx(audio,language="chess-EN", grammar="chess.gram")# return a result of recognition

# 使用CMU Sphinx引擎去识别音频
try:
    print("Sphinx thinks you said: " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

# write audio to a WAV file
with open("C:\WorkBench\Python\microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())    

print('Ok')
