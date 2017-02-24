#! /usr/bin/env python

import pygame
import random
import socket
import sys

HOST = '127.0.0.1' 
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket created")


class Snake:
    def __init__(self,surface):
        self.surface=surface
        self.x=surface.get_width()/2
        self.y=surface.get_height()/2
        self.length=1
        self.grow_to=50
        self.vx=0
        self.vy=-1
        self.body=[]
        self.crashed=False
        self.color=255,255,0

    def consume(self):
        self.grow_to+=25
        
    def event(self,event):
        if event.key==pygame.K_UP:
            self.vx=0
            self.vy=-1
        elif event.key==pygame.K_DOWN:
            self.vx=0
            self.vy=1
        elif event.key==pygame.K_LEFT:
            self.vx=-1
            self.vy=0
        elif event.key==pygame.K_RIGHT:
            self.vx=1
            self.vy=0

    def motion(self):
        self.x+=self.vx
        self.y+=self.vy
        
        if (self.x,self.y) in self.body:
            self.crashed=True
            
        self.body.insert(0,(self.x,self.y))
        if (self.grow_to>self.length):
            self.length+=1

        if len(self.body) > self.length:
            self.body.pop()

    def draw(self):
        for x,y in self.body:
            self.surface.set_at((x,y),self.color)

    def position(self):
        return self.x, self.y

class Food:
    def __init__(self,surface):
        self.surface=surface
        self.x=random.randint(0,surface.get_width())
        self.y=random.randint(0,surface.get_height())
        self.color=255,255,255

    def draw(self):
        self.surface.set_at((self.x,self.y),self.color)

    def position(self):
        return self.x, self.y

w=500
h=500
screen=pygame.display.set_mode((w,h))
clock=pygame.time.Clock()
score=0
snake=Snake(screen)
food=Food(screen)
running=True

while running:
    screen.fill((0,0,0))
    snake.motion()
    snake.draw()
    food.draw()
    if snake.crashed:
        running=False
        
        try:
            s.connect((HOST,PORT))
            print("Connected")
            s.send(str(score))
            print("Your score %d" %score )
            data=s.recv(1024)
            hs=data.split(",")
            print ("High score is: " + hs[1] + " which belongs to " + hs[0])


        except:
            print("Not connected")

        s.close()

    elif snake.x <= 0 or snake.x >= w-1:
        running=False
    
        try:
            s.connect((HOST,PORT))
            print("Connected")     
            s.send(str(score))
            print("Your score %d" %score )
            data=s.recv(1024)
            hs=data.split(",")
            print ("High score is: " + hs[1] + " which belongs to " + hs[0])


        except:
            print("Not connected")

        s.close()

    elif snake.y <= 0 or snake.y >=h-1:
        running=False
    
        try:
            s.connect((HOST,PORT))
            print("Connected")
            s.send(str(score))
            print("Your score %d" %score )
            data=s.recv(1024)
            hs=data.split(",")
            print ("High score is: " + hs[1] + " which belongs to " + hs[0])



        except:
            print("Not connected")

        s.close()

    elif snake.position()==food.position():
        score+=1
        snake.consume()
        #print "HIGHEST SCORE: %d" %score
        food=Food(screen) 

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            
            try:
                s.connect((HOST,PORT))
                print("Connected")
                s.send(str(score))
                print("Your score %d" %score )
                data=s.recv(1024)
                hs=data.split(",")
                print ("High score is: " + hs[1] + " which belongs to " + hs[0])


            except:
                print("Not connected")

            s.close()



        elif event.type==pygame.KEYDOWN:
            snake.event(event)
    
    pygame.display.flip()
    clock.tick(100)
