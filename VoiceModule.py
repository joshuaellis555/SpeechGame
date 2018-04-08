import speech_recognition as sr
import Snake

cont = True
#obtan audio from microphone
r = sr.Recognizer()
print("Calibrating...")
r.adjust_for_ambient_noise(sr.Microphone,duration=5)
while(cont):
    audio = r.listen(sr.Microphone)
#recognize speech using Sphinx
    try:
        
        words = r.recognize_sphinx(audio)
        wordArray = words.split()
        for word in wordArray:
            if word == "up":
                Snake.setDirection("up")
            elif word == "down":
                Snake.setDirection("down")
            elif word == "left":
                Snake.setDirection("left")
            elif word == "right":
                Snake.setDirection("right")
        
    except sr.UnknownValueError:
        print("Could not understand you")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
