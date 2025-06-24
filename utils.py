import pygame
import sys
from assets import WIDTH, HEIGHT, background, FONT

def show_summary(screen, player, mode, elapsed_seconds, level_manager=None):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180) 
    overlay.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(overlay, (0, 0))

    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    accuracy = (player.hits / player.shots * 100) if player.shots > 0 else 0

    if mode == "training":
        lines = [
            "Training Complete!",
            f"Shots Fired: {player.shots}",
            f"Hits: {player.hits}",
            f"Accuracy: {accuracy:.1f}%",
            f"Time: {minutes}m {seconds}s",
            "",
            "Click the mouse or press any key to exit"
        ]
    else:
        lines = [
            "Game Over!",
            f"Level Reached: {level_manager.level}",
            f"Shots Fired: {player.shots}",
            f"Hits: {player.hits}",
            f"Accuracy: {accuracy:.1f}%",
            f"Time: {minutes}m {seconds}s",
            "",
            "Click the mouse or press any key to exit"
        ]

    y = HEIGHT // 3
    for line in lines:
        text_surf = FONT.render(line, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(WIDTH // 2, y))
        screen.blit(text_surf, text_rect)
        y += 40

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT):
                waiting = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.time.Clock().tick(30)
