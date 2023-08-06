import pygame
import math
from bluebeam.objects import EnemyBullet


class Laser(EnemyBullet):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.owner = 1
        self._emitter = None
        self.emitpoint = pygame.math.Vector2(0, 0)
        self.speed = pygame.math.Vector2(0., 0.)
        self.vel = self.speed
        self.lifespan = 2.33
        self._objid = 4
        self._dir = 1
        self._width = 16

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, d_):
        self._dir = d_

    @property
    def emitter(self):
        return self._emitter

    @emitter.setter
    def emitter(self, e_):
        self._emitter = e_

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w_):
        self._width = w_

    def expand(self):
        len = 16
        pow = 5
        self.rect = pygame.rect.Rect(self.emitpoint.x, self.emitpoint.y, 2 + 14 * (self._dir % 2 == 0),
                                     2 + 14 * (self._dir % 2 == 1))
        self.set_dir()
        while pow >= 0 and len < 1024:
            len += math.pow(4, pow)
            self.rect = self.rect.inflate(math.pow(4, pow) * (self._dir % 2 == 0),
                                          math.pow(4, pow) * (self._dir % 2 == 1))
            self.set_dir()
            if self.collision_surface():
                self.rect = self.rect.inflate(-math.pow(4, pow) * (self._dir % 2 == 0),
                                              -math.pow(4, pow) * (self._dir % 2 == 1))
                self.set_dir()
                len -= math.pow(4, pow)
                pow -= 1
        self.rect = self.rect.inflate((self._width - 2) * (self._dir % 2 == 1),
                                      (self._width - 2) * (self._dir % 2 == 0))

    def set_dir(self):
        if self._dir == 0:
            self.rect.midleft = self.emitpoint
        elif self._dir == 1:
            self.rect.midtop = self.emitpoint
        elif self._dir == 2:
            self.rect.midright = self.emitpoint
        elif self._dir == 3:
            self.rect.midbottom = self.emitpoint

    def update(self):
        self.emitpoint = self._emitter.emitpoint
        self.expand()
        self.lifespan -= self.g.delta_time
        if self.lifespan <= 0: self.fadeout()

    def fadeout(self):
        self.l.uncreate(self.instid)

    def hit(self):
        pass

    def render(self):
        pygame.draw.rect(self.l.s, (64, 64, 255, 100), self.rect.copy().move(-self.l.view))
