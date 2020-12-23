import pygame
import sodoku
import colour

import numpy as np
import time

pygame.init()

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

gameover = False

TOGGLECTRL = False

pygame.display.set_caption("Sodoku Player")
icon = pygame.image.load("dep/sudoku.png")
pygame.display.set_icon(icon)

def displayNum(num, r, c):
    num_font = pygame.font.Font('freesansbold.ttf', 40)
    static_num_dsp = num_font.render(str(num), True, (0,0,0))
    screen.blit(static_num_dsp, ((c+0.25)*cell_size, (r+0.25)*cell_size))

def highlightCell(coord, COL):
    xpos = coord[0]*cell_size
    ypos = coord[1]*cell_size
    pygame.draw.rect(screen,COL,(xpos, ypos, cell_size, cell_size))


running = True
def backtrackVisualise(board):
    SIMULATE = True
    file = open("new.txt")
    sodoku.runRecursiveHistory(board)
   
    while SIMULATE:
        # time.sleep(0.001)
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIMULATE, running = False

        string = file.readline()
        
        act = string[0]
        num = int(string[1])
        posr = int(string[2])
        posc = int(string[3])

        board[posr][posc] = num


        for r in range(9):
            for c in range(9):
                
                if board[r][c] != 0:
                    displayNum(board[r][c], r, c)   

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
    
        pygame.display.update()
#ghost entries
ghost = []
    

for r in range(9):
    row = []
    for c in range(9):
        row.append([0,0,0,0,0,0,0,0,0])
    ghost.append(row)

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
                
                       
#Game Loop
highlightcell = (-1,-1)
oldcell = (-1,-1)
numbers = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9 )
while running:
    screen.fill(WHITE)

     

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print("Mouse")
            oldcell = highlightcell
            highlightcell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
        if event.type == pygame.KEYDOWN:
            c = int(highlightcell[0])
            r = int(highlightcell[1])
           # print(highlightcell)
            
            if event.key in numbers and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                
                value = int(pygame.key.name(event.key))

                print("CTRL " + str(value))
                if value not in ghost[r][c]:
                    ghost[r][c][value-1]=value#add to ghost entries
                else:
                    ghost[r][c][value-1] = 0

            elif event.key in numbers:
                value = int(pygame.key.name(event.key))
                if sodoku.addEntry(board, r, c, value):
                    ghost[r][c] = [0,0,0,0,0,0,0,0,0] 
                print(str(value))
               
            elif event.key == pygame.K_SPACE:                
               backtrackVisualise(board)  
               print("Space")
                 
    if oldcell != highlightcell:
        highlightCell(oldcell, WHITE)
        highlightCell(highlightcell, YELLOW)
    else:
        highlightcell=(1000,1000)
        highlightCell(oldcell, WHITE)
        highlightCell(highlightcell, YELLOW)
        


    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                displayNum(board[r][c], r, c)   

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

    
        
    pygame.display.update()

    GAMEOVERSCREEN = True
    if sodoku.nextBlank(board) is None:
   
        while GAMEOVERSCREEN:
             for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GAMEOVERSCREEN, running = False
                pygame.draw.rect(screen,BLACK,(0, 540, 540, 60))
                pygame.draw.rect(screen,WHITE,(2, 542, 536, 66))
                num_font = pygame.font.Font('freesansbold.ttf', 40)
                static_num_dsp = num_font.render("YOU WIN!", True, (0,0,0))
                screen.blit(static_num_dsp, (175, 550))
                pygame.display.update() 