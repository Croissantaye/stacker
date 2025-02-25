import pygame as pg

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

onLedStartPos: pg.Vector2 = pg.Vector2(0, gridHeight - 1)
onLed: list[pg.Vector2] = [pg.Vector2(onLedStartPos.x, onLedStartPos.y)]

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
    hasHitRight: bool = onLedStartPos.x + ledCount - 1 == gridWidth and bounceDirection == 1
    hasHitLeft: bool = onLedStartPos.x == -1 and bounceDirection == -1 
    if(hasHitRight or hasHitLeft):
        bounceDirection *= -1
        onLedStartPos.x = onLed[0].x + bounceDirection
    for x in range(ledCount):
        if(len(onLed) < x + 1):
            onLed.append(pg.Vector2(onLed[x - 1].x + 1, onLed[x - 1].y))
        onLed[x].x = onLedStartPos.x + x
    onLedStartPos.x += bounceDirection

createLedSquares()

while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    # set on led from frame count
    frameCount += 1
    if(frameCount % framesPerMove == 0):
        bounceLeds()        

    displayLeds(onLed)

    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(frameRate)  # limits FPS to 60

