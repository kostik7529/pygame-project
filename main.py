import pygame
from screens import main_screen, game_screen, lose_screen

screen_type = {1: main_screen, 2: game_screen, 3: lose_screen}

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    cur_screen = 1
    while cur_screen:
        cur_screen = screen_type[cur_screen](screen)
    pygame.quit()