import pygame as pg

# pg setup
pg.init()
pg.font.init()

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
framesPerMove = 1
speed: list[float] = [6, 3, 2]
speedChanges: list[float] = [6, 12]
speedTracker: int = 0

ledBounceLength: list[int] = [3, 2, 1]
ledBounceLengthTracker: int = 0
ledBounceChanges: list[int] = [6, 12]

bounceDirection: int = 1
ledCount: int = 3

screen = pg.display.set_mode((screenWidth, screenHeight))
prizeFont = pg.font.SysFont('comicsans', 32)
minorPrize = pg.font.Font.render(prizeFont, "MINOR PRIZE", True, 'blue')
minorPrizePos = [sidePadding + ((squareSize + squarePadding) * 1.33), topPadding + ((squareSize + squarePadding) * 5.15)]
majorPrize = pg.font.Font.render(prizeFont, "MAJOR PRIZE", True, 'blue')
majorPrizePos = [sidePadding + ((squareSize + squarePadding) * 1.33), topPadding + ((squareSize + squarePadding) * 0.15)]
gameNameFont = pg.font.SysFont('comicsans', 64)
gameName = pg.font.Font.render(gameNameFont, "STACKER", True, 'black')
gameNamePos = [sidePadding + ((squareSize + squarePadding) * 0.40), topPadding + ((squareSize + squarePadding) * (gridHeight + 0.5))]

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
    # global ledCount
    # hasHitRight: bool = bounceLedStartPos.x + ledCount - 1 == gridWidth and bounceDirection == 1
    hasHitRight: bool = bounceLedStartPos.x + ledBounceLength[ledBounceLengthTracker] - 1 == gridWidth and bounceDirection == 1
    hasHitLeft: bool = bounceLedStartPos.x == -1 and bounceDirection == -1 
    if(hasHitRight or hasHitLeft):
        bounceDirection *= -1
        bounceLedStartPos.x = bounceLed[0].x + bounceDirection
    for x in range(ledBounceLength[ledBounceLengthTracker]):
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
        # if(speedChanges[speedTracker] == gridHeight - bounceLed[0].y):
        # if(not speedChanges.index(bounceLed[0].y) == -1):
        if(speedChanges.count(gridHeight - bounceLed[0].y) == 1):
            speedTracker += 1
        if(ledBounceChanges.count(gridHeight - int(bounceLed[0].y)) == 1):
            ledBounceLengthTracker += 1
        if(bounceLedStartPos.y < 0 or not isStacked):
            running = False
            continue

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    # set on led from frame count
    frameCount += 1
    if(frameCount % (framesPerMove * speed[speedTracker]) == 0):
        bounceLeds()        

    displayLeds(bounceLed + onLed)

    screen.blit(minorPrize, minorPrizePos)
    screen.blit(majorPrize, majorPrizePos)
    screen.blit(gameName, gameNamePos)

    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(frameRate)  # limits FPS to 60

