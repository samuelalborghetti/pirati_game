import pygame
import json

IMPOSTAZIONI = "./dati/setting.json"

def CaricaFinestra (percorso):
    file = open (percorso, "r", encoding="utf-8")
    info = file.read()
    dati = json.loads (info)
    return dati["height"], dati["widht"]

WIDHT, HEIGHT = CaricaFinestra (IMPOSTAZIONI)

pygame.init()

bg = pygame.image.load ("assets/sfondi/defualt.jpg")
bg = pygame.transform.scale (bg, (HEIGHT, WIDHT))

screen = pygame.display.set_mode ((HEIGHT,WIDHT))
pygame.display.set_caption ("Pirates of the see")
clock = pygame.time.Clock()

menu_on = True
while menu_on:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            menu_on = False
    
    screen.blit (bg, (0,0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()