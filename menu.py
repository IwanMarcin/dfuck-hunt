import pygame
import sys
from assets import screen, FONT, WIDTH, HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = {
            "Training": pygame.Rect(WIDTH // 2 - 100, 300, 200, 50),
            "Survival": pygame.Rect(WIDTH // 2 - 100, 400, 200, 50),
            "Exit": pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)
        }
        self.background = pygame.image.load("assets/menu.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (100, 100, 255), rect)
            label = FONT.render(text, True, (255, 255, 255))
            self.screen.blit(label, (rect.x + rect.width // 2 - label.get_width() // 2, rect.y + 10))
        pygame.display.update()

    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for name, rect in self.buttons.items():
                        if rect.collidepoint(pos):
                            if name == "Exit":
                                pygame.quit()
                                sys.exit()
                            return name.lower()
