import pygame

WIDTH = 900
HEIGHT = 800

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

FONT = pygame.font.Font("assets/font/18 ARMY.otf", 24)
screen = pygame.display.set_mode([WIDTH, HEIGHT])

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
