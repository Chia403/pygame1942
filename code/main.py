import pygame
from Player import Player
from pathlib import Path
from missile import MyMissile
from enemy import Enemy
import random

pygame.init()

screenHigh = 760
screenWidth = 1000
playground = [screenWidth, screenHigh]
screen = pygame.display.set_mode((screenWidth,screenHigh))
keyCountX = 0
keyCountY = 0
Missiles=[]
enemy = Enemy(playground)
enemies = [enemy]
launchMissile = pygame.USEREVENT + 1
spawnEnemy = pygame.USEREVENT + 2

running = True
fps=120
movingScale = 600 /fps
player = Player(playground=playground, sensitivity=movingScale)
clock = pygame.time.Clock()

parent_path = Path(__file__).parents[1]
image_path = parent_path /'res'
icon_path = image_path / 'airplaneicon.png'

pygame.display.set_caption("1942偽")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((50,50,50))
pygame.time.set_timer(launchMissile, 0)
pygame.time.set_timer(spawnEnemy, 2000)


while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =  False
        
        if event.type == spawnEnemy:
           x = random.randint(0, playground[0] - 100)
           y = random.randint(-150, -50)
           enemies.append(Enemy(playground, xy=(x, y), sensitivity=movingScale))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                keyCountX += 1
                player.to_the_left()
            if event.key == pygame.K_d:
               keyCountX += 1
               player.to_the_right()
            if event.key == pygame.K_s:
                keyCountY += 1
                player.to_the_bottom()
            if event.key == pygame.K_w:
                keyCountY += 1
                player.to_the_top()
            
            if event.key == pygame.K_SPACE:
                m_x = player.x + 20
                m_y = player.y  
                Missiles.append(MyMissile(xy=(m_x,m_y),playground = playground, sensitivity = movingScale))
                m_x = player.x + 80
                Missiles.append(MyMissile(playground,(m_x,m_y),movingScale))
                pygame.time.set_timer(launchMissile,400)

            

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                if  keyCountX == 1:
                    keyCountX = 0
                    player.stop_x()
                else:
                    keyCountX -= 1
            if event.key == pygame.K_s or event.key == pygame.K_w:
                if  keyCountY == 1:
                    keyCountY = 0
                    player.stop_y()
                else:
                    keyCountY -= 1

            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(launchMissile,0)
            
            if event.type == pygame.QUIT:
                running = False
            
        if event.type == launchMissile:
            m_x = player.xy[0] + 20
            m_y = player.xy[1]  
            Missiles.append(MyMissile(xy=(m_x,m_y),playground = playground, sensitivity = movingScale))
            m_x = player.xy[0] + 80
            Missiles.append(MyMissile(xy=(m_x,m_y),playground = playground, sensitivity = movingScale))
    
    for e in enemies:
        e.update()
        screen.blit(e.image, e.xy)
                
    player.update()
    screen.blit(player.image,player.xy)
    for m in Missiles:
        m.update()
        screen.blit(m.image, m.xy)
    pygame.display.update()
    dt=clock.tick(fps)

pygame.quit()