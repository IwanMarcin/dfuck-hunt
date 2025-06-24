import pygame
import random
from sounds import play_quack
from assets import dfuck_fly_frames, dfuck_die_frames, warrior_fly_frames, warrior_die_frames, poop_img, HEIGHT

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
        if self.rect.x > 900:
            self.rect.x = -self.DUCK_SIZE

    def update_animation(self, frames, anim_speed=10):
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
        play_quack()
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
        play_quack()
        self.is_dead = True

    def update(self, player=None, mode=None):
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
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        return self.rect.y > HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
