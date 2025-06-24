import pygame
import time
import random
from player import Player
from enemies import DfuckVurnelable, DfuckArmed
from menu import Menu
from level_manager import LevelManager
from sounds import play_music, game_over
from assets import screen, background, gun_idle, gun_frames, FONT, WIDTH, HEIGHT, crosshair
from utils import show_summary

FPS = 60
muted = False

def main(mode="training"):
    start_time = time.time()
    clock = pygame.time.Clock()
    player = Player()
    enemies = [DfuckVurnelable() if random.random() < 0.7 else DfuckArmed() for _ in range(5)]
    level_manager = LevelManager()
    run = True
    pygame.mouse.set_visible(False)

    gun_anim_index = 0
    gun_anim_timer = 0
    gun_animating = False
    gun_hiding = False
    gun_hide_y = HEIGHT - gun_idle.get_height()
    gun_hide_speed = 20
    gun_showing = False
    gun_show_y = HEIGHT
    gun_show_speed = 20

    while run:
        clock.tick(FPS)
        player.update_reload()

        if gun_animating:
            gun_anim_timer += 1
            if gun_anim_timer % 2 == 0:
                gun_anim_index += 1
                if gun_anim_index >= len(gun_frames):
                    gun_animating = False
                    gun_anim_index = 0
        
        if gun_hiding:
            gun_hide_y += gun_hide_speed
            if gun_hide_y > HEIGHT:
                gun_hiding = False
                player.start_reload()
                gun_showing = True
                gun_show_y = HEIGHT
        else:
            player.update_reload()

        if gun_showing:
            gun_show_y -= gun_show_speed
            if gun_show_y <= HEIGHT - gun_idle.get_height():
                gun_showing = False
                gun_show_y = HEIGHT - gun_idle.get_height()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    elapsed = int(time.time() - start_time)
                    show_summary(screen, player, mode, elapsed, level_manager)
                elif event.key == pygame.K_m:
                    global muted
                    muted = not muted
                    if muted:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            if event.type == pygame.QUIT:
                run = False
                elapsed = int(time.time() - start_time)
                show_summary(screen, player, mode, elapsed, level_manager)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.ammo == 0 and not player.is_reloading and not gun_hiding:
                    gun_hiding = True
                    gun_hide_y = HEIGHT - gun_idle.get_height()
                elif player.fire() or mode == "training":
                    gun_animating = True
                    gun_anim_index = 0
                    gun_anim_timer = 0
                    for d in enemies:
                        if d.rect.collidepoint(event.pos):
                            d.hit(player, mode)
                            break
        
        enemies_to_remove = []
        for d in enemies:
            remove = d.update(player) if isinstance(d, DfuckArmed) else d.update()
            if remove:
                enemies_to_remove.append(d)

        for d in enemies_to_remove:
            enemies.remove(d)
            level_manager.update(player.hits)

            speed_multiplier = level_manager.get_speed_multiplier()
            poop_dmg = level_manager.get_poop_damage()
            armed_chance = level_manager.get_armed_chance()

            new_duck = DfuckArmed() if random.random() < armed_chance else DfuckVurnelable()
            new_duck.vel = int(new_duck.vel * speed_multiplier)

            player.dmg_from_poop = poop_dmg
            enemies.append(new_duck)
        
        if mode == "survival" and player.hp <= 0:
            game_over()
            run = False
            elapsed = int(time.time() - start_time)
            show_summary(screen, player, mode, elapsed, level_manager)

        screen.blit(background, (0, 0))
        for e in enemies:
            e.draw(screen)

        info_panel_width = 200
        info_panel_height = 130
        info_panel_x = WIDTH - info_panel_width 
        info_panel_y = HEIGHT - info_panel_height 
        info_panel_color = (0, 0, 0, 150)

        info_panel = pygame.Surface((info_panel_width, info_panel_height), pygame.SRCALPHA)
        info_panel.fill(info_panel_color)

        lines = [
            f"Level: {level_manager.level}",
            f"HP: {player.hp:.0f}%",
            f"Ammo: {player.ammo}/{player.max_ammo}",
            f"Hits: {player.hits}",
            f"Shots: {player.shots}"
        ]

        line_height = 24
        for i, line in enumerate(lines):
            text_surf = FONT.render(line, True, (255, 255, 255))
            info_panel.blit(text_surf, (10, 10 + i * line_height))

        screen.blit(info_panel, (info_panel_x, info_panel_y))

        if gun_hiding:
            screen.blit(gun_idle, (WIDTH // 2 - gun_idle.get_width() // 2, gun_hide_y))
        elif gun_showing:
            screen.blit(gun_idle, (WIDTH // 2 - gun_idle.get_width() // 2, gun_show_y))
        elif gun_animating:
            screen.blit(gun_frames[gun_anim_index], (WIDTH // 2 - gun_frames[gun_anim_index].get_width() // 2, HEIGHT - gun_frames[gun_anim_index].get_height()))
        else:
            screen.blit(gun_idle, (WIDTH // 2 - gun_idle.get_width() // 2, HEIGHT - gun_idle.get_height()))

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(crosshair, (mouse_pos[0] - crosshair.get_width() // 2, mouse_pos[1] - crosshair.get_height() // 2))

        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    play_music()
    menu = Menu(screen)

    while True:
        pygame.mouse.set_visible(True)
        mode = menu.run()
        if mode == "exit":
            pygame.quit()
            break
        main(mode)
