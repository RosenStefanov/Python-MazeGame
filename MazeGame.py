import copy
import os
import pygame
import random
import sys

from pygame.locals import *

WINWIDTH = 800
WINHEIGHT = 600
GAMEWIDTH = 1200
GAMEHEIGHT = 800
TILEWIDTH = 50
TILEHEIGHT = 50
HALF_GAMEWIDTH = int(GAMEWIDTH / 2)
HALF_GAMEHEIGHT = int(GAMEHEIGHT / 2)
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
MAPWIDTH = int(GAMEWIDTH / TILEWIDTH)
MAPHEIGHT = int(GAMEHEIGHT / TILEHEIGHT)
BRIGHTGREEN = (9, 217, 99)
BLACK = (0, 0, 0)
BGCOLOR = BRIGHTGREEN
TEXTCOLOR = BLACK
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global SCREEN, FONT, CLOCK, FLOORTILE, PLAYER, SHROOM, ENEMY
    pygame.init()
    SCREEN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption("MAZE")
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.Font('freesansbold.ttf', 22)
    floorTile = pygame.image.load('assets/floor.png')
    FloorTile = pygame.transform.scale(floorTile, (TILEWIDTH, TILEHEIGHT))
    wall = pygame.image.load('assets/Crate.png')
    Wall = pygame.transform.scale(wall, (TILEWIDTH, TILEHEIGHT))
    player = pygame.image.load('assets/Cactus.png')
    PLAYER = pygame.transform.scale(player, (TILEWIDTH - 10, TILEHEIGHT - 10))
    Shroom = pygame.image.load('assets/Mushroom.png')
    SHROOM = pygame.transform.scale(Shroom, (TILEWIDTH - 20, TILEHEIGHT - 20))
    ScoreSpace = pygame.transform.scale(floorTile, (TILEWIDTH, TILEHEIGHT))
    enemy = pygame.image.load('assets/Bush.png')
    ENEMY = pygame.transform.scale(enemy, (TILEWIDTH, TILEHEIGHT))
    FLOORTILE = {' ': FloorTile,
                 '#': Wall,
                 'S': ScoreSpace}
    startScreen()


def startScreen():
    MOVERATE = 0.15
    FPS = 30
    currentLevelIndex = 0
    topCoord = 130
    instructionText = ['MAZE  GAME!!!!',
                       '               ',
                       'Go to the tresure without dying.',
                       'WASD keys to move.',
                       'ESC to exit.',
                       'Press 1 for EASY mode.',
                       'Press 2 for NORMAL mode.',
                       'Press 3 for HARD mode.']

    SCREEN.fill(BGCOLOR)

    for i in range(len(instructionText)):
        instSurf = FONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height
        SCREEN.blit(instSurf, instRect)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    runGame(currentLevelIndex, MOVERATE, FPS)
                elif event.key == K_2:
                    currentLevelIndex = 1
                    FPS = 40
                    runGame(currentLevelIndex, MOVERATE, FPS)
                elif event.key == K_3:
                    currentLevelIndex = 2
                    FPS = 50
                    runGame(currentLevelIndex, MOVERATE, FPS)
                if event.key == K_ESCAPE:
                    terminate()

        pygame.display.update()
        CLOCK.tick()


def endGameScreen(score):
    SCREEN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    topCoord = 150
    endText = ['GAME OVER!!!',
               '               ',
               'Score: %s' % (score),
               'Press any key to go back to the start!']
    SCREEN.fill(BGCOLOR)

    for i in range(len(endText)):
        instSurf = FONT.render(endText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height
        SCREEN.blit(instSurf, instRect)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                startScreen()

        pygame.display.update()
        CLOCK.tick()


def runGame(levelNum, MOVERATE, FPS):
    pygame.display.set_mode((GAMEWIDTH, GAMEHEIGHT))
    levels = readLevelsFile('levels/gameDifficulty.txt')
    SCORE = 0
    levelObj = levels[levelNum]
    mapObj = removePlayerFromMap(levelObj['mapObj'])
    playerPos = copy.deepcopy(levelObj['startState'])
    enemyPos = copy.deepcopy(levelObj['enemyList'])
    moveUp = False
    moveDown = False
    moveLeft = False
    moveRight = False
    enemyCounter = 0
    shroom = getRandomLocation(levelObj['mapObj'])
    allEnemies = createAllEnemies(enemyPos)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                elif event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key == (K_BACKSPACE):
                    SCREEN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
                    startScreen()
                elif event.key == K_ESCAPE:
                    terminate()
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
                elif event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False

        if enemyCounter < 4:
            enemyCounter += 1
            for enemy in allEnemies:
                if enemy['dir'] == 0:
                    if enemyWallCollision(enemy['x'], enemy['y'] - MOVERATE, mapObj):
                        while enemy['dir'] == 0:
                            enemy['dir'] = random.randint(0, 3)
                    else:
                        enemy['y'] = enemy['y'] - MOVERATE
                elif enemy['dir'] == 2:
                    if enemyWallCollision(enemy['x'], enemy['y'] + MOVERATE, mapObj):
                        while enemy['dir'] == 2:
                            enemy['dir'] = random.randint(0, 3)
                    else:
                        enemy['y'] = enemy['y'] + MOVERATE
                elif enemy['dir'] == 1:
                    if enemyWallCollision(enemy['x'] + MOVERATE, enemy['y'], mapObj):
                        while enemy['dir'] == 1:
                            enemy['dir'] = random.randint(0, 3)
                    else:
                        enemy['x'] = enemy['x'] + MOVERATE
                elif enemy['dir'] == 3:
                    if enemyWallCollision(enemy['x'] - MOVERATE, enemy['y'], mapObj):
                        while enemy['dir'] == 3:
                            enemy['dir'] = random.randint(0, 3)
                    else:
                        enemy['x'] = enemy['x'] - MOVERATE

        elif enemyCounter == 4:
            for enemy in allEnemies:
                newDir = random.randint(0, 3)
                if newDir == 0 & enemy['dir'] != 2:
                    enemy['dir'] = newDir
                elif newDir == 2 & enemy['dir'] != 0:
                    enemy['dir'] = newDir
                elif newDir == 1 & enemy['dir'] != 3:
                    enemy['dir'] = newDir
                elif newDir == 3 & enemy['dir'] != 1:
                    enemy['dir'] = newDir
                if enemy['dir'] == 0:
                    if enemyWallCollision(enemy['x'], enemy['y'], mapObj):
                        enemy['y'] = enemy['y']
                    else:
                        enemy['y'] = enemy['y'] - MOVERATE
                elif enemy['dir'] == 2:
                    if enemyWallCollision(enemy['x'], enemy['y'], mapObj):
                        enemy['y'] = enemy['y']
                    else:
                        enemy['y'] = enemy['y'] + MOVERATE
                elif enemy['dir'] == 1:
                    if enemyWallCollision(enemy['x'], enemy['y'], mapObj):
                        enemy['x'] = enemy['x']
                    else:
                        enemy['x'] = enemy['x'] + MOVERATE
                elif enemy['dir'] == 3:
                    if enemyWallCollision(enemy['x'], enemy['y'], mapObj):
                        enemy['x'] = enemy['x']
                    else:
                        enemy['x'] = enemy['x'] - MOVERATE
            enemyCounter = 0
        if moveLeft:
            playerPos[0] -= MOVERATE
            if wallCollision(playerPos, mapObj):
                playerPos[0] += MOVERATE
        if moveRight:
            playerPos[0] += MOVERATE
            if wallCollision(playerPos, mapObj):
                playerPos[0] -= MOVERATE
        if moveUp:
            playerPos[1] -= MOVERATE
            if wallCollision(playerPos, mapObj):
                playerPos[1] += MOVERATE
        if moveDown:
            playerPos[1] += MOVERATE
            if wallCollision(playerPos, mapObj):
                playerPos[1] -= MOVERATE
        if shroomCollision(shroom, playerPos):
            shroom = getRandomLocation(levelObj['mapObj'])
            SCORE += 1
        if enemyCollision(allEnemies, playerPos):
            endGameScreen(SCORE)
        drawMap(mapObj)
        drawScore(SCORE)
        drawShroom(shroom)
        drawEnemy(allEnemies)
        drawPlayer(playerPos)
        pygame.display.update()
        CLOCK.tick(FPS)


def drawMap(mapObj):
    for x in range(MAPWIDTH):
        for y in range(MAPHEIGHT):
            baseTile = FLOORTILE[mapObj[x][y]]
            spaceRect = pygame.Rect((x * TILEWIDTH, y * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
            SCREEN.blit(baseTile, spaceRect)


def shroomCollision(shroom, playerPos):
    playerRect = pygame.Rect((playerPos[0] * TILEWIDTH, playerPos[1] * TILEHEIGHT, TILEWIDTH - 10, TILEHEIGHT - 10))
    x = shroom[0]
    y = shroom[1]
    shroomRect = pygame.Rect(x * TILEWIDTH, y * TILEHEIGHT, TILEWIDTH - 20, TILEHEIGHT - 20)
    if playerRect.colliderect(shroomRect):
        return True


def enemyCollision(allEnemies, playerPos):
    playerRect = pygame.Rect((playerPos[0] * TILEWIDTH, playerPos[1] * TILEHEIGHT, TILEWIDTH - 10, TILEHEIGHT - 10))
    for x in range(len(allEnemies)):
        enemyRect = pygame.Rect(
            (allEnemies[x]['x'] * TILEWIDTH, allEnemies[x]['y'] * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
        if playerRect.colliderect(enemyRect):
            return True


def wallCollision(playerPos, mapObj):
    playerRect = pygame.Rect((playerPos[0] * TILEWIDTH, playerPos[1] * TILEHEIGHT, TILEWIDTH - 10, TILEHEIGHT - 10))
    for x in range(MAPWIDTH):
        for y in range(MAPHEIGHT):
            baseTile = FLOORTILE[mapObj[x][y]]
            if baseTile == FLOORTILE['#']:
                wallRect = pygame.Rect((x * TILEWIDTH, y * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
            if playerRect.colliderect(wallRect):
                return True


def makeNewEnemy(enemyx, enemyy):
    newEnemy = {}
    newEnemy['x'], newEnemy['y'] = enemyx, enemyy
    newEnemy['dir'] = random.randint(0, 3)
    return newEnemy


def createAllEnemies(enemyPos):
    allEnemies = []
    for x in enemyPos:
        allEnemies.append(makeNewEnemy(x[0], x[1]))
    return allEnemies


def enemyWallCollision(enemyx, enemyy, mapObj):
    enemyRect = pygame.Rect((enemyx * TILEWIDTH, enemyy * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
    for x in range(MAPWIDTH):
        for y in range(MAPHEIGHT):
            baseTile = FLOORTILE[mapObj[x][y]]
            if baseTile == FLOORTILE['#']:
                wallRect = pygame.Rect((x * TILEWIDTH, y * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
            if enemyRect.colliderect(wallRect):
                return True


def drawScore(score):
    scoreSurf = FONT.render('Score: %s' % (score), True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (GAMEWIDTH - 190, 12)
    SCREEN.blit(scoreSurf, scoreRect)


def drawEnemy(allEnemies):
    for x in range(len(allEnemies)):
        enemyx = allEnemies[x]['x']
        enemyy = allEnemies[x]['y']
        enemyRect = pygame.Rect((enemyx * TILEWIDTH, enemyy * TILEHEIGHT, TILEWIDTH, TILEHEIGHT))
        SCREEN.blit(ENEMY, enemyRect)


def drawPlayer(playerPos):
    playerRect = pygame.Rect((playerPos[0] * TILEWIDTH, playerPos[1] * TILEHEIGHT, TILEWIDTH - 10, TILEHEIGHT - 10))
    SCREEN.blit(PLAYER, playerRect)


def removePlayerFromMap(mapObj):
    mapObjCopy = copy.deepcopy(mapObj)
    for x in range(len(mapObjCopy)):
        for y in range(len(mapObjCopy[0])):
            if mapObjCopy[x][y] in ('@', 'X'):
                mapObjCopy[x][y] = ' '
    return mapObjCopy


def getRandomLocation(levelObj):
    while True:
        randLoc = [random.randint(1, MAPWIDTH - 2), random.randint(1, MAPHEIGHT - 2)]
        if levelObj[randLoc[0]][randLoc[1]] != '#':
            if levelObj[randLoc[0]][randLoc[1]] != '@':
                break
    return randLoc


def drawShroom(shroom):
    x = shroom[0]
    y = shroom[1]
    shroomRect = pygame.Rect((x * TILEWIDTH) + 10, (y * TILEHEIGHT) + 10, TILEWIDTH - 20, TILEHEIGHT - 20)
    SCREEN.blit(SHROOM, shroomRect)


def readLevelsFile(filename):
    assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
    mapFile = open(filename, 'r')
    content = mapFile.readlines() + ['\r\n']
    mapFile.close()
    levels = []
    levelNum = 0
    mapTextLines = []
    mapObj = []
    enemyList = []
    for lineNum in range(len(content)):
        line = content[lineNum].rstrip('\r\n')
        if ';' in line:
            line = line[:line.find(';')]
        if line != '':
            mapTextLines.append(line)
        elif line == '' and len(mapTextLines) > 0:
            for x in range(len(mapTextLines[0])):
                mapObj.append([])
            for y in range(len(mapTextLines)):
                for x in range(24):
                    mapObj[x].append(mapTextLines[y][x])
            startx = None
            starty = None
            for x in range(24):
                for y in range(len(mapObj[x])):
                    if mapObj[x][y] == '@':
                        startx = x
                        starty = y
                    if mapObj[x][y] == 'X':
                        enemy = [x, y]
                        enemyList.append(enemy)
            playerPos = [startx, starty]
            levelObj = {'mapObj': mapObj,
                        'startState': playerPos,
                        'enemyList': enemyList}
            levels.append(levelObj)
            enemyList = []
            mapTextLines = []
            mapObj = []
            gameStateObj = {}
            levelNum += 1
    return levels


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
