import pygame
import random
import sys
import math

pygame.init()
fps = 60
timer = pygame.time.Clock()

WIDTH = 900
HEIGHT = 800
FONT = pygame.font.SysFont("monospace", 24)
screen = pygame.display.set_mode([WIDTH, HEIGHT])

class Player:
    def __init__(self):
        self.hp = 100
        self.ammo = 12
        self.max_ammo = 12
        self.shots = 0
        self.hits = 0

    def fire(self):
        if self.ammo == 0:
            self.reload()  
        if self.ammo > 0:
            self.shots += 1
            self.ammo -= 1
            return True
        return False

    def reload(self):
        self.ammo = self.max_ammo

class Dfuck:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 50), random.randint(50, HEIGHT - 50), 50, 50)
        self.vel = random.choice([3, 4, 5])

    def move(self):
        self.rect.x += self.vel
        
        if self.rect.x > WIDTH: 
            self.rect.x = -50

    def draw(self, win):
        pygame.draw.rect(win, (200, 200, 200), self.rect)

class DfuckVurnelable(Dfuck):
    def hit(self, player, mode):
        player.hits += 1
        if mode == "survival":
            player.hp = min(100, player.hp + 1)


class DfuckArmed(Dfuck):
    def __init__(self):
        super().__init__()
        self.next_poop = random.randint(100, 300)
    
    def hit(self, player, mode):
        player.hits += 1

    def update(self, player):
        self.next_poop -= 1
        if self.next_poop <= 0:
            player.hp -= 5
            self.next_poop = random.randint(100, 300)

def main(mode="training"):
    clock = pygame.time.Clock()
    player = Player()
    enemies = [DfuckVurnelable() if random.random()<0.7 else DfuckArmed() for _ in range(5)]
    run = True
    
    while run:
        clock.tick(fps)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if player.fire() or mode == "training":
                    for d in enemies:
                        if d.rect.collidepoint(e.pos):
                            d.hit(player, mode)
                            enemies.remove(d)
                            enemies.append(DfuckVurnelable() if random.random()<0.7 else DfuckArmed())
                            break
        
        for d in enemies:
            d.move()
            if isinstance(d, DfuckArmed):
                d.update(player)

        
        if mode == "survival" and player.hp <= 0:
            run = False
            
        screen.fill((50, 50, 50))
        for e in enemies: 
            e.draw(screen)

        txt = f"HP: {player.hp:.0f}% Hits: {player.hits} Shoots: {player.shots}"
        screen.blit(FONT.render(txt, True, (255, 255, 255)), (10, 10))
        pygame.display.update()

    screen.fill((0, 0, 0))
    if mode == "training":
        percentage = (player.hits/player.shots*100) if player.shots > 0 else 0
        msg = f"Ratio: {percentage:.1f}%"
    else:
        msg: f"You've shot {player.hits} freaking dfucks"
        
    screen.blit(FONT.render(msg, True, (255, 0, 0)), (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main("survival")