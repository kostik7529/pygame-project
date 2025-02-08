import random
import pygame
from functions import load_image, show_score, show_misses


fires = pygame.sprite.Group()


class Star(pygame.sprite.Sprite):
    def __init__(self, pos, speed, *group):
        super().__init__(*group)
        self.image = load_image('star.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.group = group

    def update(self, hero, screen):
        if not self.rect.colliderect((0, 0, 600, 300)):
            self.kill()
            show_misses(screen, True)
        if not pygame.sprite.collide_mask(self, hero):
            self.rect = self.rect.move(0, self.speed)
        else:
            hero.create_particles(self.group)
            self.kill()
            show_score(screen, 1, False)
            show_misses(screen, False)


class VipStar(Star):
    def __init__(self, pos, speed, *group):
        super().__init__(pos, speed, *group)
        self.image = load_image('vip_star.png')

    def update(self, hero, screen, catch_by_mouse=False):
        if catch_by_mouse:
            self.kill()
            show_score(screen, 5, False)
            show_misses(screen, False)
        else:
            if not self.rect.colliderect((0, 0, 600, 300)):
                self.kill()
                show_misses(screen, True)
            if not pygame.sprite.collide_mask(self, hero):
                self.rect = self.rect.move(0, 2 * self.speed)
            else:
                hero.create_particles(self.group)
                self.kill()
                show_score(screen, 5, False)
                show_misses(screen, False)


class SuperStar(Star):
    def __init__(self, pos, speed, *group):
        super().__init__(pos, speed, *group)
        self.image = load_image('super_star.png')

    def update(self, hero, screen, catch_by_mouse=False):
        if catch_by_mouse:
            self.kill()
            show_score(screen, 15, False)
            show_misses(screen, False)
        else:
            if not self.rect.colliderect((0, 0, 600, 300)):
                self.kill()
                show_misses(screen, True)
            if not pygame.sprite.collide_mask(self, hero):
                self.rect = self.rect.move(0, 3 * self.speed)
            else:
                hero.create_particles(self.group)
                self.kill()
                show_score(screen, 15, False)
                show_misses(screen, False)


class MainHero(pygame.sprite.Sprite):
    def __init__(self, *group, pos):
        super().__init__(*group)
        self.images = {'right': pygame.transform.scale(load_image('main_hero.png'), (70, 70)),
                       'left': pygame.transform.flip(pygame.transform.scale(load_image('main_hero.png'), (70, 70)), True, False)}
        self.image = self.images['right']
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, direction=1):
        if -10 < self.rect.x + 20 * direction < 550:
            self.rect = self.rect.move(20 * direction, 0)

    def flip(self, side):
        self.image = self.images[side]

    def create_particles(self, *group):
        numbers = range(-20, 20)
        for _ in range(20):
            Particle([self.rect.x + 35, self.rect.y + 35], random.choice(numbers), random.choice(numbers), (self.rect.x - 50, self.rect.y - 50, self.rect.w + 100, self.rect.h + 100),*group)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, rect, *group):
        super().__init__(*group)
        scale = random.randint(5, 15)
        self.image = pygame.transform.scale(load_image(random.choice(['star.png', 'vip_star.png', 'super_star.png'])), (scale, scale))
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1
        self.rect_col = rect

    def update(self, *args):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect((0, 0, 600, 600)):
            self.kill()