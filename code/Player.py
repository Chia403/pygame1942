from pathlib import Path
from typing import Union
import pygame
from pygame.surface import Surface, SurfaceType
from GameObject import GameObject
import math
class Player(GameObject):
    def __init__(self,playground, xy=None, sensitivity=1):
        GameObject.__init__(self,playground)
        self._moveScale = 0.5*sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__player_path = __parent_path /'res'/'airforce.png'
        self._image = pygame.image.load(self.__player_path)
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h / 2
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)  #碰撞半徑

        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w) / 2
            self._y = 3 * self._playground[1] / 4
        else:
            self._x = xy[0]
            self._y = xy[1]

        self._objectBound = (10,self._playground[0] - (self._image.get_rect().w + 10),10,self._playground[1] - (self._image.get_rect().w + 10))

    def update(self):
        GameObject.update(self)
        self._center = self._x + self._image.get_rect().w / 2 ,self._y + self._image.get_rect().h / 2

    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                self._hp-=10
                self._collided = True
                m.hp = -1
                m.collided = True
                m.available = False



