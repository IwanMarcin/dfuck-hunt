import pygame
from sounds import play_shot, play_reload

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
        self.dmg_from_poop = 5 

    def fire(self):
        if self.is_reloading:
            return False
        if self.ammo == 0:
            self.start_reload()
            return False
        play_shot()
        self.shots += 1
        self.ammo -= 1
        return True

    def start_reload(self):
        if not self.is_reloading:
            self.is_reloading = True
            self.reload_timer = self.reload_duration
            play_reload()

    def update_reload(self):
        if self.is_reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.reload()
                self.is_reloading = False

    def reload(self):
        self.ammo = self.max_ammo
