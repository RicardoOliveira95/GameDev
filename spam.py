import turtle
from turtle import *
import time

start_time=time.time()
timer=0
running=True
sc=turtle.Screen()
sc.title("SPAM")
sc.bgcolor("gray")
sc.setup(width=640,height=480)
#LEFT PLAYER
left_player=turtle.Turtle()
left_player.shape("circle")
left_player.color("red")
left_player.shapesize(stretch_wid=5,stretch_len=2)
left_player.penup()
left_player.goto(-240,100)
#RIGHT PLAYER
right_player=turtle.Turtle()
right_player.shape("circle")
right_player.color("blue")
right_player.shapesize(stretch_wid=5,stretch_len=2)
right_player.penup()
right_player.goto(240,100)

right_player_scr=0
left_player_scr=0
print("Variables: ",right_player_scr,", ",left_player_scr)
#SCOREBOARD
sketch=turtle.Turtle()
sketch.speed(0)
sketch.color("yellow")
sketch.penup()
sketch.goto(0,150)
sketch.write("Left player: 0   -   Right player : 0",align="center",font=("Arial",18,"normal"))

def inc_rp():
	global right_player_scr
	right_player_scr=right_player_scr+1
	print(right_player_scr)

def inc_lp():
	global left_player_scr
	left_player_scr+=1
	print(left_player_scr)

sc.listen()
sc.onkeypress(inc_rp,"x")
sc.onkeypress(inc_lp,"space")

while True:
	sc.update()
	if running:
		sketch.clear()
		sketch.write("Left player: {}    -     Right player: {}".format(left_player_scr,right_player_scr),align="center",font=("Arial",20,"normal"))

	last_time=time.time()
	print(start_time,",",last_time)
	if(last_time-20>start_time):
		sketch.clear()
		running=False
		if(left_player_scr>right_player_scr):
			sketch.write("Left player won with "+str(left_player_scr)+" hits!",align="center",font=("Arial",20,"normal"))
		elif(right_player_scr>left_player_scr):
			sketch.write("Right player with "+str(right_player_scr)+" hits!",align="center",font=("Arial",20,"normal"))
		else:
			sketch.write("It's a draw.. "+str(right_player_scr)+"-"+str(left_player_scr),align="center",font=("Arial",20,"normal"))
	