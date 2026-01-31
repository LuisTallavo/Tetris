import pygame
import asyncio
from src.shape import Shape
from src.gameboard import Gameboard
from src.gameboard import gameboardheight

WHITE = (255,255,255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (180, 60, 60)

menu_button = pygame.Rect(400, 10, 80, 30)
quit_button = pygame.Rect(490, 10, 80, 30)

# Global variables
screen = None
myfont = None
HSfont = None
done = False
started = False
game_ended = False
delay = 0
name = ""
slowtimedelay = 0
namelist = [0 for y in range(5)]
scorelist = [0 for y in range(5)]
titlescreen = None
shape = None
nextshape = None
gameboard = None
event = None

def load_highscores():
    global namelist, scorelist
    try:
        HSfile = open("Highscores.txt", "r")
        for i in range(5):
            namelist[i] = HSfile.readline().rstrip('\n')
        for i in range(5):
            scorelist[i] = HSfile.readline().rstrip('\n')
        HSfile.close()
    except:
        for i in range(5):
            namelist[i] = "---"
            scorelist[i] = "0"

def go_to_menu():
    global started, name, shape, nextshape, gameboard, slowtimedelay, delay
    checkHighScores()
    name = ""
    started = False
    delay = 0
    gameboard = Gameboard(WHITE, 25)
    slowtimedelay = 0
    shape = Shape()
    nextshape = Shape()

def keycheck():
    global started, name, shape, nextshape, gameboard, slowtimedelay
    if event.key == pygame.K_LEFT:
        shape.moveLeft()
    elif event.key == pygame.K_RIGHT:
        shape.moveRight()
    elif event.key == pygame.K_UP:
        shape.rotateCW()
    elif event.key == pygame.K_d:
        shape.moveDown()
    elif event.key == pygame.K_DOWN:
        shape.rotateCCW()
    elif event.key == pygame.K_SPACE:
        gameboard.score += (gameboardheight-shape.blockList[0].gridYpos)
        shape.drop()
    elif event.key == pygame.K_t and gameboard.numslowtime > 0:
        gameboard.numslowtime -= 1
        gameboard.slowtimeon = True
    elif event.key == pygame.K_s and gameboard.numswap > 0:
        gameboard.numswap -= 1
        gameboard.swapshape = True

def drawscreen():
    screen.fill(BLACK)
    shape.draw(screen)
    gameboard.draw(screen)
    nextshape.drawnextshape(screen)
    scoretext = myfont.render("Score: " + str(gameboard.score), 1, WHITE)
    screen.blit(scoretext, (400,400))
    linestext = myfont.render("Lines: " + str(gameboard.numlines), 1, WHITE)
    screen.blit(linestext, (400,350))
    leveltext = myfont.render("Level: " + str(gameboard.level), 1, WHITE)
    screen.blit(leveltext, (400,300))
    poweruptext = myfont.render("Power Ups: ", 1, WHITE)
    screen.blit(poweruptext, (50,525))
    numslowtimetext = myfont.render(" x" + str(gameboard.numslowtime), 1, WHITE)
    screen.blit(numslowtimetext, (310, 525))
    slowtime_image = pygame.image.load("assets/clock.png")
    screen.blit(slowtime_image, (250, 515))
    numswaptext = myfont.render(" x" + str(gameboard.numswap), 1, WHITE)
    screen.blit(numswaptext, (435, 525))
    swap_image = pygame.image.load("assets/swap.png")
    screen.blit(swap_image, (375,515))
    for i in range(5):
        hsnametext = HSfont.render(str(namelist[i]),1, WHITE)
        hsscoretext = HSfont.render(str(scorelist[i]), 1, WHITE)
        screen.blit(hsnametext, (580, i*25 + 125))
        screen.blit(hsscoretext, (700, i*25 + 125))
    nextshapetext = myfont.render("Next: ", 1, WHITE)
    screen.blit(nextshapetext, (400,50))
    pygame.draw.rect(screen,WHITE,[400,100,6*shape.blockList[0].size,6*shape.blockList[0].size], 1)
    highscoretext = myfont.render("High Scores", 1, WHITE)
    screen.blit(highscoretext, (575, 50))
    pygame.draw.rect(screen, WHITE, [575, 100, 200, 400], 1)
    playernametext = myfont.render("Player: " + name, 1, WHITE)
    screen.blit(playernametext, (515, 525))
    pygame.draw.rect(screen, GRAY, menu_button, border_radius=5)
    pygame.draw.rect(screen, RED, quit_button, border_radius=5)
    menubtntext = HSfont.render("Home", 1, WHITE)
    quitbtntext = HSfont.render("Quit", 1, WHITE)
    menubtntext_rect = menubtntext.get_rect(center=menu_button.center)
    quitbtntext_rect = quitbtntext.get_rect(center=quit_button.center)
    screen.blit(menubtntext, menubtntext_rect)
    screen.blit(quitbtntext, quitbtntext_rect)
    pygame.display.flip()

def draw_end_screen():
    screen.fill(BLACK)
    endtext = myfont.render("Thanks for playing!", 1, WHITE)
    endtext_rect = endtext.get_rect(center=(400, 270))
    screen.blit(endtext, endtext_rect)
    subtext = HSfont.render("You can close this tab now.", 1, GRAY)
    subtext_rect = subtext.get_rect(center=(400, 320))
    screen.blit(subtext, subtext_rect)
    pygame.display.flip()

def checkHighScores():
    newhighscore = False
    tempnamelist = [0 for y in range(5)]
    tempscorelist = [0 for y in range(5)]
    for i in range(5):
        if gameboard.score > int(scorelist[i]) and newhighscore == False:
            newhighscore = True
            tempscorelist[i] = gameboard.score
            tempnamelist[i] = name
        elif newhighscore == True:
            tempscorelist[i] = scorelist[i-1]
            tempnamelist[i] = namelist[i-1]
        else:
            tempscorelist[i] = scorelist[i]
            tempnamelist[i] = namelist[i]

    for i in range(5):
        scorelist[i] = tempscorelist[i]
        namelist[i] = tempnamelist[i]

    try:
        HSfile = open("Highscores.txt", "w")
        for i in range(5):
            HSfile.write(str(namelist[i]) + '\n')
        for i in range(5):
            HSfile.write(str(scorelist[i]) + '\n')
        HSfile.close()
    except:
        pass

def resetHighScores():
    global namelist, scorelist
    for i in range(5):
        namelist[i] = "---"
        scorelist[i] = "0"
    try:
        HSfile = open("Highscores.txt", "w")
        for i in range(5):
            HSfile.write(namelist[i] + '\n')
        for i in range(5):
            HSfile.write(str(scorelist[i]) + '\n')
        HSfile.close()
    except:
        pass

async def main():
    global screen, myfont, HSfont, done, started, game_ended, delay, name, slowtimedelay
    global namelist, scorelist, titlescreen, shape, nextshape, gameboard, event

    pygame.init()
    pygame.mixer.init()
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    myfont = pygame.font.Font('freesansbold.ttf', 30)
    HSfont = pygame.font.Font('freesansbold.ttf', 20)

    try:
        pygame.mixer.music.load('assets/AvalancheBGM.wav')
        pygame.mixer.music.play(-1)
    except:
        pass

    load_highscores()

    titlescreen = pygame.image.load("assets/Backdrop.png")
    titlescreen = pygame.transform.scale(titlescreen, (950, 750))

    shape = Shape()
    nextshape = Shape()
    gameboard = Gameboard(WHITE, shape.blockList[0].size)

    reset_button = pygame.Rect(250, 400, 150, 30)
    title_quit_button = pygame.Rect(410, 400, 80, 30)

    while not done:
        # Title screen loop
        while not started and not done:
            screen.blit(titlescreen, (-80, -175))
            enterednametext = myfont.render("Please Type in Your Name", 1, WHITE)
            nametext = myfont.render(name, 1, WHITE)
            screen.blit(enterednametext, (200,200))
            screen.blit(nametext, (300,250))
            pygame.draw.rect(screen, GRAY, reset_button, border_radius=5)
            pygame.draw.rect(screen, RED, title_quit_button, border_radius=5)
            resetbtntext = HSfont.render("Reset Scores", 1, WHITE)
            quitbtntext = HSfont.render("Quit", 1, WHITE)
            resetbtntext_rect = resetbtntext.get_rect(center=reset_button.center)
            quitbtntext_rect = quitbtntext.get_rect(center=title_quit_button.center)
            screen.blit(resetbtntext, resetbtntext_rect)
            screen.blit(quitbtntext, quitbtntext_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    game_ended = True
                    started = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_button.collidepoint(event.pos):
                        resetHighScores()
                    elif title_quit_button.collidepoint(event.pos):
                        done = True
                        game_ended = True
                        started = True
                if event.type == pygame.KEYDOWN:
                    if event.key >= 33 and event.key <= 126 and len(name) < 10:
                        name = name + chr(event.key)
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    if event.key == pygame.K_RETURN:
                        if name == "":
                            name = "Player1"
                        started = True

            await asyncio.sleep(0)

        # Game loop
        while started and not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    game_ended = True
                if event.type == pygame.KEYDOWN:
                    keycheck()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_button.collidepoint(event.pos):
                        go_to_menu()
                    elif quit_button.collidepoint(event.pos):
                        done = True
                        game_ended = True

            delay += 1
            if delay >= 10:
                delay = 0
                shape.falling()
            if gameboard.slowtimeon:
                slowtimedelay += 1
                if slowtimedelay > 50:
                    slowtimedelay = 0
                    gameboard.slowtimeon = False
            if gameboard.swapshape:
                shape = nextshape
                nextshape = Shape()
                gameboard.swapshape = False
            if shape.active == False:
                gameboard.clearFullRows()
                shape = nextshape
                nextshape = Shape()
            if gameboard.checkloss():
                checkHighScores()
                gameboard = Gameboard(WHITE, shape.blockList[0].size)
                slowtimedelay = 0
                shape = Shape()
                nextshape = Shape()
            drawscreen()

            sleep_time = 0.11 - gameboard.level * 0.01 + gameboard.slowtimeon * 0.1
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            else:
                await asyncio.sleep(0.01)

    # Show end screen when quitting
    if game_ended:
        pygame.mixer.music.stop()
        draw_end_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            await asyncio.sleep(0.1)

    pygame.quit()

asyncio.run(main())
