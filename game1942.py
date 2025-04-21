import pygame
pygame.init()

screenHigh = 760
screenWidth = 1000
screen = pygame.display.set_mode((screenWidth,screenHigh))

running = True
fps=120
clock = pygame.time.Clock()



from pathlib import Path
parent_path = Path(__file__).parents[1]
image_path = parent_path /'res'
icon_path = image_path / 'airplaneicon.png'

pygame.display.set_caption("1942偽")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((50,50,50))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =  False
    screen.blit(background,(0,0))
    pygame.display.update()
    dt=clock.tick(fps)
pygame.quit()