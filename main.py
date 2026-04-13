import pygame
import json
import random
from struttura_dati import PERSONAGGI, CIBO, EQUIPAGGIAMENTO, EVENTI

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
bg = pygame.image.load("assets/sfondi/main.png")
bg = pygame.transform.scale (bg, (WIDTH, HEIGHT))

schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schermata nera")
clock = pygame.time.Clock()
        
def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

        
def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64*MOD, 78*MOD), flip=False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)
    
def riordina_per_profondita(pers):
    n = len(pers)
    for i in range(n - 1):
        n_scambi = 0
        for j in range(n - i - 1):
            if pers[j]["pos"]["main"]["y_attuale"] > pers[j + 1]["pos"]["main"]["y_attuale"]:
                pers[j], pers[j + 1] = pers[j + 1], pers[j]
                n_scambi += 1
        if n_scambi == 0:
            break
def controllo_distanze(pers):
    trovato = True
    while trovato:
        trovato = False 
        for i in range(len(pers)):
            for j in range(len(pers)):
                if i != j: 
                    distanza_x = abs(pers[i]["pos"]["main"]["x_attuale"] - pers[j]["pos"]["main"]["x_attuale"])
                    distanza_y = abs(pers[i]["pos"]["main"]["y_attuale"] - pers[j]["pos"]["main"]["y_attuale"])
                    if distanza_x < 40 * MOD and distanza_y < 40 * MOD:
                        trovato = True     
                        if random.choice([True, False]):
                            pers[i]["pos"]["main"]["x_attuale"] = random.randint(400*MOD, WIDTH - 420*MOD)
                        else:
                            pers[i]["pos"]["main"]["x_attuale"] = random.randint(400*MOD, WIDTH - 420*MOD)
                        if random.choice([True, False]):
                            pers[i]["pos"]["main"]["y_attuale"] = random.randint(430*MOD, 470*MOD)
                        else:
                            pers[i]["pos"]["main"]["y_attuale"] = random.randint(430*MOD, 470*MOD)
                            
                            
def scelta_eventi(EVENTI):
    evento_Selezionato = random.choice(EVENTI)
    return evento_Selezionato

controllo_distanze(PERSONAGGI_SCELTI)     
riordina_per_profondita(PERSONAGGI_SCELTI)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    schermo.blit(bg, (0, 0))
    for p in PERSONAGGI_SCELTI:
        disegna_animazione(schermo, p["sprites"], "idle", 200*MOD, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]), flip = False)  
    pygame.display.update()
    clock.tick(60)

pygame.quit()