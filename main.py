import pygame
import json
import random
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
x = 0
pygame.init()
schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schermata nera")
clock = pygame.time.Clock()
def x_for_map(x):
    direzione = random.choice(["left", "right", "stop"])
    if direzione == "left":
        x -= 5 * MOD
    elif direzione == "right":
        x += 5 * MOD
    elif direzione == "stop":
        x = x
    return x
        
def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

        
def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64*MOD, 78*MOD), flip=False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)
    
def aggiorna_movimento(p, velocita=2,x_min = 0, x_max= WIDTH - 50):
    tempo_corrente = pygame.time.get_ticks()

    if tempo_corrente - p["pos"]["main"]["ultimo_cambio"] > 2000:  
        p["pos"]["main"]["direzione"] = random.choice(["destra", "sinistra", "fermo"])
        p["pos"]["main"]["ultimo_cambio"] = tempo_corrente
    
    if p["pos"]["main"]["x_attuale"] < x_min:
        p["pos"]["main"]["direzione"] = "destra"
    elif p["pos"]["main"]["x_attuale"] > x_max:
        p["pos"]["main"]["direzione"] = "sinistra"

    if p["pos"]["main"]["direzione"] == "destra":
        p["pos"]["main"]["x_attuale"] += velocita * MOD
        return False, "walk_cycle"
    elif p["pos"]["main"]["direzione"] == "sinistra":
        p["pos"]["main"]["x_attuale"] -= velocita * MOD
        return True, "walk_cycle"
    else:
        return False, "idle"
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    schermo.fill((0, 0, 0))
    for p in PERSONAGGI_SCELTI:
        flip, animazione = aggiorna_movimento(p)
        disegna_animazione(schermo, p["sprites"], animazione, 200, (p["pos"]["main"]["x_attuale"], 300), flip=flip)  
    pygame.display.update()
    clock.tick(60)

pygame.quit()