from Player import Player
from pathlib import Path
from missile import MyMissile
from enemy import Enemy
from explosion import Explosion
import random
import pygame

pygame.init()  #初始化

screenHigh = 760
screenWidth = 1000
playground = [screenWidth, screenHigh]
screen = pygame.display.set_mode((screenWidth,screenHigh))
keyCountX = 0
keyCountY = 0
Missiles = []
enemies = []
Boom = []

enemy_spawn_interval = 1000  # 毫秒，每 1 秒出現一台敵機
last_enemy_spawn_time = pygame.time.get_ticks()
launchMissile = pygame.USEREVENT + 1  #自訂事件(自動連射飛彈)

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
background_path = image_path / 'background.jpg'
background_image = pygame.image.load(background_path)
background_image = pygame.transform.scale(background_image, (screenWidth, screenHigh))
bg_y1 = 0            # 背景圖的 Y 座標
bg_y2 = -screenHigh  # 第二張接在上面
bg_scroll_speed = 2  # 每幀往下移動的速度
heart_path = image_path / 'heart.png'
heart_image = pygame.image.load(heart_path)
heart_image = pygame.transform.scale(heart_image, (32, 32)) 
game_over_path = image_path / 'gameover.png'
game_over_img = pygame.image.load(game_over_path)   #gameover圖片
game_over_img = pygame.transform.scale(game_over_img, (1000, 760)) 

while running:
    # 畫兩張背景圖
    screen.blit(background_image, (0, bg_y1))
    screen.blit(background_image, (0, bg_y2))

    # 捲動背景圖
    bg_y1 += bg_scroll_speed
    bg_y2 += bg_scroll_speed

    # 如果一張完全離開螢幕，就重設到上方
    if bg_y1 >= screenHigh:
        bg_y1 = bg_y2 - screenHigh
    if bg_y2 >= screenHigh:
      bg_y2 = bg_y1 - screenHigh

    game_over = False

    if player._hp <= 0:
        game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =  False
        
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
                m_x = player.x + 20  #左邊飛彈位置
                m_y = player.y  
                Missiles.append(MyMissile(xy=(m_x,m_y),playground = playground, sensitivity = movingScale))  # 關鍵字參數
                m_x = player.x + 80  #右邊飛彈位置
                Missiles.append(MyMissile(playground,(m_x,m_y),movingScale))  # 位置參數
                pygame.time.set_timer(launchMissile,400)  #連射 速度

            if event.key == pygame.K_r:
               # 重新初始化遊戲狀態
               game_over = False
               player._hp = player.max_hp
               player._collided = False
               player._last_hit_time = 0
               enemies.clear()
               Missiles.clear()
               Boom.clear()

            

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
    
    #自動產生敵人
    now = pygame.time.get_ticks()
    if now - last_enemy_spawn_time > enemy_spawn_interval:
        x = random.randint(0, playground[0] - 100)
        y = random.randint(-200, -50)
        enemies.append(Enemy(playground, xy=(x, y), sensitivity=movingScale))
        last_enemy_spawn_time = now

    if not game_over:
         # 事件更新（碰撞）
        player.collision_detect(enemies)
        for m in Missiles:
            m.collision_detect(enemies)

        for e in enemies[:]:
           if e.collided:
                Boom.append(Explosion(xy=e.center))
                enemies.remove(e)
        
        player.update()   #所有物件 update 
        if player.should_draw():  #在should_draw的時候畫 無敵才會閃爍
             screen.blit(player.image,player.xy)
        
        # 血量顯示（右上角）
        for i in range(player._hp):
            screen.blit(heart_image, (screenWidth - (i+1)*40 - 10, 10))

        for m in Missiles:
            m.update()
            screen.blit(m.image, m.xy)

        for e in enemies:
            e.update()
            screen.blit(e.image, e.xy)

        for e in Boom:
            e.update()
            screen.blit(e.image, e.xy)
    
        # 移除已無效物件
        Missiles = [m for m in Missiles if m._available]
        enemies = [e for e in enemies if e._available]
        Boom = [b for b in Boom if b._available]

    else:
        screen.blit(game_over_img, ((screenWidth - game_over_img.get_width()) // 2,  #gameover時顯示圖片
                    (screenHigh - game_over_img.get_height()) // 2))

    # 更新畫面 + 時脈控制
    pygame.display.update()
    dt=clock.tick(fps)

pygame.quit()