import pygame
from pygame.locals import *
pygame.init()
import sys
import random
import math

screenWidth = 480
screenHeight = 480
Screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Snake")
FPS = 24

def Game(food):
    _snake,Head,Tail=ResetSnake()
    GoLeft=True
    GoRight=False
    GoUp=False
    GoDown=False
    updateTime=pygame.time.get_ticks()
    hr=0
    phr=hr
    nearFood=False
    turnhead=False
    score=0
    sc=score
    Slist=[]
    while True:
        Slist.insert(0,sc%10)
        sc=sc//10
        if sc==0:
            break
    eat=False
    Dead=False
    spin=False
    askReset=False
    spini=0
    spinTime=pygame.time.get_ticks()
    
    while True:
        for event in pygame.event.get():#takes input from the player
            if event.type==QUIT:#quit the game when the player clicks quit
                pygame.quit()
                sys.exit()
            if askReset:
                if event.type == KEYDOWN and event.key==K_SPACE:
                    Game(food) 
            if not Dead:
                if (event.type == KEYDOWN and (event.key==K_w or event.key==K_UP)) and not GoDown:
                    turnhead=True
                    hr=270
                    GoLeft=False
                    GoRight=False
                    GoUp=True
                    GoDown=False
                elif (event.type == KEYDOWN and (event.key==K_s or event.key==K_DOWN)) and not GoUp:
                    turnhead=True
                    hr=90
                    GoLeft=False
                    GoRight=False
                    GoUp=False
                    GoDown=True
                elif (event.type == KEYDOWN and (event.key==K_d or event.key==K_RIGHT)) and not GoLeft:
                    turnhead=True
                    hr=180
                    GoLeft=False
                    GoRight=True
                    GoUp=False
                    GoDown=False
                elif (event.type == KEYDOWN and (event.key==K_a or event.key==K_LEFT)) and not GoRight:
                    turnhead=True
                    hr=0
                    GoLeft=True
                    GoRight=False
                    GoUp=False
                    GoDown=False

        if pygame.time.get_ticks() > updateTime+100 and not askReset: 
            if not Dead:
                if turnhead:
                    if nearFood:
                        Head = pygame.transform.rotate(SnakeMouthOpen, hr)
                    else:
                        Head = pygame.transform.rotate(SnakeHead, hr)                    
                    turnhead=False
                if not eat:
                    tailx=_snake[len(_snake)-2]["x"]
                    taily=_snake[len(_snake)-2]["y"]
                    for position in range(len(_snake)-1,0,-1):
                        _snake[position]["x"]=_snake[position-1]["x"]
                        _snake[position]["y"]=_snake[position-1]["y"]
                    if tailx==_snake[len(_snake)-2]["x"]:
                        if taily<_snake[len(_snake)-2]["y"]:#goingdown
                            Tail=pygame.transform.rotate(SnakeTail,90)
                        elif taily>_snake[len(_snake)-2]["y"]:#goingup
                            Tail=pygame.transform.rotate(SnakeTail,270)
                    else:
                        if tailx<_snake[len(_snake)-2]["x"]:#goingright
                            Tail=pygame.transform.rotate(SnakeTail,180)
                        elif tailx>_snake[len(_snake)-2]["x"]:#goingleft
                            Tail=pygame.transform.rotate(SnakeTail,0)
                else:
                    _snake.insert(1, {"x":_snake[0]["x"],"y":_snake[0]["y"]})
                    eat=False
                if GoRight:
                    _snake[0]["x"]+=16
                elif GoLeft:
                    _snake[0]["x"]-=16
                elif GoDown:
                    _snake[0]["y"]+=16
                elif GoUp:
                    _snake[0]["y"]-=16
                Dead = checkCollision(_snake)
                if Dead:
                    Head=pygame.transform.rotate(SnakeCrashed, hr)
                else:
                    phr=hr
            else:
                Head=pygame.transform.rotate(SnakeCrashed, phr)
                _snake[0]["x"]=_snake[1]["x"]
                _snake[0]["y"]=_snake[1]["y"]
                spin=True
                spini=0
                spinTime=pygame.time.get_ticks()
                askReset=True
            if _snake[0]["x"]==food["x"] and _snake[0]["y"]==food["y"]:
                score+=1
                sc=score
                Slist=[]
                while True:
                    Slist.insert(0,sc%10)
                    sc=sc//10
                    if sc==0:
                        break
                food=randomPosition()
                print(score)
                eat=True
            if math.sqrt((_snake[0]["x"]-food["x"])**2 + (_snake[0]["y"]-food["y"])**2) <= 32 and not nearFood:
                nearFood=True
                Head=pygame.transform.rotate(SnakeMouthOpen, hr)
            elif math.sqrt((_snake[0]["x"]-food["x"])**2 + (_snake[0]["y"]-food["y"])**2) > 32 and nearFood:
                nearFood=False
                Head=pygame.transform.rotate(SnakeHead, hr)
            updateTime=pygame.time.get_ticks()
            
        Screen.fill((50,200,50))        
        for i in range(1,len(_snake)-1):
            Screen.blit(SnakeBody,(_snake[i]["x"],_snake[i]["y"]))
        Screen.blit(Tail,(_snake[len(_snake)-1]["x"],_snake[len(_snake)-1]["y"]))
        Screen.blit(Head,(_snake[0]["x"]-2,_snake[0]["y"]-2))

        Screen.blit(Apple,(food["x"],food["y"]))

        if spin:
            Screen.blit(Spinimg[spini],(_snake[0]["x"]-7,_snake[0]["y"]-7))
        if pygame.time.get_ticks()>spinTime+50:
            spini+=1
            if spini>5:
                spini=0
            spinTime=pygame.time.get_ticks()

        if askReset:
            Screen.blit(TryAgain,(164,180))
            
        uix=15
        Screen.blit(AppleLogo,(uix,15))
        uix+=35
        Screen.blit(Ximg,(uix,15))
        uix+=35
        for i in Slist:
            Screen.blit(Numbers[i],(uix,15))
            uix+=30
          
        pygame.display.update()
        fpsclock.tick(FPS)

def ResetSnake():
    snakeLength=4
    sx=240
    _snake=[]
    for i in range(snakeLength):
        _snake.append({"x":sx,"y":240})
        sx+=16
    Head=pygame.transform.rotate(SnakeHead,0)
    Tail=pygame.transform.rotate(SnakeTail,0)
    return _snake,Head,Tail

def randomPosition():
    x= random.randint(0,29)*16
    y= random.randint(0,29)*16
    food={"x":x,"y":y}
    return food

def checkCollision(_snake):
    Dead=False
    for j in range(1,len(_snake)):
        if _snake[0]["x"]==_snake[j]["x"] and _snake[0]["y"]==_snake[j]["y"]:
            Dead=True
    if (0>_snake[0]["x"] or _snake[0]["x"]>screenWidth-16) or (0>_snake[0]["y"] or _snake[0]["y"]>screenHeight-16):
        Dead=True
    return Dead

SnakeHead = pygame.image.load("Data/Sprites/snakeHead.png")
SnakeMouthOpen = pygame.image.load("Data/Sprites/snakeMouthOpen.png")
SnakeCrashed = pygame.image.load("Data/Sprites/snakeCrashed.png")
SnakeBody = pygame.image.load("Data/Sprites/snakeBody.png")
SnakeTail = pygame.image.load("Data/Sprites/snakeTail.png")
Apple = pygame.image.load("Data/Sprites/apple.png")
AppleLogo = pygame.image.load("Data/Sprites/appleLogo.png")
Numbers=(
    pygame.image.load("Data/Sprites/numbers/0.png"),
    pygame.image.load("Data/Sprites/numbers/1.png"),
    pygame.image.load("Data/Sprites/numbers/2.png"),
    pygame.image.load("Data/Sprites/numbers/3.png"),
    pygame.image.load("Data/Sprites/numbers/4.png"),
    pygame.image.load("Data/Sprites/numbers/5.png"),
    pygame.image.load("Data/Sprites/numbers/6.png"),
    pygame.image.load("Data/Sprites/numbers/7.png"),
    pygame.image.load("Data/Sprites/numbers/8.png"),
    pygame.image.load("Data/Sprites/numbers/9.png"),
    )
Ximg=pygame.image.load("Data/Sprites/numbers/x.png")

Spinimg=(
    pygame.image.load("Data/Sprites/spin1.png"),
    pygame.image.load("Data/Sprites/spin2.png"),
    pygame.image.load("Data/Sprites/spin3.png"),
    pygame.image.load("Data/Sprites/spin4.png"),
    pygame.image.load("Data/Sprites/spin5.png"),
    pygame.image.load("Data/Sprites/spin6.png"),
    )
TryAgain=pygame.image.load("Data/Sprites/tryagain.png")

fpsclock=pygame.time.Clock()
food=randomPosition()
Game(food)