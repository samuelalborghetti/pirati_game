import pygame
import json
import random
import copy
from struttura_dati import PERSONAGGI, CIBO, BIBITE, EQUIPAGGIAMENTO, EVENTI
from gestione_eventi import *


GIALLO = (255, 215, 0)
BIANCO = (255, 255, 255)
numero_settimane = 8
settimana_corrente = 1


def CaricaSettings(percorso):
    file = open(percorso, "r", encoding="utf-8")
    dati = json.loads(file.read())
    file.close()
    return dati["height"], dati["width"], dati["audio"], dati["mod"]

def Carica_equip(percorso):
    file = open(percorso, "r", encoding="utf-8")
    dati = json.loads(file.read())
    file.close()
    return dati["personaggi"], dati["cibo"], dati["equip"], dati["soldi"]



def carica_verdura_totale(Cibo_scelto):
    verdura_totale = 0
    non_verdura_totale = 0
    for c in Cibo_scelto:
        if c["stats"]["verdura"] == True:
            verdura_totale += c["stats"]["saturazione"]
        else:
            non_verdura_totale += c["stats"]["saturazione"]
    return verdura_totale, non_verdura_totale

def carica_acqua_totale(Bibite_scelto):
    acqua_totale = 0
    for b in Bibite_scelto:
        if b["info"]["name"] == "acqua":
            acqua_totale += b["stats"]["saturazione"]
    return acqua_totale


HEIGHT, WIDTH, VOLUME, MOD = CaricaSettings("dati/setting.json")
personaggi_scelti, cibo_scelto, equip_scelto, soldi_rimanenti = Carica_equip("dati/equip.json")

PERSONAGGI_SCELTI = []
for nome in personaggi_scelti:
    for p in PERSONAGGI:
        if p["info"]["name"] == nome:
            p_copia = {
                "stats": copy.deepcopy(p["stats"]),
                "pos": copy.deepcopy(p["pos"]),
                "sprites": p["sprites"],
                "info": p["info"],
            }
            PERSONAGGI_SCELTI.append(p_copia)

CIBO_SCELTO   = [i for i in CIBO if i["info"]["name"] in cibo_scelto]
BIBITE_SCELTE = [i for i in BIBITE if i["info"]["name"] in cibo_scelto]
EQUIP_SCELTO  = [i for i in EQUIPAGGIAMENTO if i["info"]["name"] in equip_scelto]
verdura_totale, non_verdura_totale = carica_verdura_totale(CIBO_SCELTO)
acqua_totale = carica_acqua_totale(BIBITE_SCELTE)
saturazione_totale = verdura_totale + non_verdura_totale


pygame.init()
pygame.display.set_icon(pygame.image.load("assets/sfondi/icon.png"))

schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("main")
clock = pygame.time.Clock()
font_numeri = pygame.font.Font("assets/fonts/Barrio-Regular.ttf", int(24 * MOD))
title_font = pygame.font.Font("assets/fonts/PixelifySans-Medium.ttf", int(18 * MOD))

bg = pygame.transform.scale(pygame.image.load("assets/sfondi/main.png"), (WIDTH, HEIGHT))

play = pygame.transform.scale(pygame.image.load("assets/tasti/play.png"), (int(150 * MOD), int(75 * MOD)))
rect_play = play.get_rect(topleft=(WIDTH - 200 * MOD, HEIGHT - 100 * MOD))

SCAFFALE_MONEY = pygame.transform.scale(pygame.image.load("assets/tasti/scaffalemain.png"), (int(310 * MOD), int(280 * MOD)))


posizioni = [
    (400*MOD, 420*MOD), (455*MOD, 420*MOD), (500*MOD, 430*MOD), (550*MOD, 430*MOD),
    (70*MOD,  340*MOD), (165*MOD, 330*MOD), (23*MOD,  365*MOD), (600*MOD, 480*MOD),
    (400*MOD, 480*MOD), (117*MOD, 370*MOD), (600*MOD, 420*MOD), (650*MOD, 450*MOD),
    (330*MOD, 380*MOD), (455*MOD, 470*MOD), (500*MOD, 480*MOD), (550*MOD, 470*MOD),
]


def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = int(tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def shell_sort_per_profondita(personaggi):
    n = len(personaggi)
    
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = personaggi[i]
            j = i
            
            
            while j >= gap and personaggi[j-gap]["pos"]["main"]["y_attuale"] > temp["pos"]["main"]["y_attuale"]:
                personaggi[j] = personaggi[j-gap]
                j -= gap
            personaggi[j]= temp
        gap //= 2

def assegna_posizioni(pers, posizioni):
    for i in range(min(len(pers), len(posizioni))):
        pers[i]["pos"]["main"]["x_attuale"] = posizioni[i][0]
        pers[i]["pos"]["main"]["y_attuale"] = posizioni[i][1]

def Drawtext(schermo, text: list, y_in, x_testo, font_scelto, colore, spazio_tra_righe):
    y = y_in
    for riga in text:
        testo = font_scelto.render(riga, True, colore)
        schermo.blit(testo, (x_testo, y))
        y += spazio_tra_righe

def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64*MOD, 78*MOD), flip=False):
    frame_grezzo  = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)

def DrawMoney(screen, soldi_correnti):
    testo = font_numeri.render(f"Soldi: {soldi_correnti}", True, BIANCO)
    rett  = testo.get_rect(topright=(screen.get_width() - 20*MOD, 20*MOD))
    screen.blit(testo, rett)

def draw_settimana(screen, settimana_corrente):
    testo = font_numeri.render(f"Settimana: {settimana_corrente}", True, BIANCO)
    rett  = testo.get_rect(topright=(screen.get_width() - 15*MOD, 110*MOD))
    screen.blit(testo, rett)

def draw_cibo_totale(screen, saturazione_totale):
    testo = font_numeri.render(f"Cibo: {saturazione_totale}", True, BIANCO)
    rett  = testo.get_rect(topright=(screen.get_width() - 48*MOD, 190*MOD))
    screen.blit(testo, rett)

def draw_cibo_info_box(screen, mouse_pos, saturazione_totale, verdura_totale, acqua_totale, rect_cibo):
    if rect_cibo.collidepoint(mouse_pos):
        rect_info = pygame.Rect(rect_cibo.x + 20*MOD, (rect_cibo.y + rect_cibo.height + 5*MOD)+10*MOD, 200*MOD, 120*MOD)
        pygame.draw.rect(screen, (161, 88, 0), rect_info, 0, 10)
        pygame.draw.rect(screen, (0, 0, 0), rect_info, 3, 10)
        titolo = title_font.render("Risorse", True, BIANCO)
        cibo_text = title_font.render(f"Cibo: {saturazione_totale}", True, BIANCO)
        verdura_text = title_font.render(f"Verdura: {verdura_totale}", True, BIANCO)
        acqua_text = title_font.render(f"Acqua: {acqua_totale}", True, BIANCO)
        screen.blit(titolo, (rect_info.x + 10*MOD, rect_info.y + 10*MOD))
        screen.blit(cibo_text, (rect_info.x + 10*MOD, rect_info.y + 40*MOD))
        screen.blit(verdura_text, (rect_info.x + 10*MOD, rect_info.y + 65*MOD))
        screen.blit(acqua_text, (rect_info.x + 10*MOD, rect_info.y + 90*MOD))

def DrawButton(schermo, play, rect, x, y):
    schermo.blit(play, (x, y))

def schermata_nera(schermo, clock, durata_ms=4000):
    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        schermo.fill((0, 0, 0))
        pygame.display.update()
        clock.tick(60)

assegna_posizioni(PERSONAGGI_SCELTI, posizioni)
shell_sort_per_profondita(PERSONAGGI_SCELTI)

animazione_attiva = False
schermata = 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and schermata == 1:
            mouse_pos = pygame.mouse.get_pos()
            if rect_play.collidepoint(mouse_pos):
                settimana_corrente += 1
                saturazione_totale -= 1
                evento_casuale = scelta_evento(EVENTI)
                schermata_nera(schermo, clock)
                animazione_attiva = False
                schermata = 2

    if schermata == 1:
        schermo.blit(bg, (0,0))
        for p in PERSONAGGI_SCELTI:
            disegna_animazione(schermo, p["sprites"], "idle", 135 , (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        schermo.blit(SCAFFALE_MONEY, (WIDTH - 240 * MOD, -20 * MOD))
        DrawMoney(schermo, soldi_rimanenti)
        draw_settimana(schermo, settimana_corrente)
        rect_cibo = pygame.Rect(WIDTH - 240 * MOD, 190 * MOD - 20 * MOD, 200 * MOD, 30 * MOD)
        draw_cibo_totale(schermo, saturazione_totale)
        draw_cibo_info_box(schermo, pygame.mouse.get_pos(), saturazione_totale, verdura_totale, acqua_totale, rect_cibo)
        DrawButton(schermo, play, rect_play, WIDTH - 200 * MOD, HEIGHT - 100 * MOD)
    elif schermata == 2:
        if not animazione_attiva:
            animazione_attiva = True 
            animazione_attacco_pirata_caduta_proiettili(schermo, clock, EVENTI[14]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg) 
            animazione_divento(schermo, clock, EVENTI[17]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg, 5000, FONT_BOLD, favorevole=True)
            animazione_divento(schermo, clock, EVENTI[16]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg, 5000, FONT_BOLD, favorevole=False)
            
            animazione_albatro(schermo, clock, EVENTI[11]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
            animazione_isola(schermo, clock, EVENTI[18]["sprites"], WIDTH, HEIGHT, 5000)
            animazione_epidemia(schermo, clock, PERSONAGGI_SCELTI, bg)
            

            random.shuffle(posizioni)
            assegna_posizioni(PERSONAGGI_SCELTI, posizioni)
            shell_sort_per_profondita(PERSONAGGI_SCELTI)

            if settimana_corrente > numero_settimane:
                print("Hai vinto!")
                running = False

            schermata_nera(schermo, clock)
            schermata = 1
    pygame.display.update()
    clock.tick(60)

pygame.quit()