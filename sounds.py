import pygame

def play_shot():
    sound = pygame.mixer.Sound("assets/sounds/gunshot.mp3")
    sound.set_volume(0.5)
    sound.play()

def play_reload():
    sound = pygame.mixer.Sound("assets/sounds/gunreload.wav")
    sound.play()

def play_quack():
    sound = pygame.mixer.Sound("assets/sounds/quack.mp3")
    sound.play()

def play_music():
    pygame.mixer.music.load("assets/sounds/music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def game_over():
    sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")
    sound.play()

def next_level():
    sound = pygame.mixer.Sound("assets/sounds/next_level.mp3")
    sound.play()