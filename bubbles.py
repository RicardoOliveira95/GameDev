import math
import random
import pygame
from pygame import mixer

num_of_bubbles=29
pygame.init()
screen=pygame.display.set_mode((640,480))
pygame.display.set_caption("BUBBLE'z")

bubbleX=[]
bubbleY=[]
bubbleX_change=[]
bubbleY_change=[]
score=0

for i in range(num_of_bubbles):
    bubbleX.append(random.randint(0,640))
    bubbleY.append(random.randint(-300,0))
    bubbleY_change.append(15)

def bubble(x,y):
    #print("DRAW BUBBLE")
    ell_rect=pygame.Rect(x,y,20,20)
    pygame.draw.ellipse(screen,(10,5,250),ell_rect)
score=0
running=True

while running:
    #pygame.time.delay(100)
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()
            quit()
        
        if event.type==pygame.MOUSEBUTTONDOWN:
            x=pygame.mouse.get_pos()[0]
            y=pygame.mouse.get_pos()[1]
            print("MOUSE: ",x,", ",y)

            for i in range(num_of_bubbles):
                print(bubbleX[i],", ",bubbleY[i])
                if(bubbleX[i]<x and bubbleX[i]+20>x and int(bubbleY[i])<y and int(bubbleY[i])+20>y):
                    print("CLICK: ",bubbleX[i]," ,",bubbleY[i])
                    bubbleX[i]=1000
                    bubbleY[i]=1000
                    score+=1
        
    for i in range(num_of_bubbles):
        bubbleY[i]+=bubbleY_change[i]*0.001
        bubble(bubbleX[i],bubbleY[i])
    
    font=pygame.font.SysFont('arial',21)
    score_text=font.render("SCORE: "+str(score),1,(200,100,50))
    screen.blit(score_text,(550,10))
    pygame.display.update()

        