import pygame
import json
from struttura_dati import PERSONAGGI, CIBO, EQUIPAGGIAMENTO

def CaricaSettings(percorso):
    file = open(percorso, "r", encoding="utf-8")
    info = file.read()
    dati = json.loads(info)
    file.close()
    return dati["height"], dati["width"], dati["audio"], dati["mod"]
def Carica_equip(percorso):
    file = open(percorso, "r", encoding="utf-8")
    info = file.read()
    dati = json.loads(info)
    file.close()
    return dati["personaggi"], dati["cibo"], dati["equip"]

HEIGHT, WIDTH, VOLUME, MOD = CaricaSettings("dati/setting.json")
personaggi_scelti, cibo_scelto, equip_scelto = Carica_equip("dati/equip.json")
PERSONAGGI_SCELTI = [i for i in PERSONAGGI if i["info"]["name"] in personaggi_scelti]
CIBO_SCELTO = [i for i in CIBO if i["info"]["name"] in cibo_scelto]
EQUIP_SCELTO = [i for i in EQUIPAGGIAMENTO if i["info"]["name"] in equip_scelto]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schermata nera")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()