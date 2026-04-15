import pygame
import json
import random
from struttura_dati import PERSONAGGI, CIBO, EQUIPAGGIAMENTO, EVENTI
import copy
from gestione_eventi import *

numero_settimane = 8
settimana_corrente = 1

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
    return dati["personaggi"], dati["cibo"], dati["equip"], dati["soldi"]

HEIGHT, WIDTH, VOLUME, MOD = CaricaSettings("dati/setting.json")
personaggi_scelti, cibo_scelto, equip_scelto, soldi_rimanenti = Carica_equip("dati/equip.json")
PERSONAGGI_SCELTI = []
for nome in personaggi_scelti:
    for p in PERSONAGGI:
        if p["info"]["name"] == nome:
            p_copia = { "stats": copy.deepcopy(p["stats"]), "pos": copy.deepcopy(p["pos"]), "sprites": p["sprites"], "info": p["info"],}
            PERSONAGGI_SCELTI.append(p_copia)
CIBO_SCELTO = [i for i in CIBO if i["info"]["name"] in cibo_scelto]
EQUIP_SCELTO = [i for i in EQUIPAGGIAMENTO if i["info"]["name"] in equip_scelto]

pygame.init()
pygame.display.set_icon(pygame.image.load("assets/sfondi/icon.png"))
bg = pygame.image.load("assets/sfondi/main.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schermata nera")
clock = pygame.time.Clock()
font_numeri = pygame.font.Font("assets/fonts/Barrio-Regular.ttf", int(24 * MOD))
GIALLO = (255, 215, 0)

def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = int(tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64*MOD, 78*MOD), flip=False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)

def DrawMoney(screen, soldi_correnti):
    testo = font_numeri.render(f"Soldi: {soldi_correnti}", True, GIALLO)
    rett = testo.get_rect(topright=(screen.get_width() - 20, 20))
    screen.blit(testo, rett)

def bubble_sort_per_profondita(personaggi):
    n = len(personaggi)
    for i in range(n):
        for j in range(0, n - i - 1):
            if personaggi[j]["pos"]["main"]["y_attuale"] > personaggi[j + 1]["pos"]["main"]["y_attuale"]:
                personaggi[j], personaggi[j + 1] = personaggi[j + 1], personaggi[j]

def schermo_nero(schermo, ora, ultimo_nero, tempro_prima_prossimo_nero=10000, durata=2000):
    tempo_dal_nero = ora - ultimo_nero
    if tempo_dal_nero >= tempro_prima_prossimo_nero:
        schermo.fill((0, 0, 0))
        if tempo_dal_nero >= tempro_prima_prossimo_nero + durata:
            ultimo_nero = ora
    return ultimo_nero

def assegna_posizioni(pers, posizioni):
    for i in range(min(len(pers), len(posizioni))):
        pers[i]["pos"]["main"]["x_attuale"] = posizioni[i][0]
        pers[i]["pos"]["main"]["y_attuale"] = posizioni[i][1]

play = pygame.image.load("assets/tasti/play.png")
play = pygame.transform.scale(play, (int(150*MOD), int(75*MOD)))
rect_play = play.get_rect(topleft=(WIDTH-200*MOD, HEIGHT-100*MOD))

def DrawButton(schermo, play, rect, x, y):
    schermo.blit(play, (x, y))

posizioni = [
    (400*MOD, 420*MOD),
    (455*MOD, 420*MOD),
    (500*MOD, 430*MOD),
    (550*MOD, 430*MOD),
    (70*MOD, 340*MOD),
    (165*MOD, 330*MOD),
    (23*MOD, 365*MOD),
    (600*MOD, 480*MOD),
    (400*MOD, 480*MOD),
    (117*MOD, 370*MOD),
    (600*MOD, 420*MOD),
    (650*MOD, 450*MOD),
    (330*MOD, 380*MOD),
    (455*MOD, 470*MOD),
    (500*MOD, 480*MOD),
    (550*MOD, 470*MOD),
]

ultimo_nero = pygame.time.get_ticks()
assegna_posizioni(PERSONAGGI_SCELTI, posizioni)
bubble_sort_per_profondita(PERSONAGGI_SCELTI)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if rect_play.collidepoint(mouse_pos):
                settimana_corrente += 1
                evento_casuale = scelta_evento(EVENTI)
                print(f"Settimana {settimana_corrente}: {evento_casuale}")
                random.shuffle(posizioni)
                assegna_posizioni(PERSONAGGI_SCELTI, posizioni)
                bubble_sort_per_profondita(PERSONAGGI_SCELTI)

    schermo.blit(bg, (0, 0))
    for p in PERSONAGGI_SCELTI:
        disegna_animazione(schermo, p["sprites"], "idle", 150*MOD, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]), flip=False)
    DrawMoney(schermo, soldi_rimanenti)
    DrawButton(schermo, play, rect_play, WIDTH-200*MOD, HEIGHT-100*MOD)

    pygame.display.update()
    clock.tick(60)

pygame.quit()