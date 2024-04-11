import pygame
from camera import Camera, camera_configure
import settings
from player import Player
from map import load_map

pygame.init()


def start_level(all_sprites: pygame.sprite.Group):
    walls, portals, map_width, map_height, player_x, player_y = load_map(
        level_schema="./levels/1.txt",
        wall_img="./images/platform.png",
        portal_img="./images/portal.png",
        all_sprites=all_sprites,
    )
    hero = Player(
        groups=(all_sprites,),
        image="./images/mario.png",
        start_x=player_x,
        start_y=player_y,
    )
    camera = Camera(camera_configure, map_width, map_height)

    return hero, walls, portals, camera


def main():
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # версия с полноэкранным режимом
    screen = pygame.display.set_mode(settings.SCREEN_SIZE)

    all_sprites = pygame.sprite.Group()

    hero, walls, portals, camera = start_level(all_sprites)

    clock = pygame.time.Clock()
    run = True
    end_game = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(settings.BACKGROUND_COLOR)

        if not end_game:
            hero.move_controll(walls)
            hero.handle_gravity(walls)

            # all_sprites.draw(screen) # 1. вариант до камеры
            camera.update(hero.sprite)
            for sprite in all_sprites:
                screen.blit(sprite.image, (camera.apply(sprite)))

            for portal in portals:
                if pygame.sprite.collide_mask(hero.sprite, portal):
                    end_game = True

        else:
            font_obj = pygame.font.Font(None, 64)
            text = font_obj.render("YOU WIN!", True, "white")
            screen.blit(text, (500, 300))

        pygame.display.update()
        clock.tick(settings.FPS)


main()

pygame.quit()
