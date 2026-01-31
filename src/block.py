import pygame

class Block():

    def __init__(self, colour, gridXpos, gridYpos):
        self.colour = colour
        self.gridXpos = int(gridXpos)
        self.gridYpos = int(gridYpos)
        self.size = 25

    def draw(self,screen):
        pygame.draw.rect(screen, self.colour, [self.gridXpos*self.size, self.gridYpos*self.size, self.size-1, self.size-1], 0)
    
