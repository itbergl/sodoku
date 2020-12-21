import pygame
import sodoku
import colour

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


pygame.display.set_caption("Sodoku Player")
icon = pygame.image.load("dep/sudoku.png")
pygame.display.set_icon(icon)

def displayNum(num, r, c):
    num_font = pygame.font.Font('freesansbold.ttf', 40)
    static_num_dsp = num_font.render(str(num), True, (0,0,0))
    screen.blit(static_num_dsp, ((c+0.25)*cell_size, (r+0.25)*cell_size))

def highlightCell(old_coord, new_coord):
    xpos = old_coord[0]*cell_size
    ypos = old_coord[1]*cell_size
    pygame.draw.rect(screen,WHITE,(xpos, ypos, cell_size, cell_size))
    
    xpos = new_coord[0]*cell_size
    ypos = new_coord[1]*cell_size
    pygame.draw.rect(screen,YELLOW,(xpos, ypos, cell_size, cell_size))

#Game Loop
running = True
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
            oldcell = highlightcell
            highlightcell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
        if event.type == pygame.KEYDOWN:
            c = int(highlightcell[0])
            r = int(highlightcell[1])
            print(highlightcell)
            if event.key == pygame.K_SPACE:
                sodoku.recursive(board)
            if event.key == pygame.K_1:              
                sodoku.addEntry(board, r, c, 1)               
            if event.key == pygame.K_2:
                sodoku.addEntry(board, r, c, 2)
            if event.key == pygame.K_3:
                sodoku.addEntry(board, r, c, 3)
            if event.key == pygame.K_4:
                sodoku.addEntry(board, r, c, 4)
            if event.key == pygame.K_5:
                sodoku.addEntry(board, r, c, 5)
            if event.key == pygame.K_6:
                sodoku.addEntry(board, r, c, 6)
            if event.key == pygame.K_7:
                sodoku.addEntry(board, r, c, 7)
            if event.key == pygame.K_8:
                sodoku.addEntry(board, r, c, 8)
            if event.key == pygame.K_9:
                sodoku.addEntry(board, r, c, 9)

    #SHIFT NUM DOES BLANK
    #CLICK TO AUTO FILL
    #NUMBER FILLS IN
    if oldcell != highlightcell:
        highlightCell(oldcell, highlightcell)
    else:
        highlightCell(oldcell, (1000,1000))

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

    GAMEOVERSCREEN = True
    if sodoku.nextBlank(board) is None:
        while GAMEOVERSCREEN:
             for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GAMEOVERSCREEN, running = False
                pygame.draw.rect(screen,BLACK,(100, 100, 340, 340))
                pygame.draw.rect(screen,WHITE,(102, 102, 336, 336))
                num_font = pygame.font.Font('freesansbold.ttf', 40)
                static_num_dsp = num_font.render("YOU WIN!", True, (0,0,0))
                screen.blit(static_num_dsp, (175, 250))
                pygame.display.update() 