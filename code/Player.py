from pathlib import Path
from GameObject import GameObject
import pygame
import math
class Player(GameObject):
    def __init__(self,playground, xy=None, sensitivity=1):
        GameObject.__init__(self,playground)
        self._moveScale = 0.5*sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__player_path = __parent_path /'res'/'airforce.png'
        self._image = pygame.image.load(self.__player_path)
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h / 2  #用get_rect取得圖片長寬後設定中心點
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)  #碰撞半徑
        self.max_hp = 3
        self._hp = self.max_hp
        self._last_hit_time = 0
        self._invincible_duration = 1000  #  無敵時間1秒
  
        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w) / 2
            self._y = 3 * self._playground[1] / 4
        else:
            self._x = xy[0]
            self._y = xy[1]
        #設定邊界
        self._objectBound = (10,self._playground[0] - (self._image.get_rect().w + 10),10,self._playground[1] - (self._image.get_rect().w + 10))  

    def update(self):
        GameObject.update(self)
        self._center = self._x + self._image.get_rect().w / 2 ,self._y + self._image.get_rect().h / 2

    def collision_detect(self, enemies):
        now = pygame.time.get_ticks()
        if now - self._last_hit_time < self._invincible_duration:
            return  # 無敵中，暫時不碰撞
        
        for m in enemies:
            if self._collided_(m):
                self._hp-=1
                self._collided = True
                self._last_hit_time = now  # 記錄被打時間
                m.hp = -1
                m.collided = True
                m.available = False

    def should_draw(self):
    # 無敵時間內交錯閃爍
        now = pygame.time.get_ticks()
        if now - self._last_hit_time < self._invincible_duration:
            return (now // 100) % 2 == 0  # 每 100ms 閃一次
        return True  #不在無敵狀態內