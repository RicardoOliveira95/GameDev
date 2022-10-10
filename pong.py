import turtle
from turtle import *

speed=35
sc=turtle.Screen()
sc.title("PONG")
sc.bgcolor("black")
sc.setup(width=640,height=480)
#LEFT PADDLE
left_pad=turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("white")
left_pad.shapesize(stretch_wid=5,stretch_len=2)
left_pad.penup()
left_pad.goto(-300,0)
#RIGHT PADDLE
right_pad=turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("white")
right_pad.shapesize(stretch_wid=5,stretch_len=2)
right_pad.penup()
right_pad.goto(300,0)
#BALL
ball=turtle.Turtle()
ball.speed(speed)
ball.shape("circle")
ball.color("orange")
ball.shapesize(stretch_wid=2,stretch_len=2)
ball.penup()
ball.goto(0,0)
ball.dx=7
ball.dy=-7
#Init scores
left_player=0
right_player=0
#Display score
sketch=turtle.Turtle()
sketch.speed(0)
sketch.color("green")
sketch.penup()
sketch.goto(0,180)
sketch.write("Left player: 0    Right player: 0",align="center",font=("Arial",18,"normal"))
#Middle line
x1=(0,-320)
x2=(0,320)
tur=turtle.Turtle()
tur.color('white')
tur.penup()
tur.width(10)
tur.goto(x1)
tur.pendown()
tur.goto(x2)
#Middle circle
t=turtle.Turtle()
t.color("white")
t.pensize(5)
t.setposition(0,-30)
t.circle(30)
#t.goto(0,25)
#tur.forward(150)
#tur.done()

def paddlea_up():
	y=left_pad.ycor()
	y+=18
	left_pad.sety(y)

def paddlea_down():
	y=left_pad.ycor()
	y-=18
	left_pad.sety(y)

def paddleb_up():
	y=right_pad.ycor()
	y+=18
	right_pad.sety(y)

def paddleb_down():
	y=right_pad.ycor()
	y-=18
	right_pad.sety(y)

sc.listen()
sc.onkeypress(paddlea_up,"w")
sc.onkeypress(paddlea_down,"s")
sc.onkeypress(paddleb_up,"Up")
sc.onkeypress(paddleb_down,"Down")

while True:
	sc.update()

	ball.setx(ball.xcor()+ball.dx)
	ball.sety(ball.ycor()+ball.dy)
	#Checking borders
	if ball.ycor()>240:
		ball.sety(240)
		ball.dy*=-1
	if ball.ycor()<-240:
		ball.sety(-240)
		ball.dy*=-1
	#Goal
	if ball.xcor()>320:
		ball.goto(0,0)
		ball.dy*=-1
		left_player+=1
		sketch.clear()
		sketch.write("Left player :{}    Right player: {}".format(left_player,right_player),align="center",font=("Arial",20,"normal"))

	if ball.xcor()<-320:
		ball.goto(0,0)
		right_player+=1
		ball.dy*=-1
		sketch.clear()
		sketch.write("Left player :{}    Right player: {}".format(left_player,right_player),align="center",font=("Arial",20,"normal"))
	#Collision w/paddles
	if ball.xcor()>300 and ball.xcor()<310 and ball.ycor()<right_pad.ycor()+40 and ball.ycor()>right_pad.ycor()-40:
		ball.setx(300)
		ball.dx*=-1
	if ball.xcor()<-300 and ball.xcor()>-310 and ball.ycor()<left_pad.ycor()+40 and ball.ycor()>left_pad.ycor()-40:
		ball.setx(-300)
		ball.dx*=-1

	#print(ball.xcor(),",",ball.ycor())
	#print(right_pad.ycor())
	#OFFBOUNDS
	if left_pad.ycor()>240:
		left_pad.sety(240)
	if left_pad.ycor()<-240:
		left_pad.sety(-240)
	if right_pad.ycor()>240:
		right_pad.sety(240)
	if right_pad.ycor()<-240:
		right_pad.sety(-240)

	if left_player==7:
		sketch.clear()
		sketch.write("Left player won!",align="center",font=("Arial",20,"normal"))
		left_player=0
		right_player=0
	elif right_player==7:
		sketch.clear()
		sketch.write("Right player won!",align="center",font=("Arial",20,"normal"))
		left_player=0
		right_player=0