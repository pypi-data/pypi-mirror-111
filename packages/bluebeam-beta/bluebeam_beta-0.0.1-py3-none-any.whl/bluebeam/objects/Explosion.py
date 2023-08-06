from bluebeam.objects import EnemyBullet
import pygame


class Explosion(EnemyBullet):

    def __init__(self, g_, l_, pos_):
        super().__init__(g_, l_, pos_)
        self.lifespan = 1
        self.dmg = 20
        pass

    def radius(self, radi):
        self.rect = pygame.rect.Rect(self.pos.x - radi / 2, self.pos.y - radi / 2, radi, radi)
        self.rect.center = self.pos

    def hit(self):
        pass

    def update(self):
        if self.lifespan <= 0:
            self.l.uncreate(self.instid)
        else:
            self.lifespan = 0

    def render(self):
        pygame.draw.circle(self.l.s, (255, 255, 128, 100), self.rect.center - self.l.view, self.rect.width / 1.71)
