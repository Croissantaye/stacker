import pygame as pg

# pg setup
pg.init()

gridHeight = 15
gridWidth = 7
squareSize = 30

bottomPadding = 100
sidePadding = 100
squarePadding = 5

screenWidth = gridWidth * (squareSize + squarePadding) + (2 * sidePadding)
screenHeight = gridHeight * (squareSize + squarePadding) + ( 2 * bottomPadding)
screenCenter = pg.Vector2(screenWidth/2, screenWidth/2)

ledSquares: list[pg.Rect] = []

squareOff = 'grey'
squareOn = 'red'

frameRate = 30

screen = pg.display.set_mode((screenWidth, screenHeight))

clock = pg.time.Clock()

running = True

onLed = 0

frameCount = 0

def createLedSquares():
    for y in range(gridHeight):
        for x in range(gridWidth):
            pos = pg.Vector2(sidePadding + (x * squareSize) + (x * squarePadding), bottomPadding + (y * squareSize) + (y * squarePadding))
            led = pg.Rect(pos.x, pos.y, squareSize, squareSize)
            ledSquares.append(led)

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
    # draw LED squares
    for led in range(len(ledSquares)):
        color = squareOff 
        print(led)
        if(led == onLed):
            color = squareOn
        pg.draw.rect(screen, color, ledSquares[led])

    # set on led from frame count
    frameCount += 1
    if(frameCount % 5 == 0):
        onLed += 1
        onLed = onLed % (gridWidth * gridHeight)

    print(onLed)

    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(frameRate)  # limits FPS to 60

