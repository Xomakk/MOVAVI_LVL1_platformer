import pygame
import settings


class Player:
    def __init__(
        self,
        groups: tuple[pygame.sprite.Group],
        image: str,
        start_x: int = settings.TILE_WIDTH + 5,
        start_y: int = settings.TILE_HEIGHT + 5,
    ) -> pygame.sprite.Sprite:
        self.sprite = pygame.sprite.Sprite(*groups)
        self.sprite.image = pygame.image.load(image)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = start_x
        self.sprite.rect.y = start_y
        self.onGround = False
        self.x_speed = 0
        self.y_speed = 0

    def check_collide(self, tiles, x_vel=0, y_vel=0):
        for tile in tiles:
            if pygame.sprite.collide_mask(self.sprite, tile):
                if x_vel > 0:
                    self.sprite.rect.right = tile.rect.left

                if x_vel < 0:
                    self.sprite.rect.left = tile.rect.right

                if y_vel > 0:
                    self.sprite.rect.bottom = tile.rect.top
                    self.onGround = True
                    self.y_speed = 0

                if y_vel < 0:
                    self.sprite.rect.top = tile.rect.bottom
                    self.y_speed = 0

    def move_controll(self, tiles):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed = -settings.PLAYER_MOVE_SPEED
        elif keys[pygame.K_d]:
            self.x_speed = settings.PLAYER_MOVE_SPEED
        else:
            self.x_speed = 0

        self.sprite.rect.x += self.x_speed
        self.check_collide(tiles, x_vel=self.x_speed)

    def handle_gravity(self, tiles):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.y_speed = -settings.JUMP_POWER

        if not self.onGround:
            self.y_speed += settings.GRAVITY

        self.onGround = False

        self.sprite.rect.y += self.y_speed
        self.check_collide(tiles, y_vel=self.y_speed)
