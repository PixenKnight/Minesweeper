import pygame
import time
from random import randint

pygame.init()

gaming = True
reset = False

mTiles = 99
wTiles = 30
hTiles = 16

width = wTiles * 32
height = hTiles * 32
fps = 10
sqSize = 32

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
timeStart = time.time()
timeElapsed = 0.01

path = "Assets\\Images\\"

bgTile = pygame.transform.scale(pygame.image.load(f"{path}empty.png"), (sqSize, sqSize))
urTile = pygame.transform.scale(pygame.image.load(f"{path}unrevealed.png"), (sqSize, sqSize))
flTile = pygame.transform.scale(pygame.image.load(f"{path}flag.png"), (sqSize, sqSize))
ifTile = pygame.transform.scale(pygame.image.load(f"{path}incFlag.png"), (sqSize, sqSize))
miTile = pygame.transform.scale(pygame.image.load(f"{path}mine.png"), (sqSize, sqSize))
mrTile = pygame.transform.scale(pygame.image.load(f"{path}mineRed.png"), (sqSize, sqSize))
onTile = pygame.transform.scale(pygame.image.load(f"{path}num1.png"), (sqSize, sqSize))
twTile = pygame.transform.scale(pygame.image.load(f"{path}num2.png"), (sqSize, sqSize))
thTile = pygame.transform.scale(pygame.image.load(f"{path}num3.png"), (sqSize, sqSize))
foTile = pygame.transform.scale(pygame.image.load(f"{path}num4.png"), (sqSize, sqSize))
fiTile = pygame.transform.scale(pygame.image.load(f"{path}num5.png"), (sqSize, sqSize))
siTile = pygame.transform.scale(pygame.image.load(f"{path}num6.png"), (sqSize, sqSize))
seTile = pygame.transform.scale(pygame.image.load(f"{path}num7.png"), (sqSize, sqSize))
eiTile = pygame.transform.scale(pygame.image.load(f"{path}num8.png"), (sqSize, sqSize))

tileNumbers = [onTile, twTile, thTile, foTile, fiTile, siTile, seTile, eiTile]

board = []
tiles = pygame.sprite.Group()
minesGroup = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, value):
        pygame.sprite.Sprite.__init__(self)
        self.image = urTile
        self.rect = pygame.Rect((0, 0), (sqSize - 1, sqSize - 1))
        self.rect.x = x
        self.rect.y = y
        self.value = value
        self.flagged = False
        self.clicked = False
        self.surrounding = 0

    def flag(self):
        if not self.clicked:
            if not self.flagged:
                self.flagged = True
                self.image = flTile
            else:
                self.flagged = False
                self.image = urTile

    def click(self, sweeps, mines, x, y, clickMore=True):
        if not self.flagged and not self.clicked:
            self.clicked = True
            if self.value == "x":
                for m in mines:
                    m.reveal()
                self.image = mrTile
                return True
            else:
                if self.value == 0:
                    self.image = bgTile
                    for tY in range((y - 1), (y + 2)):
                        for tX in range((x - 1), (x + 2)):
                            if (tY != -1) and (tX != -1) and (tY != len(sweeps)) and (tX != len(sweeps[tY])):
                                if sweeps[tY][tX].value != "x":
                                    sweeps[tY][tX].click(sweeps, mines, tX, tY)
                else:
                    self.image = tileNumbers[self.value - 1]
        elif self.clicked and not self.flagged and self.value > 0 and clickMore == False:
            self.surrounding = 0
            for tY in range((y - 1), (y + 2)):
                for tX in range((x - 1), (x + 2)):
                    if (tY != -1) and (tX != -1) and (tY != len(sweeps)) and (tX != len(sweeps[tY])):
                        if sweeps[tY][tX].flagged == True:
                            self.surrounding += 1
            if self.surrounding == self.value:
                for tY in range((y - 1), (y + 2)):
                    for tX in range((x - 1), (x + 2)):
                        if (tY != -1) and (tX != -1) and (tY != len(sweeps)) and (tX != len(sweeps[tY])):
                            temperMine = sweeps[tY][tX].click(sweeps, mines, tX, tY)
                            if temperMine:
                                return True

    def reveal(self):
        if not self.flagged:
            self.image = miTile


def boardCreate(w, h, mines):
    # Creation of empty board
    for y in range(h):
        tempX = []
        for x in range(w):
            tempTile = Tile(x * sqSize, y * sqSize, 0)
            tiles.add(tempTile)
            tempX.append(tempTile)
        board.append(tempX)

    # Mine placement
    m = mines
    while m != 0:
        x = randint(0, w - 1)
        y = randint(0, h - 1)
        if board[y][x].value != "x":
            board[y][x].value = "x"
            minesGroup.add(board[y][x])
            m -= 1

    # Calculates numbers for each tile according to adjacent mines
    for y1 in range(h):
        for x1 in range(w):
            for y2 in range((y1 - 1), (y1 + 2)):
                for x2 in range((x1 - 1), (x1 + 2)):
                    if (y2 != -1) and (x2 != -1) and (y2 != h) and (x2 != w):
                        if (board[y2][x2].value == "x") and (board[y1][x1].value != "x"):
                            board[y1][x1].value += 1

def frame():
    tiles.draw(screen)
    pygame.display.update()
    clock.tick(fps)


while True:

    board = []
    boardCreate(wTiles, hTiles, mTiles)
    gaming = True

    while gaming:

        c = -1
        d = -1
        a = -1
        b = -1

        # Quit and mouse click check
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    c, d = event.pos
                elif event.button == 3:
                    a, b = event.pos

        # Click check
        for tY in range(len(board)):
            for tX in range(len(board[tY])):
                if board[tY][tX].rect.collidepoint(c, d):
                    tempMine = board[tY][tX].click(board, minesGroup, tX, tY, False)
                    if tempMine:
                        frame()
                        time.sleep(3)
                        gaming = False

                elif board[tY][tX].rect.collidepoint(a, b):
                    board[tY][tX].flag()

        frame()

    while not reset:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset = True
                elif event.key == pygame.K_q:
                    quit()
