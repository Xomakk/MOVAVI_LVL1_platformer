import pygame
import settings


def create(
    groups: tuple[pygame.sprite.Group],
    image_filepath: str,
    start_x: int = settings.TILE_WIDTH + 5,
    start_y: int = settings.TILE_HEIGHT + 5,
) -> pygame.sprite.Sprite:
    player = pygame.sprite.Sprite(*groups)
    player.image = pygame.image.load(image_filepath)
    player.rect = player.image.get_rect()
    player.onGround = False
    player.x_speed = 0
    player.y_speed = 0
    player.rect.x = start_x
    player.rect.y = start_y
    return player


def check_collide(hero, tiles, x_vel=0, y_vel=0):
    for tile in tiles:
        if pygame.sprite.collide_mask(hero, tile):
            if x_vel > 0:
                hero.rect.right = tile.rect.left

            if x_vel < 0:
                hero.rect.left = tile.rect.right

            if y_vel > 0:
                hero.rect.bottom = tile.rect.top
                hero.onGround = True
                hero.y_speed = 0

            if y_vel < 0:
                hero.rect.top = tile.rect.bottom
                hero.y_speed = 0


def move_controll(hero, tiles):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        hero.x_speed = -settings.PLAYER_MOVE_SPEED
    elif keys[pygame.K_d]:
        hero.x_speed = settings.PLAYER_MOVE_SPEED
    else:
        hero.x_speed = 0

    hero.rect.x += hero.x_speed
    check_collide(hero, tiles, x_vel=hero.x_speed)


def handle_gravity(hero, tiles):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if hero.onGround:  # прыгаем, только когда можем оттолкнуться от земли
            hero.y_speed = -settings.JUMP_POWER

    if not hero.onGround:
        hero.y_speed += settings.GRAVITY

    hero.onGround = False

    hero.rect.y += hero.y_speed
    check_collide(hero, tiles, y_vel=hero.y_speed)
