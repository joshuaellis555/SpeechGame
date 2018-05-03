import speech_recognition as sr
print("asdf")
import Pacman
print("asdf")

UP=(0,-1)
DOWN=(0,1)
LEFT=(-1,0)
RIGHT=(1,0)

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
                PLAYER.setDirection(UP)
            elif word == "down":
                PLAYER.setDirection(DOWN)
            elif word == "left":
                PLAYER.setDirection(LEFT)
            elif word == "right":
                PLAYER.setDirection(RIGHT)
        
    except sr.UnknownValueError:
        print("Could not understand you")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
