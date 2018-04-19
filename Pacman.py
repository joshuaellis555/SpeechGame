import threading
import random
import os.path
from tkinter import *
import time

WIDTH = 28
HEIGHT = 31
TILESIZE=20

UP=(0,-1)
DOWN=(0,1)
LEFT=(-1,0)
RIGHT=(1,0)

BLANK='blank'
DOT='dot'
POWER='power'
PACMAN='pacman'
WALL='wall'

#initialize the board with nothing
BOARD=[[None for y in range(HEIGHT)] for x in range(WIDTH)]

global CANVAS

PLAYER=None

def rectangle(x,y,color,outline):#Generates a tkinter rectangle on the canvas
    return CANVAS.create_rectangle(
        TILESIZE*x, TILESIZE*y, TILESIZE*(x+1)-1, TILESIZE*(y+1)-1, outline=outline, fill=color)

class Tile():#Template
    def __init__(self,x,y,color,tileType,outline='#000',block=False):
        self.x=x%WIDTH
        self.y=y%HEIGHT
        self.color=color
        self.outline=outline
        self.rect=rectangle(x,y,color,outline)
        
        self.tileType=tileType
        self.block=block

    def X(self):
        return self.x

    def Y(self):
        return self.y

    def remove(self):
        CANVAS.delete(self.rect)

    def replace(self):
        Tile.__init__(self,self.x,self.y,self.color,self.tileType)

    def removeReplace(self,x,y):
        self.x=x
        self.y=y
        self.remove()
        self.replace()

    def type(self):
        return self.tileType

    def blocks(self):
        return self.block
        
############Types of Tiles#################
class Blank(Tile):
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#000',BLANK,outline='#333')

class Dot(Tile):
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#fff',DOT)

class Power(Tile):
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#fc5',POWER,outline='#f00')

class Wall(Tile):
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#00f',WALL,outline='#33f',block=True)

class Pacman(Tile):#The player
    """The player is also a tile in the GRID"""
    def __init__(self,x,y):
        Tile.__init__(self,x, y,'#ff0',PACMAN)
        
        self.direction=LEFT
        
        self.consumed=Blank(x,y)
        self.consumed.remove()

    def _consume(self,tile):
        if tile.type() == BLANK or tile.type() == POWER or tile.type() == DOT:
            r=self.consumed
            self.consumed=tile
            r=Blank(r.X(),r.Y())
            return r
        else:
            return None
        
    def move(self,direction=None):
        direction = direction if direction else self.direction
        x=self.X()+direction[0]
        y=self.Y()+direction[1]
        
        self.direction=direction
        target=BOARD[x][y]
        poo=self._consume(target)
        if poo:
            ox,oy=self.X(),self.Y()
            
            poo.replace()
            target.remove()
            
            self.removeReplace(x,y)
            BOARD[ox][oy]=poo

    def setDirection(self,newDirection):
        x=self.X()+newDirection[0]
        y=self.Y()+newDirection[1]
        if not BOARD[x][y].blocks():
            self.direction = newDirection


class Game(Frame):

    def __init__(self):
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
                    BOARD[x][y]=Power(x,y)
                if char=='C':
                    PLAYER=Pacman(x,y)
                    BOARD[x][y]=PLAYER
                if char=='X':
                    BOARD[x][y]=Wall(x,y)
                x+=1
            y+=1

        self.player=PLAYER

        self.play()
        
    def play(self):#Main play loop
        interval=.333
        start=time.time()
        playing=True
        while playing:
            self.update_idletasks()
            self.update()
            
            if start+interval>time.time():
                continue
            
            start=time.time()
            self.player.move()
            
            self.canvas.update()

    def input(self,event):
        if event.keycode == 38:
            self.player.setDirection(UP)
        elif event.keycode == 39:
            self.player.setDirection(RIGHT)
        elif event.keycode == 40:
            self.player.setDirection(DOWN)
        elif event.keycode == 37:
            self.player.setDirection(LEFT)

Game().mainloop()
