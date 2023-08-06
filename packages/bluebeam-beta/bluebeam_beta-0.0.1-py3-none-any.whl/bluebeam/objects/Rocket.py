from bluebeam.objects import EnemyBullet, Explosion
import pygame


class Rocket(EnemyBullet):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.lifespan = 10.

    def hit(self):
        boom = self.l.create("Explosion", self.pos.xy)
        boom.radius(192)
        self.l.uncreate(self.instid)
