from src.block import Block
from src.gameboard import gameboardwidth
from src.gameboard import gameboardheight
import random
from src.gameboard import activeBoardSpot
from src.gameboard import activeBoardColour
import pygame

BLACK = (0,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
TURQUOISE = (0, 206, 209)
ALLCOLOURS = [WHITE, GREEN, RED, BLUE, YELLOW, MAGENTA, TURQUOISE, BLACK]

ZSHAPE = [[(gameboardwidth/2)-1,0],[(gameboardwidth/2)-2,0],[(gameboardwidth/2)-1,1],[(gameboardwidth/2),1]]
SSHAPE = [[(gameboardwidth/2)-1,0],[(gameboardwidth/2),0],[(gameboardwidth/2)-2,1],[(gameboardwidth/2)-1,1]]
LINESHAPE = [[(gameboardwidth/2)-1,0],[(gameboardwidth/2)-2,0],[(gameboardwidth/2),0],[(gameboardwidth/2)+1,0]]
SQUARESHAPE = [[(gameboardwidth/2)-1,0],[(gameboardwidth/2),0],[(gameboardwidth/2),1],[(gameboardwidth/2)-1,1]]
LSHAPE = [[(gameboardwidth/2)-1,1],[(gameboardwidth/2)-1,0],[(gameboardwidth/2)-1,2],[(gameboardwidth/2),2]]
MLSHAPE = [[(gameboardwidth/2),1],[(gameboardwidth/2),0],[(gameboardwidth/2),2],[(gameboardwidth/2)-1,2]]
TSHAPE = [[(gameboardwidth/2)-1,1],[(gameboardwidth/2)-1,0],[(gameboardwidth/2),1],[(gameboardwidth/2)-2,1]]
ALLSHAPES = [ZSHAPE, SSHAPE, LINESHAPE, SQUARESHAPE, LSHAPE, MLSHAPE, TSHAPE]


class Shape():

    def __init__(self):
        self.numblocks = 4
        self.active = True
        randomNum = random.randrange(7)
        self.colour = ALLCOLOURS[randomNum]
        self.shape = ALLSHAPES[randomNum]
        self.blockList = []
        for i in range (self.numblocks):
            self.blockList.append(Block(self.colour, self.shape[i][0],  self.shape[i][1]))

    def draw(self, screen):
        for i in range (self.numblocks):
            self.blockList[i].draw(screen)

    
    def moveLeft(self):
        blocked = False
        for i in range(self.numblocks):
            if self.blockList[i].gridXpos == 0 or activeBoardSpot[self.blockList[i].gridXpos-1][self.blockList[i].gridYpos]:
                 blocked = True
        if blocked == False:
            for i in range(self.numblocks):
                self.blockList[i].gridXpos -= 1

    def moveRight(self):
        blocked = False
        for i in range(self.numblocks):
            if self.blockList[i].gridXpos == gameboardwidth-1 or activeBoardSpot[self.blockList[i].gridXpos+1][self.blockList[i].gridYpos]:
                 blocked = True
        if blocked == False:
            for i in range(self.numblocks):
                self.blockList[i].gridXpos += 1

    def moveDown(self):
        blocked = False
        for i in range(4):
            if self.blockList[i].gridYpos == gameboardheight-1 or activeBoardSpot[self.blockList[i].gridXpos][self.blockList[i].gridYpos+1]:
                blocked = True
        if blocked == False:
            for i in range(4):
                self.blockList[i].gridYpos += 1

    def rotateCW(self):
        if self.shape != SQUARESHAPE:
            canrotate = True
            newBlockX = [0,0,0,0]
            newBlockY = [0,0,0,0]
            for i in range(self.numblocks):
                newBlockX[i] = -(self.blockList[i].gridYpos - self.blockList[0].gridYpos) + self.blockList[0].gridXpos
                newBlockY[i] = (self.blockList[i].gridXpos - self.blockList[0].gridXpos) + self.blockList[0].gridYpos

                if newBlockX[i] < 0 or newBlockX[i] >= (gameboardwidth-1):
                    canrotate = False
                elif newBlockY[i] < 0 or newBlockY[i] >= gameboardheight -1:
                    canrotate = False
                elif activeBoardSpot[newBlockX[i]][newBlockY[i]]:
                    canrotate = False

            if canrotate:
                for i in range(self.numblocks):
                    self.blockList[i].gridXpos = newBlockX[i]
                    self.blockList[i].gridYpos = newBlockY[i]

    def rotateCCW(self):
        if self.shape != SQUARESHAPE:
            canrotate = True
            newBlockX = [0,0,0,0]
            newBlockY = [0,0,0,0]
            for i in range(self.numblocks):
                newBlockX[i] =(self.blockList[i].gridYpos - self.blockList[0].gridYpos) + self.blockList[0].gridXpos
                newBlockY[i] =-(self.blockList[i].gridXpos - self.blockList[0].gridXpos) + self.blockList[0].gridYpos

                if newBlockX[i] < 0 or newBlockX[i] >= (gameboardwidth-1):
                    canrotate = False
                elif newBlockY[i] < 0 or newBlockY[i]>= gameboardheight -1:
                    canrotate = False
                elif activeBoardSpot[newBlockX[i]][newBlockY[i]]:
                    canrotate = False
            if canrotate:
                for i in range(self.numblocks):
                    self.blockList[i].gridXpos = newBlockX[i]
                    self.blockList[i].gridYpos = newBlockY[i]

    def falling(self):
        for i in range(self.numblocks):
            if self.blockList[i].gridYpos == gameboardheight - 1 or activeBoardSpot[self.blockList[i].gridXpos][self.blockList[i].gridYpos + 1]:
                self.hitBottom()
        for i in range(self.numblocks):
            if self.active:
                self.blockList[i].gridYpos += 1

    def hitBottom(self):
        for i in range(self.numblocks):
            activeBoardSpot[self.blockList[i].gridXpos][self.blockList[i].gridYpos] = True
            activeBoardColour[self.blockList[i].gridXpos][self.blockList[i].gridYpos] = self.blockList[i].colour
            self.active = False

    def drop(self):
        while self.active:
            for i in range(self.numblocks):
                if self.blockList[i].gridYpos == gameboardheight - 1 or activeBoardSpot[self.blockList[i].gridXpos][self.blockList[i].gridYpos + 1]:
                    self.hitBottom()
            for i in range(self.numblocks):
                if self.active:
                    self.blockList[i].gridYpos += 1

    def drawnextshape(self, screen):
        for i in range(self.numblocks):
            pygame.draw.rect(screen, self.blockList[i].colour, [self.blockList[i].gridXpos*self.blockList[i].size + 325, self.blockList[i].gridYpos*self.blockList[i].size + 150, self.blockList[i].size - 1, self.blockList[i].size -1], 0)
