import pygame
from pygame.mixer import pause
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sodoku

import numpy as np
import time

pygame.init()
GAMEOVERSCREEN = True
#Colours
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (200,200,200)
YELLOW = (255, 255, 153)

#Screen
cell_size = 60
screen = pygame.display.set_mode((9*cell_size,10*cell_size))

#initialise board
board = sodoku.init_arr()
board_copy = np.copy(board)

gameover = False
simulated = False

TOGGLECTRL = False

pygame.display.set_caption("Sodoku Player")
icon = pygame.image.load("dep/sudoku.png")
pygame.display.set_icon(icon)

def displayNum(num, r, c, colour):
    num_font = pygame.font.Font('freesansbold.ttf', 40)
    static_num_dsp = num_font.render(str(num), True, colour)
    screen.blit(static_num_dsp, ((c+0.25)*cell_size, (r+0.25)*cell_size))

def highlightCell(coord, COL):
    xpos = coord[0]*cell_size
    ypos = coord[1]*cell_size
    pygame.draw.rect(screen,COL,(xpos, ypos, cell_size, cell_size))


running = True
def backtrackVisualise(screen):
    index = 0
    global board
    global simulated
    simulated = True
    SIMULATE = True
    list = []
    ret = sodoku.runRecursiveHistory(board, list)
   
    while SIMULATE:
        screen.fill(WHITE)
        NEXTSTEP = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIMULATE = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                board = ret
                NEXTSTEP = False
                SIMULATE = False
                
                
        if NEXTSTEP:
            if len(list) >= index-1:
                string = list[index]
                index += 1
            
                act = string[0]
                num = int(string[1])
                posr = int(string[2])
                posc = int(string[3])

                board[posr][posc] = num
            else:
                SIMULATE = False



        drawBoard(screen)
    
        pygame.display.update()
    
    


#ghost entries
ghost = []
    
def init_ghost():
    global ghost
    for r in range(9):
        row = []
        for c in range(9):
            row.append([0,0,0,0,0,0,0,0,0])
        ghost.append(row)
init_ghost()

badEntry = []
    
def init_badEntry():
    global badEntry
    for r in range(9):
        row = []
        for c in range(9):
            row.append(0)
        badEntry.append(row)
init_badEntry()

def ghostEntry():

    for r in range(9):
        for c in range(9):
            for v in ghost[r][c]:
                if v != 0:

                    c_big = c*cell_size + ((v-1)%3)*cell_size/3
                    r_big = r*cell_size + (int((v-1)/3))*cell_size/3

                    num_font = pygame.font.Font('freesansbold.ttf', 20)
                    ghost_num_dsp = num_font.render(str(v), True, (100,100,100))
                    screen.blit(ghost_num_dsp, (c_big+3, r_big+3))
#PAUSE SCREEN

def pauseScreen(screen):
    PAUSED = True
    global GAMEOVERSCREEN
    global running
    while PAUSED:

        drawBoard(screen)

       
        pygame.draw.rect(screen,BLACK,(150, 150, 240, 235))
        #TOP - RETURN
        RETURN_BOX = pygame.Rect((152, 152, 236, 57))
        pygame.draw.rect(screen,WHITE, RETURN_BOX)       
        num_font = pygame.font.Font('freesansbold.ttf', 24)
        static_num_dsp = num_font.render("Return (esc)", True, (0,0,0))
        screen.blit(static_num_dsp, (210, 170))
        #MIDDLE - RESET
        RESET_BOX = pygame.Rect((152, 211, 236, 56)) 
        pygame.draw.rect(screen,WHITE, RESET_BOX)
        num_font = pygame.font.Font('freesansbold.ttf', 24)
        static_num_dsp = num_font.render("Reset Game", True, (0,0,0))
        screen.blit(static_num_dsp, (210, 227))
        #MIDDLE - NEW
        NEW_BOX = pygame.Rect((152, 269, 236, 56)) 
        pygame.draw.rect(screen,WHITE,NEW_BOX)
        num_font = pygame.font.Font('freesansbold.ttf', 24)
        static_num_dsp = num_font.render("New Game", True, (0,0,0))
        screen.blit(static_num_dsp, (210, 283))

        #QUIT
        QUIT_BOX = pygame.Rect((152, 327, 236, 56)) 
        pygame.draw.rect(screen,WHITE,QUIT_BOX)
        num_font = pygame.font.Font('freesansbold.ttf', 24)
        static_num_dsp = num_font.render("QUIT", True, (0,0,0))
        screen.blit(static_num_dsp, (210, 339))

        global board
        global ghost
        global board_copy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PAUSED, running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                x = mouse_pos[0]
                y = mouse_pos[1]
                mouse = pygame.Rect(x, y, 0,0) 
                if RETURN_BOX.collidepoint(x,y):
                    PAUSED = False
                if NEW_BOX.collidepoint(x,y):
                    
                    board = sodoku.init_arr()
                    board_copy = np.copy(board)
                    ghost = []
                    GAMEOVERSCREEN = False
                    init_ghost()
                    PAUSED = False
                if QUIT_BOX.collidepoint(x,y):
                    PAUSED = False
                    running = False
                    
                    GAMEOVERSCREEN = False
                if RESET_BOX.collidepoint(x,y):
                    PAUSED = False
                    board = np.copy(board_copy)
                    ghost = []
                    init_ghost()
                    GAMEOVERSCREEN = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                PAUSED = False


        pygame.display.update()

def drawBoard(screen):
    DULLRED = (200,200,255)
    for r in range(9):
        for c in range(9):
            if badEntry[r][c] != 0:
                for r_2 in range(9):
                    for c_2 in range(9):
                        if board[r_2][c_2] == badEntry[r][c]:
                            highlightCell((c_2, r_2), DULLRED)

    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:     
                displayNum(board[r][c], r, c, (0,0,0))
            if badEntry[r][c] != 0:  
                    displayNum(badEntry[r][c], r, c, (255,0,0)) 
    

    ghostEntry()

    for r in range(9):  
        thickness = 1  
        if r%3 == 0:
            thickness = 2  
        pygame.draw.line(screen,BLACK,(r*cell_size, 0), (r*cell_size, 9*cell_size),thickness)
    for c in range(10): 
        thickness = 1  
        if c%3 == 0:
            thickness = 2       
        pygame.draw.line(screen,BLACK,(0, c*cell_size), (9*cell_size, c*cell_size),thickness)


def bottomText(screen):
    num_font = pygame.font.Font('freesansbold.ttf', 16)
    #Space     
    static_num_dsp = num_font.render("Space: start solve (press again to skip)", True, (0,0,0))
    screen.blit(static_num_dsp, (0, 550))

    #GHOST    
    static_num_dsp = num_font.render("Shift + num: ghost entry", True, (0,0,0))
    screen.blit(static_num_dsp, (350, 550))

    #PAUSE
    static_num_dsp = num_font.render("Esc: open menu", True, (0,0,0))
    screen.blit(static_num_dsp, (0, 580))

    #BACKSPACE
    static_num_dsp = num_font.render("Backspace: erase entry", True, (0,0,0))
    screen.blit(static_num_dsp, (350, 580))

def printClock(time, screen):
    #print box
    TIME_BOX = pygame.Rect((210, 570, 120, 30)) 
    pygame.draw.rect(screen,BLACK,TIME_BOX)

    #print time
    num_font = pygame.font.Font('freesansbold.ttf', 20)
    static_num_dsp = num_font.render(str(time/1000), True, WHITE)
    screen.blit(static_num_dsp, (250, 574))



#Game Loop
highlightcell = (-1,-1)
oldcell = (-1,-1)
numbers = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9 )
clock = pygame.time.Clock()
passed_time = 0
timer_started = False
while running:
    passed_time += clock.get_time()
    print(passed_time)
    screen.fill(WHITE)    

    for event in pygame.event.get():
        #close game
        if event.type == pygame.QUIT:
            running = False
        #click for L and R mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1,3):
            mouse_pos = pygame.mouse.get_pos()
            
            
            oldcell = highlightcell
            highlightcell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
            if highlightcell[0] > 8 or highlightcell[1] > 8:
                highlightcell = (-1,-1)
            
            print(pygame.mouse.get_pressed())
        if event.type == pygame.KEYDOWN:
            c = int(highlightcell[0])
            r = int(highlightcell[1])
           
            # pause game
            if event.key == pygame.K_ESCAPE:
                pauseScreen(screen)
            
            #input ghost entry
            if (event.key in numbers or event.key == pygame.K_BACKSPACE) and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                if event.key == pygame.K_BACKSPACE:
                    value = 0
                else:
                    value = int(pygame.key.name(event.key))

                print("CTRL " + str(value))
                if value not in ghost[r][c]:
                    ghost[r][c][value-1]=value
                else:
                    ghost[r][c][value-1] = 0

            #input answer numbers
            elif event.key in numbers:
                value = int(pygame.key.name(event.key))
                if board_copy[r][c] == 0:
                    if sodoku.addEntry(board, r, c, value):
                        
                        ghost[r][c] = [0,0,0,0,0,0,0,0,0]
                        badEntry[r][c] = 0
                    elif board[r][c]!=value:
                        if badEntry[r][c]==value:
                            value = 0
                        badEntry[r][c] = value                   

                print(str(value))

            #run backtracking algorithm visualisation animation
            elif event.key == pygame.K_SPACE:                
                backtrackVisualise(screen) 
                print("Space")
            #Backspace if it is a writable cell
            elif event.key == pygame.K_BACKSPACE:
                if board_copy[r][c] == 0:
                    board[r][c] = 0
                 
    if oldcell != highlightcell:
        highlightCell(oldcell, WHITE)
        highlightCell(highlightcell, YELLOW)
    else:
        highlightcell=(1000,1000)
        highlightCell(oldcell, WHITE)
        highlightCell(highlightcell, YELLOW)

    drawBoard(screen)  
    bottomText(screen)
    printClock(passed_time, screen)
    clock.tick(30)
    pygame.display.update()

    
    if sodoku.nextBlank(board) is None:
   
        while GAMEOVERSCREEN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GAMEOVERSCREEN = False                  
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pauseScreen(screen)
                    print("jere")
            pygame.draw.rect(screen,BLACK,(0, 540, 540, 60))
            pygame.draw.rect(screen,WHITE,(2, 542, 536, 66))
            num_font = pygame.font.Font('freesansbold.ttf', 40)
           
            if not simulated:
                static_num_dsp = num_font.render("COMPUTER WINS!", True, (0,0,0))
                screen.blit(static_num_dsp, (105, 550))
            else:
                static_num_dsp = num_font.render("YOU WIN!    " + str(passed_time/1000) + "s", True, (0,0,0))
                screen.blit(static_num_dsp, (80, 550))
            
            
            pygame.display.update() 