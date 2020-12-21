import pygame
import math


pygame.init()

screen = pygame.display.set_mode((800,600))


pygame.display.set_caption("Sodoku Player")
icon = pygame.image.load("sudoku.png")
pygame.display.set_icon(icon) 

#background = pygame.image.load("background.jpg")

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

def score():
    score = font.render("Score: " + str(score_value), True, (0,0,0))
    screen.blit(score, (textX, textY))

#player
playerImg = pygame.image.load("penis.png")
playerX = 300
playerY = 500
d_playerX = 0

def player(x,y):
    screen.blit(playerImg, (x, y))

#enemy
enemyImg = pygame.image.load("buttocks.png")
enemyX = []
enemyY = []
alive = []
d_enemyX = 0.05
num_of_enemies = 18

for i in range(num_of_enemies):
    alive.append(True)
    enemyX.append(i%6*100 + 10)
    enemyY.append(int(i/6)*100)
    

def enemy(x,y):
    screen.blit(enemyImg, (x, y))

#bullet
bulletImg = pygame.image.load("drop.png")
bulletX = 0
bulletY = playerY-16
d_bulletY = -0.5
bullet_state = "READY"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "FIRE"
    screen.blit(bulletImg, (x+24, y+16))

def isCollision(i, bulletX, bulletY):
    x = enemyX[i]
    y = enemyY[i]
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip((x, y), (bulletX, bulletY))]))
    if distance < 27:
        return True
    else:
        return False
        


#Game Loop
running = True
while running:
    screen.fill((255,255,255))
    #screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                d_playerX += -0.2
            if event.key == pygame.K_RIGHT:
                d_playerX += 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state is "READY":
                    bullet_state = "FIRE"
                    bulletX = playerX
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                d_playerX -= -0.2
            if event.key == pygame.K_RIGHT:
                d_playerX -= 0.2

    if playerX <=0:
        playerX=0
    elif playerX >=736:
        playerX=736
    
    for i in range(num_of_enemies):
        if enemyX[i] <=0:
            d_enemyX=0.05
            for j in range(num_of_enemies):
                enemyY[j]+=10
        elif enemyX[i] >=736:
            d_enemyX=-0.05
            for j in range(num_of_enemies):
                enemyY[j]+=10
        
        if alive[i]:

            if isCollision(i, bulletX, bulletY):
                bulletY = playerY - 16
                bullet_state = "READY"
                alive[i]=False       
                score_value += 1
                print(score)

       
            enemyX[i] += d_enemyX
            enemy(enemyX[i], enemyY[i])

   
        
    if bullet_state is "FIRE":
        fire_bullet(bulletX, bulletY)
        bulletY += d_bulletY

        if bulletY <= 0:
            bullet_state = "READY"
            bulletY = playerY-16 


    playerX += d_playerX
   
    player(playerX, playerY)
    score()
    
    pygame.display.update()
