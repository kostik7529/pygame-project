import os
import sys
import pygame

SCORE = 0
MISSES = 0
fires = pygame.sprite.Group()


class Fires(pygame.sprite.Sprite):
    def __init__(self, pos, x, y, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('fire.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.move_x, self.move_y = x, y

    def update(self, screen, rect):
        if not self.rect.colliderect(rect):
            self.kill()
        else:
            self.rect = self.rect.move(0, 1)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def show_score(screen, value=0, called_from_main=True):
    global SCORE
    if value is not None:
        SCORE += value
    font = pygame.font.Font(None, 50)
    score = font.render(f'Score: {SCORE}', 1, pygame.Color('purple'))
    score_rect = score.get_rect()
    score_rect.top = 10
    score_rect.x = int((600 - score_rect.width) * 0.5)
    if not called_from_main:
        for i in range(score_rect.x, score_rect.x + score_rect.w, 30):
            Fires([i, score_rect.h - 20], 1, 0, fires)
    fires.update(screen, (score_rect.x - 20, score_rect.y, score_rect.w + 40, score_rect.h - 10))
    fires.draw(screen)
    screen.blit(score, score_rect)


def show_misses(screen, missed=None):
    global MISSES
    if missed is not None:
        MISSES = 0 if not missed else (MISSES + 1)
    font = pygame.font.Font(None, 50)
    misses = font.render(f'Missed: {MISSES}', 1, pygame.Color('red'))
    misses_rect = misses.get_rect()
    misses_rect.top = 10
    misses_rect.x = 10
    screen.blit(misses, misses_rect)

def sound():
    pygame.mixer.music.load('data/sound.wav')
    pygame.mixer.music.play()