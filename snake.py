import pygame
import time
import random

pygame.init()

clock=pygame.time.Clock()
white = (255,255,255)
red = (255,0,0)
green= (0,145,0)
blue = (0,0,255)
black=(0,0,0)
direction="right"
block=20
width=800
height=600
gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Snakey')
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)
sndtrck=pygame.mixer.music.load("Race_car.wav")

img1=pygame.image.load("apple.png")
img=pygame.image.load('snakehd2.png')
font = pygame.font.SysFont(None,  25)

def pause():
    paused=True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()

    pygame.fill(black)
    message(pausef,green)

def game_intro():

    intro=True

    while intro:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    intro=False

        gameDisplay.fill(black)
        message("Welcome to Snake!",blue,-45)
        message("Press C to play!", blue)

        pygame.display.update()
        clock.tick(15)

def paused():
    print("PAUSE")
    gameDisplay.fill(black)
    message("PAUSE",red)
    message("PRESS C TO PLAY AGAIN", red)

def transition(block,snakelist):
    print("Transition")

def snake(block, snakelist):

    if direction=="down":
        head=pygame.transform.rotate(img,270)

    #gameDisplay.blit(head,(snakelist[-1][0],snakelist[-1][1]))

    for xy in snakelist[:-1]: #except last elem
        pygame.draw.rect(gameDisplay, green, [xy[0], xy[1], block, block])

def text_objects(msg,color):
    textSurface=font.render(msg,True,color)  #gets the font
    return textSurface,textSurface.get_rect()

def message(msg,color,yOffSet=-15,xOffset=0):
    textSurf, textRect = text_objects(msg,color)
    #screen_text=font.render(msg,True,color)
    #gameDisplay.blit(screen_text, (width/2,height/2))
    textRect.center = (width/2-xOffset),(height/2-yOffSet)
    gameDisplay.blit(textSurf, textRect)

def gameLoop():
    score = 0
    direction="right"
    vel=1

    gameExit = False
    gameOver = False

    lead_x = width / 2
    lead_y = height / 2
    lead_x_change = 10
    lead_y_change = 0

    snakelist=[]
    snakeLength=1

    randAppleX = round(random.randrange(0, width - block))# / 10* 10
    randAppleY = round(random.randrange(0, height - block))# / 10) * 10

    pygame.mixer.music.play(-1)

    while not gameExit:

        while gameOver:
            gameDisplay.fill(white)
            message("Press C to play again or Q to quit",green)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit=True
                    gameOver=False
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        gameExit=True
                        gameOver=False
                    if event.key==pygame.K_c:
                        gameExit=False
                        gameLoop()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit=True
            if event.type==pygame.KEYDOWN:
                if event.type==pygame.K_p:
                    paused()
                if event.key == pygame.K_a and not direction =="left":
                    lead_x_change-=block+vel
                    lead_y_change=0
                    direction="left"
                elif event.key == pygame.K_d and not direction =="right":
                    lead_x_change+=block+vel
                    lead_y_change=0
                    direction="right"
                elif event.key == pygame.K_w and not direction =="up":
                    lead_y_change-=block+vel
                    lead_x_change=0
                    direction="up"
                elif event.key == pygame.K_s and not direction =="down":
                    lead_y_change+=block+vel
                    lead_x_change=0
                    direction="down"

        if lead_x<0 or lead_x>width or lead_y<0 or lead_y>height:
            transition(block,snakelist)

        if lead_x>=width or lead_x<0 or lead_y>=height or lead_y<0:
                gameOver=True

        lead_x+=lead_x_change
        lead_y+=lead_y_change

        gameDisplay.fill(black)
        ###################################
        appleThickness=30
        #apple = pygame.draw.rect(gameDisplay, red, (randAppleX, randAppleY, appleThickness, appleThickness))
        gameDisplay.blit(img1,(randAppleX,randAppleY))

        snakeHead=[]
        snakeHead.append(int(lead_x))
        snakeHead.append(int(lead_y))
        snakelist.append(snakeHead)

        if len(snakelist)>snakeLength:
            del snakelist[0]

        #Snake colision
        for eachSegment in snakelist[:-1]: #ult elem
            if eachSegment==snakeHead:
                gameOver=True
            #print("List: ",snakelist)
            #print("Head: ",snakeHead)
        snake(block,snakelist)

        pygame.draw.rect(gameDisplay, green, (int(lead_x),int(lead_y),block,block))
        message("SCORE: "+str(score),blue,280,358)
        ###################################
        pygame.display.update()

        """
        if lead_x>=randAppleX and lead_x<=randAppleX+appleThickness and lead_y>=randAppleY and lead_y<=randAppleY+appleThickness:
            randAppleX = round(random.randrange(0, width - block))# / 10) * 10
            randAppleY = round(random.randrange(0, height - block))# / 10) * 10
            snakeLength += 1
        """

        if lead_x>randAppleX and lead_x<randAppleX+appleThickness or lead_x+block>randAppleX and lead_x+block<randAppleX+appleThickness:
            if lead_y>randAppleY and lead_y<randAppleY or lead_y+block>randAppleY and lead_y-block<randAppleY+appleThickness:
                randAppleX = round(random.randrange(0, width - block))  # / 10) * 10
                randAppleY = round(random.randrange(0, height - block))  # / 10) * 10
                snakeLength += 1
                score+=2

        vel+=vel/pygame.time.get_ticks()
        #print(vel)

        clock.tick(15)

    pygame.quit()

game_intro()
gameLoop()