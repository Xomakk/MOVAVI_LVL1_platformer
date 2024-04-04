import pygame
import settings


def load_map(
    level_filepath: str,
    image_filepath: str,
    tile_groups: tuple[pygame.sprite.Group],
    portal_filepath: str,
    portal_groups: tuple[pygame.sprite.Group],
):
    tiles_group = pygame.sprite.Group()
    portals_group = pygame.sprite.Group()
    player_x = settings.TILE_WIDTH
    player_y = settings.TILE_HEIGHT

    with open(level_filepath, "r") as level_map_file:
        data = level_map_file.readlines()

    for row_index, line in enumerate(data):
        for col_index, item in enumerate(line):
            tile = None
            if item == "-":
                tile = pygame.sprite.Sprite(tiles_group, *tile_groups)
                tile.image = pygame.image.load(image_filepath)
            elif item == "?":
                tile = pygame.sprite.Sprite(portals_group, *portal_groups)
                tile.image = pygame.image.load(portal_filepath)
            elif item == "P":
                player_x = col_index * settings.TILE_WIDTH
                player_y = row_index * settings.TILE_HEIGHT

            if tile:
                tile.rect = tile.image.get_rect()
                tile.rect.x = col_index * settings.TILE_WIDTH
                tile.rect.y = row_index * settings.TILE_HEIGHT

    map_width = (col_index + 1) * settings.TILE_WIDTH
    map_height = (row_index + 1) * settings.TILE_HEIGHT

    return tiles_group, portals_group, map_width, map_height, player_x, player_y
