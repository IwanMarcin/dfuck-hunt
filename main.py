import pygame
import random
import sys
import time

FPS = 60
WIDTH = 900
HEIGHT = 800

pygame.init()

FONT = pygame.font.Font("assets/font/ARMY RUST.ttf", 32)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()

background = pygame.image.load("assets/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

gun_idle = pygame.image.load("assets/shotgun/shotgun.png").convert_alpha()
gun_idle = pygame.transform.scale(gun_idle, (450, 270))

gun_frames = [pygame.image.load(f"assets/shotgun/shotgun_fire{i}.png").convert_alpha() for i in range(6)]
gun_frames = [pygame.transform.scale(img, (500, 350)) for img in gun_frames]

dfuck_fly_frames = [pygame.image.load(f"assets/dfuck/dfuck{i}.png").convert_alpha() for i in range(1,6)]
dfuck_fly_frames = [pygame.transform.scale(img, (100, 100)) for img in dfuck_fly_frames]

dfuck_die_frames = [pygame.image.load(f"assets/dfuck/dfuck_die{i}.png").convert_alpha() for i in range(1,5)]
dfuck_die_frames = [pygame.transform.scale(img, (100, 100)) for img in dfuck_die_frames]

warrior_fly_frames = [pygame.image.load(f"assets/warrior_dfuck/warrior_dfuck{i}.png").convert_alpha() for i in range(1, 6)]
warrior_fly_frames = [pygame.transform.scale(img, (100, 100)) for img in warrior_fly_frames]

warrior_die_frames = [pygame.image.load(f"assets/warrior_dfuck/warrior_dfuck_die{i}.png").convert_alpha() for i in range(1, 6)]
warrior_die_frames = [pygame.transform.scale(img, (100, 100)) for img in warrior_die_frames]

poop_img = pygame.image.load("assets/poop.png").convert_alpha()
poop_img = pygame.transform.scale(poop_img, (90, 90))

crosshair = pygame.image.load("assets/crosshair.png").convert_alpha()

class Player:
    def __init__(self):
        self.hp = 100
        self.ammo = 12
        self.max_ammo = 12
        self.shots = 0
        self.hits = 0
        self.is_reloading = False
        self.reload_timer = 0
        self.reload_duration = 150 

    def fire(self):
        if self.is_reloading:
            return False

        if self.ammo == 0:
            self.start_reload()
            return False

        self.shots += 1
        self.ammo -= 1
        return True

    def start_reload(self):
        if not self.is_reloading:
            self.is_reloading = True
            self.reload_timer = self.reload_duration

    def update_reload(self):
        if self.is_reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.reload()
                self.is_reloading = False

    def reload(self):
        self.ammo = self.max_ammo

class Dfuck:
    DUCK_SIZE = 100
    def __init__(self):
        self.rect = pygame.Rect(
            -self.DUCK_SIZE,
            random.randint(0, int(HEIGHT * 0.4) - self.DUCK_SIZE),
            self.DUCK_SIZE,
            self.DUCK_SIZE
        )
        self.vel = random.choice([3, 4, 5])
        self.anim_index = 0
        self.anim_timer = 0

    def move(self):
        self.rect.x += self.vel
        
        if self.rect.x > WIDTH: 
            self.rect.x = -self.DUCK_SIZE

    def update_animation(self, frames, anim_speed = 10):
        self.anim_timer += 1
        if self.anim_timer % anim_speed == 0:
            self.anim_index = (self.anim_index + 1) % len(frames) 

    def draw(self, screen):
        pass

class DfuckVurnelable(Dfuck):
    def __init__(self):
        super().__init__()
        self.is_dead = False
        self.die_anim_index = 0
        self.die_anim_timer = 0
    
    def hit(self, player, mode):
        player.hits += 1
        player.hp = min(player.hp + 1, 100)
        self.is_dead = True
    
    def update(self):
        if self.is_dead:
            self.die_anim_timer += 1
            if self.die_anim_timer % 10 == 0:
                self.die_anim_index += 1
                if self.die_anim_index >= len(dfuck_die_frames):
                    return True
        else:
            self.move()
            self.update_animation(dfuck_fly_frames)
        return False
    
    def draw(self, screen):
        if self.is_dead:
            if self.die_anim_index < len(dfuck_die_frames):
                screen.blit(dfuck_die_frames[self.die_anim_index], self.rect.topleft)
        else:
            screen.blit(dfuck_fly_frames[self.anim_index], self.rect.topleft)


class DfuckArmed(Dfuck):
    def __init__(self):
        super().__init__()
        self.is_dead = False
        self.die_anim_index = 0
        self.die_anim_timer = 0 
        self.next_poop = random.randint(100, 300)
        self.poops = []

    def hit(self, player, mode):
        player.hits += 1
        self.is_dead = True

    def update(self, player = None):
        if self.is_dead:
            self.die_anim_timer += 1
            if self.die_anim_timer % 10 == 0:
                self.die_anim_index += 1
                if self.die_anim_index >= len(warrior_die_frames):
                    return True
        else:
            self.move()
            self.update_animation(warrior_fly_frames)
            self.next_poop -= 1

            if self.next_poop <= 0:
                self.poops.append(Poop(self.rect.centerx, self.rect.bottom))
                self.next_poop = random.randint(100, 300)
            
            for poop in self.poops[:]:
                if poop.update():
                    if player and mode != "training":
                        player.hp = max(player.hp - player.dmg_from_poop, 0)
                    self.poops.remove(poop)
        return False
    
    def draw(self, screen):
        if self.is_dead:
            if self.die_anim_index < len(warrior_die_frames):
                screen.blit(warrior_die_frames[self.die_anim_index], self.rect.topleft)
        else:
            screen.blit(warrior_fly_frames[self.anim_index], self.rect.topleft)

        for poop in self.poops:
            poop.draw(screen)

class Poop:
    def __init__(self, x, y):
        self.image = poop_img
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        return self.rect.y > HEIGHT
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

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

class LevelManager:
    def __init__(self):
        self.level = 1
        self.score_for_next = 10
    
    def update(self, hits):
        if hits >= self.level * self.score_for_next and self.level < 50:
            self.level += 1

    def get_spawn_chance(self):
        base = 0.7
        if 10 <= self.level < 20:
            return base + 0.05
        elif 30 <= self.level < 40:
            return base + 0.10
        elif 40 <= self.level <= 50:
            return base + 0.20
        return base

    def get_speed_multiplier(self):
        if 20 <= self.level < 30:
            return 1.10
        elif 30 <= self.level < 40:
            return 1.05
        elif 40 <= self.level <= 50:
            return 1.10
        return 1.0

    def get_poop_damage(self):
        base = 5
        if 10 <= self.level < 20:
            return base + 5
        elif 20 <= self.level < 30:
            return base + 10
        elif 40 <= self.level <= 50:
            return base + 20
        return base

    def get_armed_chance(self):
        return min(0.3 + self.level * 0.01, 0.6)

def show_summary(screen, player, mode, elapsed_seconds, level_manager=None):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)  # przezroczystość tła
    overlay.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(overlay, (0, 0))

    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    accuracy = (player.hits / player.shots * 100) if player.shots > 0 else 0

    lines = []
    if mode == "training":
        lines = [
            f"Trening zakończony!",
            f"Strzały: {player.shots}",
            f"Trafienia: {player.hits}",
            f"Celność: {accuracy:.1f}%",
            f"Czas: {minutes}m {seconds}s",
            "",
            "Kliknij mysz lub naciśnij dowolny klawisz, aby wyjść"
        ]
    else:
        lines = [
            f"Przegrana!",
            f"Poziom: {level_manager.level}",
            f"Strzały: {player.shots}",
            f"Trafienia: {player.hits}",
            f"Celność: {accuracy:.1f}%",
            f"Czas: {minutes}m {seconds}s",
            "",
            "Kliknij mysz lub naciśnij dowolny klawisz, aby wyjść"
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


def main(mode="training"):
    start_time = time.time()
    clock = pygame.time.Clock()
    player = Player()
    enemies = [DfuckVurnelable() if random.random()<0.7 else DfuckArmed() for _ in range(5)]
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
            if event.type == pygame.QUIT:
                run = False
                end_time = time.time()
                elapsed = int(end_time - start_time)
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
            if isinstance(d, DfuckVurnelable):
                remove = d.update()
            else:
                remove = d.update(player)
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
            run = False
            end_time = time.time()
            elapsed = int(end_time - start_time)
            show_summary(screen, player, mode, elapsed)

        if mode == "training":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    end_time = time.time()
                    elapsed = int(end_time - start_time)
                    show_summary(screen, player, mode, elapsed)
            
        screen.blit(background, (0, 0))
        for e in enemies: 
            e.draw(screen)

        txt = f"Level: {level_manager.level} | HP: {player.hp:.0f}% Hits: {player.hits} Shoots: {player.shots}"

        screen.blit(FONT.render(txt, True, (255, 255, 255)), (10, 10)) 

        if gun_hiding:
            screen.blit(gun_idle, (WIDTH // 2 - gun_idle.get_width() // 2, gun_hide_y))
        elif gun_showing:
            screen.blit(gun_idle, (WIDTH // 2 - gun_idle.get_width() // 2, gun_show_y))
        elif gun_animating:
            current_gun_img = gun_frames[gun_anim_index]
            screen.blit(current_gun_img, (WIDTH // 2 - current_gun_img.get_width() // 2, HEIGHT - current_gun_img.get_height()))
        else:
            screen.blit(gun_idle, (WIDTH // 2 - gun_idle.get_width() // 2, HEIGHT - gun_idle.get_height()))

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(crosshair, (mouse_pos[0] - crosshair.get_width() // 2,
                                mouse_pos[1] - crosshair.get_height() // 2))
        pygame.display.update()

    pygame.mouse.set_visible(True)
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(overlay, (0, 0))

    summary_title = "Training Summary" if mode == "training" else "Game Over"
    accuracy = (player.hits / player.shots * 100) if player.shots > 0 else 0
    summary_lines = [
        f"Shots fired: {player.shots}",
        f"Hits: {player.hits}",
        f"Accuracy: {accuracy:.1f}%",
        f"Time: {minutes}m {seconds}s"
    ]

    if mode == "survival":
        summary_lines.insert(0, f"Final Level: {level_manager.level}")

    title_text = FONT.render(summary_title, True, (255, 0, 0))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))

    for i, line in enumerate(summary_lines):
        text_surf = FONT.render(line, True, (255, 255, 255))
        screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, 250 + i * 50))

    back_rect = pygame.Rect(WIDTH // 2 - 100, 600, 200, 50)
    pygame.draw.rect(screen, (100, 100, 255), back_rect)
    label = FONT.render("Back to Menu", True, (255, 255, 255))
    screen.blit(label, (back_rect.x + back_rect.width // 2 - label.get_width() // 2, back_rect.y + 10))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    waiting = False

    mode = menu.run()
    main(mode)


if __name__ == "__main__":
    menu = Menu(screen)
    mode = menu.run()
    main(mode)