import math
import random
import pygame
from pygame import mixer
from pygame.locals import *

colors=[(10,5,250),(250,10,5)]
num_of_bubbles=29
num_of_bombs=3
total_bubbles=0
time=0
pygame.init()
screen=pygame.display.set_mode((640,480))
pygame.display.set_caption("BUBBLE'z")

bubbleX=[]
bubbleY=[]
bubbleX_change=[]
bubbleY_change=[]
bombX=[]
bombY=[]
bombX_change=[]
bombY_change=[]
score=0
grav=random.randrange(1,9)*0.001

pygame.time.set_timer(USEREVENT+1,5000)

for i in range(num_of_bubbles):
    bubbleX.append(random.randint(0,640))
    bubbleY.append(random.randint(-300,0))
    bubbleY_change.append(15)

for i in range(num_of_bombs):
    bombX.append(random.randint(0,640))
    bombY.append(random.randint(-300,0))
    bombY_change.append(15)

def bubble(x,y):
    #print("DRAW BUBBLE")
    ell_rect=pygame.Rect(x,y,20,20)
    pygame.draw.ellipse(screen,colors[0],ell_rect)

def bomb(x,y):
    #print("DRAW BUBBLE")
    ell_rect=pygame.Rect(x,y,20,20)
    pygame.draw.ellipse(screen,colors[1],ell_rect)

score=0
running=True

while running:
    time+=1
    #pygame.time.delay(100)
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()
            quit()
        
        #if event.type==USEREVENT+1:
            #num_of_bubbles+=5
        
        if event.type==pygame.MOUSEBUTTONDOWN:
            x=pygame.mouse.get_pos()[0]
            y=pygame.mouse.get_pos()[1]
            #print("MOUSE: ",x,", ",y)

            for i in range(num_of_bubbles):
                #print(bubbleX[i],", ",bubbleY[i])
                if(bubbleX[i]<x and bubbleX[i]+20>x and int(bubbleY[i])<y and int(bubbleY[i])+20>y):
                    #print("CLICK: ",bubbleX[i]," ,",bubbleY[i])
                    bubbleX[i]=random.randrange(0,620)
                    bubbleY[i]=-random.randrange(100,300)
                    score+=1
                    total_bubbles+=1
                if(bubbleY[i]>640):
                    bubbleY[i]=-random.randrange(100,300)
                    total_bubbles+=1
            
            for i in range(num_of_bombs):
                #print(bubbleX[i],", ",bubbleY[i])
                if(bombX[i]<x and bombX[i]+20>x and int(bombY[i])<y and int(bombY[i])+20>y):
                    #print("CLICK: ",bubbleX[i]," ,",bubbleY[i])
                    bombX[i]=random.randrange(0,620)
                    bombY[i]=-random.randrange(100,300)
                    score-=5
                if(bombY[i]>640):
                    bombY[i]=-random.randrange(100,300)
        
    for i in range(num_of_bubbles):
        bubbleY[i]+=bubbleY_change[i]*grav
        bubble(bubbleX[i],bubbleY[i])
    
    for i in range(num_of_bombs):
        bombY[i]+=bombY_change[i]*grav
        bomb(bombX[i],bombY[i])

    font=pygame.font.SysFont('arial',21)
    score_text=font.render("SCORE: "+str(score),1,(200,100,50))
    
    if(time>=100000):
        num_of_bubbles=0
        num_of_bombs=0
        final_score_text=font.render(str(score)+"/"+str(total_bubbles),1,(10,10,245))
        screen.blit(final_score_text,(300,240))
        #print("timeout..")
    
    screen.blit(score_text,(550,10))
    pygame.display.update()

        
