import pygame as pg
from pygame.math import Vector2

# pg setup
pg.init()

gridHeight = 15
gridWidth = 7
squareSize = 30

topPadding = 100
sidePadding = 100
squarePadding = 5

screenWidth = gridWidth * (squareSize + squarePadding) + (2 * sidePadding)
screenHeight = gridHeight * (squareSize + squarePadding) + ( 2 * topPadding)
screenCenter = pg.Vector2(screenWidth/2, screenWidth/2)

ledSquares: list[list[pg.Rect]]= []

squareOff = 'grey'
squareOn = 'red'

frameRate = 30
framesPerMove = 5

bounceDirection: int = 1
ledCount: int = 3

screen = pg.display.set_mode((screenWidth, screenHeight))

clock = pg.time.Clock()

running = True

bounceLedStartPos: pg.Vector2 = pg.Vector2(0, gridHeight - 1)
bounceLed: list[pg.Vector2] = [pg.Vector2(bounceLedStartPos.x, bounceLedStartPos.y)]
# onLed: list[list[pg.Vector2]] = [[pg.Vector2(0, 0)]]
onLed: list[pg.Vector2] = []

frameCount = 0

def createLedSquares():
    for y in range(gridHeight):
        ledRow: list[pg.Rect] = []
        for x in range(gridWidth):
            pos = pg.Vector2(sidePadding + (x * squareSize) + (x * squarePadding), topPadding + (y * squareSize) + (y * squarePadding))
            led = pg.Rect(pos.x, pos.y, squareSize, squareSize)
            ledRow.append(led)
        ledSquares.append(ledRow)

def displayLeds(leds: list[pg.Vector2]):
    # clear all led squares
    for ledRow in range(len(ledSquares)):
        for ledCol in range(len(ledSquares[0])):
            color = squareOff 
            pg.draw.rect(screen, color, ledSquares[ledRow][ledCol])
    for pos in leds:
        color = squareOn
        pg.draw.rect(screen, color, ledSquares[int(pos.y)][int(pos.x)])

def bounceLeds():
    global bounceDirection
    global ledCount
    hasHitRight: bool = bounceLedStartPos.x + ledCount - 1 == gridWidth and bounceDirection == 1
    hasHitLeft: bool = bounceLedStartPos.x == -1 and bounceDirection == -1 
    if(hasHitRight or hasHitLeft):
        bounceDirection *= -1
        bounceLedStartPos.x = bounceLed[0].x + bounceDirection
    for x in range(ledCount):
        if(len(bounceLed) < x + 1):
            bounceLed.append(pg.Vector2(bounceLed[x - 1].x + 1, bounceLed[x - 1].y))
        bounceLed[x].x = bounceLedStartPos.x + x
        bounceLed[x].y = bounceLedStartPos.y
    bounceLedStartPos.x += bounceDirection

createLedSquares()

while running:
    stopped: bool = False
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
            running = False
        if event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_SPACE]: 
            stopped = True

    if(stopped):
        lastRowPos: list[float] = []
        isStacked: bool = False
        for pos in onLed:
            if(pos.y == bounceLedStartPos.y + 1 and len(onLed) > 0):
                lastRowPos.append(pos.x)
        if(len(lastRowPos) > 0):
            for pos in bounceLed:
                if(lastRowPos.count(pos.x) > 0):
                    onLed.append(pg.Vector2(pos.x, pos.y))
                    isStacked = True
        if(len(onLed) == 0):
            for pos in bounceLed:
                onLed.append(pg.Vector2(pos.x, pos.y))
                isStacked = True
        # for led in bounceLed:
        #     onLed.append(pg.Vector2(led.x, led.y))
        bounceLedStartPos.y -= 1
        bounceLedStartPos.x = 0
        bounceDirection = 1
        if(bounceLedStartPos.y < 0 or not isStacked):
            running = False
            continue

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    # set on led from frame count
    frameCount += 1
    if(frameCount % framesPerMove == 0):
        bounceLeds()        

    displayLeds(bounceLed + onLed)

    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(frameRate)  # limits FPS to 60

