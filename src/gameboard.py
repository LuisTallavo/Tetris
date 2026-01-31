import pygame
gameboardwidth = 12
gameboardheight = 20
activeBoardSpot = [[0 for y in range(gameboardheight)] for x in range(gameboardwidth)]
activeBoardColour = [[0 for y in range(gameboardheight)] for x in range(gameboardwidth)]

BLACK = (0,0,0)

pygame.init()
try:
    linesound = pygame.mixer.Sound("assets/clearline.wav")
except:
    linesound = None

class Gameboard():
    def __init__(self,colour,blocksize):
        self.bordercolour = colour
        self.multiplier = blocksize
        self.score = 0
        self.numlines = 0
        self.templeveltracker = 0
        self.level = 1
        self.numslowtime = 0
        self.numswap = 0
        self.swapshape = False
        self.slowtimeon = False
        for i in range(gameboardwidth):
            for j in range (gameboardheight):
                activeBoardSpot[i][j] = False
                activeBoardColour[i][j] = (0,0,0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bordercolour, [0,0,gameboardwidth*self.multiplier, gameboardheight*self.multiplier], 1)

        for i in range(gameboardwidth):
            for j in range(gameboardheight):
                if activeBoardSpot[i][j]:
                    pygame.draw.rect(screen, activeBoardColour[i][j], [i*self.multiplier, j*self.multiplier, self.multiplier-1, self.multiplier -1], 0)

    def checkloss (self):
        for i in range(gameboardwidth):
            if activeBoardSpot[i][0]:
                return True
        return False

    def isCompleteLine (self,rowNum):
        for i in range(gameboardwidth):
            if activeBoardSpot[i][rowNum] == False:
                return False
        return True

    def clearFullRows(self):
        for j in range(gameboardheight):
            if self.isCompleteLine(j):
                if linesound:
                    linesound.play()
                self.score += 100
                self.numlines += 1
                self.templeveltracker += 1
                if self.templeveltracker == 10:
                    self.level +=1
                    self.numslowtime += 1
                    self.numswap += 1
                    self.templeveltracker = 0
                for c in range(j,1,-1):
                    for i in range(gameboardwidth):
                        activeBoardSpot[i][c] = activeBoardSpot[i][c-1]
                        activeBoardColour[i][c] = activeBoardColour[i][c-1]
                for r in range(gameboardwidth):
                    activeBoardSpot[r][0] = False
                    activeBoardColour[r][0] = BLACK
                
