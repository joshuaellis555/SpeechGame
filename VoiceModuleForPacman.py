import speech_recognition as sr
print("asdf")
import Pacman
print("asdf")

UP=(0,-1)
DOWN=(0,1)
LEFT=(-1,0)
RIGHT=(1,0)

global R

def calibrateSpeach():
    global R
    #obtan audio from microphone
    with sr.Microphone() as source:
        R = sr.Recognizer()
        print("Calibrating...")
        R.adjust_for_ambient_noise(source,duration=5)
        print("Done Calibrating")
def updateSpeach():
    print('us')
    global R
    with sr.Microphone() as source:
        print('with')
        audio = R.listen(source,duration=1)
        #recognize speech using Sphinx
        print('audio')
        try:
            words = R.recognize_sphinx(audio)
            wordArray = words.split()
            if words:
                print(words)
            else:
                print('None')
            for word in wordArray:
                if word == "up":
                    PLAYER.setDirection(UP)
                elif word == "down":
                    PLAYER.setDirection(DOWN)
                elif word == "left":
                    PLAYER.setDirection(LEFT)
                elif word == "right":
                    PLAYER.setDirection(RIGHT)
            return()
            
        except sr.UnknownValueError:
            print("Could not understand you")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
        print('error')
    return()
