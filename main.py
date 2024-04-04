import pygame
from camera import Camera, camera_configure
import settings
import player
import map

pygame.init()


levels = ["./levels/1.txt", "./levels/2.txt"]


def start_level(all_sprites: pygame.sprite.Group, level_number: int):
    walls, portals, map_width, map_height, player_x, player_y = map.load_map(
        level_filepath=levels[level_number],
        image_filepath="./images/platform.png",
        tile_groups=(all_sprites,),
        portal_filepath="./images/portal.png",
        portal_groups=(all_sprites,),
    )
    hero = player.create(
        groups=(all_sprites,),
        image_filepath="./images/mario.png",
        start_x=player_x,
        start_y=player_y,
    )
    camera = Camera(camera_configure, map_width, map_height)

    return hero, walls, portals, camera


def main():
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # версия с полноэкранным режимом
    screen = pygame.display.set_mode(settings.SCREEN_SIZE)

    all_sprites = pygame.sprite.Group()

    level_number = 0
    hero, walls, portals, camera = start_level(all_sprites, level_number)

    clock = pygame.time.Clock()
    run = True
    end_game = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(settings.BACKGROUND_COLOR)

        player.move_controll(hero, walls)
        player.handle_gravity(hero, walls)
        # all_sprites.draw(screen) # 1. вариант до камеры
        camera.update(hero)
        for sprite in all_sprites:
            screen.blit(sprite.image, (camera.apply(sprite)))

        for portal in portals:
            if pygame.sprite.collide_mask(hero, portal):
                level_number += 1
                all_sprites.empty()
                if level_number < len(levels):
                    hero, walls, portals, camera = start_level(
                        all_sprites, level_number
                    )
                else:
                    end_game = True

        if end_game is True:
            font_obj = pygame.font.Font(None, 64)
            text = font_obj.render("YOU WIN!", True, "white")
            screen.blit(text, (500, 300))

        pygame.display.update()
        clock.tick(settings.FPS)


main()

pygame.quit()
