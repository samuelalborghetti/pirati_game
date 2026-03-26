import pygame
import json

IMPOSTAZIONI = "./dati/setting.json"

def CaricaSettings (percorso):
    file = open (percorso, "r", encoding="utf-8")
    info = file.read()
    dati = json.loads (info)
    return dati["height"], dati["width"], dati["audio"], dati["mod"]

WIDTH, HEIGHT, VOLUME, MOD = CaricaSettings (IMPOSTAZIONI)

pygame.init()

bg = pygame.image.load ("./assets/sfondi/menu.jpg")
bg = pygame.transform.scale (bg, (HEIGHT, WIDTH))

screen = pygame.display.set_mode ((HEIGHT, WIDTH))
pygame.display.set_caption ("Pirates of the see")
clock = pygame.time.Clock()

BUTTONS = {"play": [pygame.transform.scale(pygame.image.load ("./assets/tasti/play.jpg"), (180 * MOD, 90 * MOD)), WIDTH, HEIGHT/10], 
            "settings": [pygame.transform.scale(pygame.image.load ("./assets/tasti/settings.jpg"), (180 * MOD, 90 * MOD)), WIDTH, HEIGHT/5], 
            "exit": [pygame.transform.scale(pygame.image.load ("./assets/tasti/exit.jpg"), (180 * MOD, 90 * MOD)), WIDTH, HEIGHT/3]}

def DrawButtons(pulsanti : dict, screen : pygame.Surface):
    for b in pulsanti:
        screen.blit (pulsanti[b][0], (pulsanti[b][1], pulsanti[b][2]))


menu_on = True
while menu_on:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            menu_on = False

    screen.blit (bg, (0,0))
    DrawButtons (BUTTONS, screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()