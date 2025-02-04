import random
import pygame
from sprites import Star, MainHero, VipStar, SuperStar
from functions import load_image, show_score, show_misses
import functions
import time


LEVEL = 1


def main_screen(screen):
    fon = load_image("img_2.png")
    pygame.display.set_mode(fon.get_size())
    intro_text = ["ИГРА", "",
                  "Правила игры: собери как можно больше звёздочек!",
                  "Если пропустишь 3 подряд - ты проиграл!",
                  "Красные звёздочки можно ловить не только зайчиком, ",
                  "но и с помощью ЛКМ, а синие - с помощью ПКМ",
                  "Для запуска игры нажми любую кнопку",
                  "Чтобы выйти из игры нажми ESCAPE",
                  f"BEST Score: {open('score.txt', 'r').read()}"]

    fon = pygame.transform.scale(fon, (600, 349))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 25)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black' if intro_text.index(line) != len(intro_text) - 1 else 'red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                return 2
        pygame.display.flip()


def game_screen(screen):
    background = load_image("img_2.png")
    pygame.display.set_mode(background.get_size())
    all_sprites = pygame.sprite.Group()
    hero = MainHero(all_sprites, pos=(250, 250))
    clock = pygame.time.Clock()
    drop_def_star = pygame.USEREVENT + 1
    pygame.time.set_timer(drop_def_star, random.randint(1000, 2000))
    drop_vip_star = pygame.USEREVENT + 2
    pygame.time.set_timer(drop_vip_star, random.randint(6000, 8000))
    drop_super_star = pygame.USEREVENT + 3
    pygame.time.set_timer(drop_super_star, random.randint(9000, 20000))
    level_up = pygame.USEREVENT + 4
    pygame.time.set_timer(level_up, 40000)
    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            global LEVEL
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                screen.fill((0, 0, 0))
                return 1
            if event.type == drop_vip_star:
                VipStar((random.randint(0, 570), 0), LEVEL, all_sprites)
            if event.type == drop_super_star:
                SuperStar((random.randint(0, 570), 0), LEVEL,  all_sprites)
            if event.type == drop_def_star:
                Star((random.randint(0, 570), 0), LEVEL,  all_sprites)
            if event.type == level_up:
                LEVEL += 1
            if event.type == 771:
                if event.text.lower() in ['d', 'в']:
                    hero.move()
                    hero.flip('right')
                if event.text.lower() in ['a', 'ф']:
                    hero.move(-1)
                    hero.flip('left')
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for i in all_sprites:
                    if i.__class__.__name__ == 'SuperStar':
                        i.update(hero, screen, True)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in all_sprites:
                    if i.__class__.__name__ == 'VipStar':
                        i.update(hero, screen, True)
        all_sprites.draw(screen)
        show_score(screen)
        show_misses(screen)
        all_sprites.update(hero, screen)
        pygame.display.flip()
        clock.tick(170 * (1 - (LEVEL // 3)))
        if functions.MISSES >= 3:
            return 3


def lose_screen(screen):
    fon = load_image("img_2.png")
    pygame.display.set_mode(fon.get_size())
    intro_text = ["ИГРА ОКОНЧЕНА", "",
                  "Ты пропустил 3 звездочки :(",
                  f"Твой счёт: {functions.SCORE}",
                  "Нажми любую кнопку для выхода в главное меню"]
    if functions.SCORE > int(open('score.txt', 'r').read()):
        open('score.txt', 'w').write(str(functions.SCORE))
    functions.SCORE = 0
    functions.MISSES = 0
    fon = pygame.transform.scale(fon, (600, 349))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                return 1
        pygame.display.flip()