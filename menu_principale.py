import pygame
import json

IMPOSTAZIONI = "./dati/setting.json"
SFONDO = "./assets/sfondi/menu.jpg"

def CaricaSettings (percorso: str):
    file = open (percorso, "r", encoding="utf-8")
    info = file.read()
    dati = json.loads (info)
    return dati["height"], dati["widht"], dati["audio"]

WIDHT, HEIGHT, VOLUME = CaricaSettings (IMPOSTAZIONI)

pygame.init()

bg = pygame.image.load (SFONDO)
bg = pygame.transform.scale (bg, (HEIGHT, WIDHT))

screen = pygame.display.set_mode ((HEIGHT,WIDHT))
pygame.display.set_caption ("Pirates of the see")
clock = pygame.time.Clock()

BUTTONS_NAME = ["play", "settings", "exit"]

BUTTONS_IMAGE = {"play": pygame.transform.scale(pygame.image.load ("./assets/tasti/play.jpg"), (70, 70)), 
                 "settings": pygame.transform.scale(pygame.image.load ("./assets/tasti/settings.jpg"), (70, 70)), 
                 "exit": pygame.transform.scale(pygame.image.load ("./assets/tasti/exit.jpg"), (70,70))}

BUTTONS_RECT = {"play": pygame.Rect (WIDHT - BUTTONS_IMAGE["play"].get_width() * 1.5, HEIGHT/10, BUTTONS_IMAGE["play"].get_height(), BUTTONS_IMAGE["play"].get_width()), 
                "settings": pygame.Rect (HEIGHT/3, WIDHT/3, BUTTONS_IMAGE["settings"].get_height(), BUTTONS_IMAGE["settings"].get_width()), 
                "exit": pygame.Rect (HEIGHT/4, WIDHT/4, BUTTONS_IMAGE["exit"].get_height(), BUTTONS_IMAGE["exit"].get_width())}

def DrawButtons(name: list, img: dict, card: dict, screen: pygame):
    for b in name:
        screen.blit (img [b], (card[b].x, card[b].y))


menu_on = True
while menu_on:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            menu_on = False

    screen.blit (bg, (0,0))
    DrawButtons (BUTTONS_NAME, BUTTONS_IMAGE, BUTTONS_RECT, screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()