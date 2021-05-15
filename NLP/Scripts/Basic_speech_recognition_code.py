************https://www.tutorialspoint.com/artificial_intelligence_with_python/artificial_intelligence_with_python_speech_recognition.htm
We need to install the following packages for this −
Pyaudio − It can be installed by using pip install Pyaudio command. (should download Pyaudio.whl file to install Pyaudio package if python versions>3.6)
SpeechRecognition − This package can be installed by using pip install SpeechRecognition.
Google-Speech-API − It can be installed by using the command pip install google-api-python-client.***********


#Code
import speech_recognition as sr
recording = sr.Recognizer()

with sr.Microphone() as source: 
    recording.adjust_for_ambient_noise(source)
    print("Please Say something:")
    audio = recording.listen(source)
   
try:
   print("You said: \n" + recording.recognize_google(audio))
except Exception as e:
   print(e)
