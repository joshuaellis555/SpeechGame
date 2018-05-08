import threading
import random
import os.path
from tkinter import *
import time
import speech_recognition as sr


WIDTH = 28
HEIGHT = 31
TILESIZE=20

UP=(0,-1)
DOWN=(0,1)
LEFT=(-1,0)
RIGHT=(1,0)
DEAD=(0,0)

BLANK='blank'
DOT='dot'
PP='pp'
PACMAN='pacman'
WALL='wall'
GATE='gate'
GHOST='ghost'

#initialize the board with nothing
BOARD=[[None for y in range(HEIGHT)] for x in range(WIDTH)]

global CANVAS

global PLAYER
PLAYER=0

global POWER
POWER=0

global RUNNING
RUNNING=False

def rectangle(x,y,color,outline):#Generates a tkinter rectangle on the canvas
    return CANVAS.create_rectangle(
        TILESIZE*x, TILESIZE*y, TILESIZE*(x+1)-1, TILESIZE*(y+1)-1, outline=outline, fill=color)

class Tile():#Template
    def __init__(self,x,y,color,tileType,outline='#000',blocks=False):
        self.x=x%WIDTH
        self.y=y%HEIGHT
        self.color=color
        self.outline=outline
        self.rect=rectangle(x,y,color,outline)
        
        self.tileType=tileType
        self.blocks=blocks

    def remove(self):
        CANVAS.delete(self.rect)

    def replace(self,x=None,y=None,color=None,outline=None):
        x=x if x!=None else self.x
        y=y if y!=None else self.y
        color=color if color!=None else self.color
        outline=outline if outline!=None else self.outline
        Tile.__init__(self,x,y,color,self.tileType,outline=outline)

    def _move(self,x,y):
        self.x=x
        self.y=y
        self.remove()
        self.replace()

        
############Types of Tiles#################
class Blank(Tile):
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#000',BLANK,outline='#333')

class Dot(Tile):
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#eee',DOT)

class Gate(Tile):
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#666',GATE, outline='#00a')

class Pp(Tile):
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#fc5',PP,outline='#f00')

class Wall(Tile):
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#00f',WALL,outline='#33f',blocks=True)

############# Player ##########################
class Pacman(Tile):#The player
    """The player is also a tile in the GRID"""
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#ff0',PACMAN)
        
        self.direction=LEFT
        self.nextDirection=self.direction
        
        self.consumed=Blank(x,y)
        self.consumed.remove()

    def _consume(self,tile):
        if tile.tileType == BLANK or tile.tileType == PP or tile.tileType == DOT:
            if tile.tileType == PP:
                global POWER
                POWER=40
            r=self.consumed
            self.consumed=tile
            r=Blank(r.x,r.y)
            return r
        elif tile.tileType == GHOST:
            if POWER>0:
                tile.kill()
                BOARD[tile.x][tile.y]=Blank(tile.x,tile.y)
            else:
                self.kill()
        else:
            return None
        
    def move(self,direction=None):
        if self.direction==DEAD:
            return
        if self.direction!=self.nextDirection:
            self.setDirection(self.nextDirection)
        direction = direction if direction else self.direction
        x=(self.x+direction[0])%WIDTH
        y=(self.y+direction[1])%HEIGHT
        
        self.direction=direction
        target=BOARD[x][y]
        poo=self._consume(target)
        if poo:
            ox,oy=self.x,self.y
            
            poo.replace()
            target.remove()
            
            self._move(x,y)
            BOARD[x][y]=self
            BOARD[ox][oy]=poo

    def setDirection(self,newDirection):
        global RUNNING
        RUNNING=True
        if self.direction==DEAD:
            return
        x=(self.x+newDirection[0])%WIDTH
        y=(self.y+newDirection[1])%HEIGHT
        if not BOARD[x][y].blocks:
            self.direction = newDirection
            self.nextDirection=self.direction
        else:
            self.nextDirection=newDirection

    def kill(self):
        print(self.tileType,"is dead!!!")
        self.remove()
        BOARD[self.x][self.y]=self.consumed.replace(self.x,self.y)
        self.direction=DEAD

################ Ghosts ###############
class Ghost(Pacman):
    """The player is also a tile in the GRID"""
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#f0f',GHOST,blocks=True)
        
        self.direction=LEFT
        self.nextDirection=self.direction
        
        self.consumed=Blank(x,y)
        self.consumed.remove()
        self.vulnerable=False

    def _consume(self,tile):
        if not tile.blocks and tile.tileType!=GHOST:
            r=self.consumed
            self.consumed=tile
            if self.consumed.tileType==PACMAN:
                global POWER
                if POWER>0:
                    self.kill()
                else:
                    self.consumed.kill()
                    self.consumed=Blank(self.x,self.y)
            return r
        else:
            self.direction=(-1*self.direction[0],-1*self.direction[1])
            return None
    def move(self):
        self.nextDirection=self.direction
        super().move()
        
    def setDirection(self):
        if self.direction==DEAD:
            return

        directions=[UP,DOWN,LEFT,RIGHT]
        
        random.shuffle(directions)
        for d in directions:
            oppositeSD=(-1*self.direction[0],-1*self.direction[1])
            if d != oppositeSD:
                x=(self.x+d[0])%WIDTH
                y=(self.y+d[1])%HEIGHT
                if not BOARD[x][y].blocks:
                    self.direction = d

    def makeVulnerable(self,vulnerable):
        if vulnerable and not self.vulnerable and not self.direction==DEAD:
            self.remove()
            self.replace(color='#77f',outline='#f0f')
        if not vulnerable and self.vulnerable and not self.direction==DEAD:
            self.remove()
            self.replace(color='#f0f',outline='#000')
        self.vulnerable=vulnerable

#########################  Voice  ###############################
class Voice():
    def __init__(self):
        with sr.Microphone() as source:
            self.recognizer = sr.Recognizer()
            print("Calibrating...")
            self.recognizer.adjust_for_ambient_noise(source,duration=5)
            print("Done Calibrating")

    def updateSpeech(self):
        while True:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, phrase_time_limit = 2)
                #recognize speech using Sphinx
                try:
                    words = self.recognizer.recognize_sphinx(audio)
                    wordArray = words.split()
                    print("words--->",words)
                    global PLAYER
                    for word in wordArray:
                        if word == "two" or word == "no":
                            print("up")
                            PLAYER.setDirection(UP)
                        elif word == "four" or word == "full":
                            print("down")
                            PLAYER.setDirection(DOWN)
                        elif word == "one" or word == "want":
                            print("left")
                            PLAYER.setDirection(LEFT)
                        elif word == "right":
                            print("right")
                            PLAYER.setDirection(RIGHT)
                    
                except:
                    print('error')

#########################  Game  ###############################
class Game(Frame):

    def __init__(self):

        self.voice=Voice()
        
        Frame.__init__(self)
        #Set up the main window frame as a grid
        self.master.title("Pacman")
        self.grid()

        #Set up main frame for game as a grid
        frame1 = Frame(self)
        frame1.grid()

        #Add a canvas to frame1 as self.canvas member 
        self.canvas = Canvas(frame1, width = WIDTH*TILESIZE, height = HEIGHT*TILESIZE, bg ="black")
        global CANVAS
        CANVAS = self.canvas
        
        self.canvas.grid(columnspan = 3)
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.input)
        self.canvas.bind("<Key>", self.input)

        self.new_game()

    def new_game(self):
        self.canvas.delete(ALL)

        self.enemies=[]
        
        f=open("Grid.txt","r")
        lines=f.readlines()
        y=0
        for line in lines:
            x=0
            for char in line:
                if char=='B':
                    BOARD[x][y]=Blank(x,y)
                if char=='O':
                    BOARD[x][y]=Dot(x,y)
                if char=='P':
                    BOARD[x][y]=Pp(x,y)
                if char=='C':
                    global PLAYER
                    PLAYER=Pacman(x,y)
                    BOARD[x][y]=PLAYER
                if char=='X':
                    BOARD[x][y]=Wall(x,y)
                if char=='H':
                    BOARD[x][y]=Gate(x,y)
                if char=='G':
                    BOARD[x][y]=Ghost(x,y)
                    self.enemies+=[BOARD[x][y]]
                x+=1
            y+=1

        self.player=PLAYER

        self.play()
        
    def play(self):#Main play loop
        print("play")
        global POWER
        global RUNNING
        interval=.4
        start=time.time()
        threading.Thread(target=self.voice.updateSpeech).start()
        while True:
            if start+interval>time.time():
                self.update()
                continue
            
            
            
            start=time.time()

            if not RUNNING:
                continue

            if POWER<0 or not POWER%2:
                for enemy in self.enemies:
                    enemy.setDirection()
                    enemy.move()
                    if POWER==40:
                        enemy.makeVulnerable(True)
                    if POWER==0:
                        enemy.makeVulnerable(False)

            POWER-=1
            
            self.player.move()
            
            self.update()

    def input(self,event):
        global PLAYER
        if event.keycode == 38:
            PLAYER.setDirection(UP)
        elif event.keycode == 39:
            PLAYER.setDirection(RIGHT)
        elif event.keycode == 40:
            PLAYER.setDirection(DOWN)
        elif event.keycode == 37:
            PLAYER.setDirection(LEFT)

Game().mainLoop()
