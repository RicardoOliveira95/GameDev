import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H=480,640
win=pygame.display.set_mode((W,H))
pygame.display.set_caption("Flappy bird'z")

bg=pygame.image.load(os.path.join('ftex','bg1.jpg')).convert()
fg=pygame.image.load(os.path.join('ftex','fg.png')).convert()
jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4]
clock=pygame.time.Clock()
isGameOver=False

class Bird(object):
    bird_img=pygame.image.load(os.path.join('ftex','bird.png'))
    bird_img1=pygame.image.load(os.path.join('ftex','bird3.png')).convert()
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.jumping=False
        self.falling=True
        self.GRAV=4
        self.jumpCount=0
        #self.hitbox=(0,0,0,0)

    def draw(self,win):
        win.blit(self.bird_img,(self.x,self.y))
        self.hitbox=(self.x,self.y,self.bird_img1.get_width(),self.bird_img.get_height())
        if self.falling:
            self.y+=self.GRAV
        
        if self.jumping:
            self.y-=6
            self.jumpCount+=1
        
        if self.jumpCount>=18:
            self.jumpCount=0
            self.jumping=False
            self.falling=True
        
        if self.y>H-self.bird_img.get_height():
            self.falling=False
            print("FALL: ",bg.get_width())

class PipeN(object):
    pipeN_img=pygame.image.load(os.path.join('ftex','pipeNorth.png'))
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vel=1.4
        self.hitbox=(0,0,0,0)
    
    def draw(self,win):
        self.hitbox=(self.x+10,self.y+5,self.pipeN_img.get_width(),self.pipeN_img.get_height())
        win.blit(self.pipeN_img,(self.x,self.y))
        self.x-=self.vel
        print(self.hitbox)

    def collide(self,rect):
        if rect[0]+rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:
            if rect[1]+rect[3]>self.hitbox[1]:
                return True
            return False

class PipeS(object):
    pipeS_img=pygame.image.load(os.path.join('ftex','pipeSouth.png'))
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vel=1.4
        #self.hitbox=(0,0,0,0)
    
    def draw(self,win):
        self.hitbox=(self.x+10,self.y+5,self.pipeS_img.get_width(),self.pipeS_img.get_height())
        win.blit(self.pipeS_img,(self.x,self.y))
        self.x-=self.vel
        #print("Pipe south: ",self.x,",",self.y);

    def collide(self,rect):
        if rect[0]+rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:
            if rect[1]+rect[3]>self.hitbox[1]:
                return True
            return False

def endScreen():
    global score,speed
    speed=30

    run=True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    quit()


def redrawWindow():
    if not isGameOver:
        font=pygame.font.SysFont("arial",22)
        win.blit(bg,(0,0))
        win.blit(fg,(0,H-fg.get_height()))
        win.blit(fg,(fg.get_width(),H-fg.get_height()))
        text=font.render('Score: '+str(score),1,(250,252,250))
        bird.draw(win)
        win.blit(text,(W-65,15))
        for obstacle in obstacles:
            obstacle.draw(win)
        win.blit(text,(600,10))
    else:
        gameOverFont=pygame.font.SysFont("comicsans",30)
        gameover_text=gameOverFont.render("GAMEOVER!",1,(250,10,5))
        win.blit(gameover_text,(W/2,H/2))
    pygame.display.update()

speed=20
score=0
run=True
bird=Bird(10,10)
pause=0
obstacles=[]
#EVENTS
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+2,1500)

while run:
    if pause>0:
        pause+=1
        if pause>speed*2:
            endScreen()
    
    score=speed//10-3

    for obstacle in obstacles:
        if obstacle.collide(bird.hitbox):
            isGameOver=True
            pause=1
        if obstacle.x<-50:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x-=1.4
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            run=False
        
        if event.type==USEREVENT+1:
            speed+=1
        
        if event.type==USEREVENT+2:
            r=random.randrange(0,2)
            if r==0:
                obstacles.append(PipeN(640,random.randrange(-100,0)))
            elif r==1:
                obstacles.append(PipeS(640,random.randrange(400,500)))

    keys=pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        bird.jumping=True   

    clock.tick(speed)
    redrawWindow()