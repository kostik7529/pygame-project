import pygame


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