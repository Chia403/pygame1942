from pathlib import Path
from GameObject import GameObject
import pygame
import random

class Explosion(GameObject):
    explosion_effect = []
    def __init__(self, xy=None):
        GameObject.__init__(self)
        if xy is None:    #預設位置，測試時可能會用到，正常運行就用不到
            self._y = -100
            self._x = random.randint( 10, self._playground[0] - 100)
        else:
          self._x = xy[0]
          self._y = xy[1]

        if Explosion.explosion_effect:
            pass  # 已經載入過圖了，就跳過
        else:     # 第一次使用才會載入圖到 explosion_effect
            __parent_path = Path(__file__).parents[1]
            icon_path = __parent_path / 'res' / 'explosion_small.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'explosion_medium.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'explosion_large.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'explosion_medium.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'explosion_small.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))

        self.__image_index = 0
        self._image = Explosion.explosion_effect[self.__image_index]
        self.__fps_count = 0
        self._available = True 

    def update(self):
        self.__fps_count +=1
        if self.__fps_count >10: #調整爆炸動畫速度
            self.__image_index +=1
           # self.__fps_count =0
            if self.__image_index>4:
                self._available = False
            else:
                self._image = Explosion.explosion_effect[self.__image_index]