import speech_recognition as sr
#import keyboard
#import Pacman


#obtan audio from microphone
r = sr.Recognizer()
print("Calibrating...")
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source,duration=5)
print("Done Calibrating")
while True:
        if keyboard.is_pressed('l'):
            with sr.Microphone() as source:
                print("listing")
                audio = r.listen(source, phrase_time_limit = 1)
                print("we heard you")
            #recognize speech using Sphinx
            try:       
                words = r.recognize_sphinx(audio)
                print(words)
                if "left" in words:
                    PLAYER.setDirection(LEFT)
                elif "right" in words:
                    PLAYER.setDirection(RIGHT)
                elif "jump" in words:
                    PLAYER.setDirection(UP)
                elif "down" in words:
                    PLAYER.setDirection(DOWN)
                else:
                    print("done")
                    pass
        ##        wordArray = words.split()        
        ##        for word in wordArray:
        ##            if word == "up":
        ##                #Snake.setDirection("up")
        ##                print("up")
        ##            elif word == "down":
        ##                #Snake.setDirection("down")
        ##                print("down")
        ##            elif word == "left":
        ##                #Snake.setDirection("left")
        ##                print("left")
        ##            elif word == "right":
        ##                #Snake.setDirection("right")
        ##                print("right")
                
            except sr.UnknownValueError:
                print("Could not understand you")
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))

