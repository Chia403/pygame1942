from pathlib import Path
from GameObject import GameObject
import pygame
import math
import random

class Enemy(GameObject):
    def __init__(self, playground, xy=None, sensitivity=1):
        GameObject.__init__(self,playground)
        self._moveScale = 0.3 * sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__enemy_path = __parent_path / 'res' / 'enemy.png'
        self._image = pygame.image.load(self.__enemy_path)
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)
        self._changeY = self._moveScale 
        self.collided = False
        self.hp = 10
        self._available = True
        
        if xy is None:
            self._x = random.randint(10, self._playground[0] - self._image.get_rect().w - 10)
            self._y = -self._image.get_rect().h 
        else:
            self._x = xy[0]
            self._y = xy[1]
        
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2
        
        # 移動邊界設定
        self._objectBound = (0,self._playground[0] - (self._image.get_rect().w), - (self._image.get_rect().w),self._playground[1])

    def update(self):
        GameObject.update(self)
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2

    @property
    def collected(self):
      return not self._available  # 被擊中後就不是 available
    
    @property
    def center(self):
      return self._center  #顯示爆炸時需用到
