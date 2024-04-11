import pygame
import settings


class Block:
    def __init__(self, img_path: str, x: int | float, y: int | float, *groups):
        self.sprite = pygame.sprite.Sprite(*groups)
        self.sprite.image = pygame.image.load(img_path)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = x
        self.sprite.rect.y = y


def load_map(
    level_schema: str,
    wall_img: str,
    portal_img: str,
    all_sprites: pygame.sprite.Group,
):
    walls_group = pygame.sprite.Group()
    portals_group = pygame.sprite.Group()
    player_x = settings.TILE_WIDTH
    player_y = settings.TILE_HEIGHT

    with open(level_schema, "r") as level_map_file:
        data = level_map_file.readlines()

    for row_index, line in enumerate(data):
        for col_index, item in enumerate(line):
            x = col_index * settings.TILE_WIDTH
            y = row_index * settings.TILE_HEIGHT
            if item == "-":
                Block(wall_img, x, y, all_sprites, walls_group)
            elif item == "?":
                Block(portal_img, x, y, all_sprites, portals_group)
            elif item == "P":
                player_x = x
                player_y = y

    map_width = (col_index + 1) * settings.TILE_WIDTH
    map_height = (row_index + 1) * settings.TILE_HEIGHT

    return walls_group, portals_group, map_width, map_height, player_x, player_y
