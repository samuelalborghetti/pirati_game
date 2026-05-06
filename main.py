import pygame
import json
import random
import copy
from struttura_dati import PERSONAGGI, CIBO, BIBITE, MERCI, EVENTI
from gestione_eventi import *
from utility import HEIGHT, WIDTH, MOD, BIANCO, font_numeri, title_font
from eventi import (
    evento_uomo_in_mare, evento_verdura_in_mare, evento_frutta_in_mare,
    evento_carne_in_mare, evento_acqua_in_mare, evento_pesca_miracolosa,
    evento_tempesta_miracolosa, evento_venti_favorevoli, evento_cattivo_tempo,
    evento_ondata, evento_infestazione_ratti, evento_avvistamento_albatro,
    evento_scialuppa, evento_epidemia, evento_attacco_pirata,
    evento_danni_timone, evento_raffiche_vento, evento_avvistamento_isola,
    step_ammutinamento, step_ricalcolo_settimane,
    conta_membri_vivi, applica_morti_morale_zero,
    mostra_messaggio_evento, gestisci_razioni_interattivo
)

numero_settimane = 8
settimana_corrente = 1

albatro_avvistato = 0
albatro_ucciso = None
fortuna_dellalbatro = False

razioni_attuali = {"verdura": 1.0, "frutta": 1.0, "carne": 1.0, "acqua": 1.0}

mazzo_eventi = [
    "UOMO IN MARE", "VERDURA IN MARE", "FRUTTA IN MARE", "CARNE IN MARE", "ACQUA IN MARE",
    "PESCA MIRACOLOSA", "TEMPESTA MIRACOLOSA", "VENTI FAVOREVOLI", "CATTIVO TEMPO", "ONDATA",
    "INFESTAZIONE RATTI", "AVVISTAMENTO ALBATRO", "AVVISTAMENTO SCIALUPPA", "EPIDEMIA",
    "ATTACCO PIRATA", "DANNI AL TIMONE", "RAFFICHE DI VENTO", "AVVISTAMENTO ISOLA",
    "NESSUN IMPREVISTO", "NESSUN IMPREVISTO", "NESSUN IMPREVISTO",
    "NESSUN IMPREVISTO", "NESSUN IMPREVISTO", "NESSUN IMPREVISTO"
]


def Carica_equip(percorso):
    with open(percorso, "r", encoding="utf-8") as f:
        dati = json.load(f)
    return dati["personaggi"], dati["cibo"], dati["equip"], dati["soldi"]

def carica_totali_cibo(cibo_lista):
    totale_verdura = totale_carne = totale_frutta = 0
    for c in cibo_lista:
        tipo = c["stats"].get("tipo_cibo", "altro")
        if tipo == "verdura":
            totale_verdura += c["stats"]["saturazione"]
        elif tipo == "carne":
            totale_carne += c["stats"]["saturazione"]
        elif tipo == "frutta":
            totale_frutta += c["stats"]["saturazione"]
    return totale_carne, totale_verdura, totale_frutta

def carica_acqua_totale(bibite_lista):
    totale = 0
    for b in bibite_lista:
        if b["info"]["name"] == "acqua":
            totale += b["stats"]["saturazione"]
    return totale

def carica_totali_equip(equip_lista):
    medicinali = 0
    armi = 0
    for e in equip_lista:
        if e["info"]["name"] == "medicinale":
            medicinali += 1
        elif e["info"]["name"] == "armi":
            armi += 1
    return medicinali, armi, len(equip_lista)

def aggiorna_saturazione(verdura, acqua, carne, frutta):
    return verdura + acqua + carne + frutta


personaggi_scelti, cibo_scelto_nomi, equip_scelto_nomi, soldi_rimanenti = Carica_equip("dati/equip.json")

PERSONAGGI_SCELTI = []
for nome in personaggi_scelti:
    for p in PERSONAGGI:
        if p["info"]["name"] == nome:
            PERSONAGGI_SCELTI.append({
                "stats": copy.deepcopy(p["stats"]),
                "pos": copy.deepcopy(p["pos"]),
                "sprites": p["sprites"],
                "info": p["info"],
            })

CIBO_SCELTO = []
for nome in cibo_scelto_nomi:
    for c in CIBO:
        if c["info"]["name"] == nome:
            CIBO_SCELTO.append(c)

BIBITE_SCELTE = []
for nome in cibo_scelto_nomi:
    for b in BIBITE:
        if b["info"]["name"] == nome:
            BIBITE_SCELTE.append(b)

lista_merci = []
for nome in equip_scelto_nomi:
    for e in MERCI:
        if e["info"]["name"] == nome:
            nuova = {"info": e["info"], "stats": copy.deepcopy(e["stats"])}
            if "sprites" in e:
                nuova["sprites"] = e["sprites"]
            lista_merci.append(nuova)

carne_totale, verdura_totale, frutta_totale = carica_totali_cibo(CIBO_SCELTO)
acqua_totale = carica_acqua_totale(BIBITE_SCELTE)
saturazione_totale = aggiorna_saturazione(verdura_totale, acqua_totale, carne_totale, frutta_totale)
totale_medicinali, totale_armi, totale_merci = carica_totali_equip(lista_merci)


pygame.init()
pygame.display.set_icon(pygame.image.load("assets/sfondi/icon.png"))
schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirates of the Sea")
clock = pygame.time.Clock()

bg = pygame.transform.scale(pygame.image.load("assets/sfondi/main.png"), (WIDTH, HEIGHT))
bg_caduta = pygame.transform.scale(pygame.image.load("assets/sfondi/sfondo_per_caduta.png"), (WIDTH, HEIGHT))

play = pygame.transform.scale(pygame.image.load("assets/tasti/play.png"), (int(150*MOD), int(75*MOD)))
rect_play = play.get_rect(topleft=(WIDTH - 200*MOD, HEIGHT - 100*MOD))
bt_wiew_equip = pygame.transform.scale(pygame.image.load("assets/tasti/play.png"), (int(150*MOD), int(75*MOD)))
rect_bt_wiew_equip = bt_wiew_equip.get_rect(topleft=(50*MOD, HEIGHT - 100*MOD))
SCAFFALE_MONEY = pygame.transform.scale(pygame.image.load("assets/tasti/scaffalemain.png"), (int(330*MOD), int(210*MOD)))

posizioni = [
    (400*MOD, 420*MOD), (455*MOD, 420*MOD), (500*MOD, 430*MOD), (550*MOD, 430*MOD),
    (70*MOD, 340*MOD), (165*MOD, 330*MOD), (23*MOD, 365*MOD), (600*MOD, 480*MOD),
    (400*MOD, 480*MOD), (117*MOD, 370*MOD), (600*MOD, 420*MOD), (650*MOD, 450*MOD),
    (330*MOD, 380*MOD), (455*MOD, 470*MOD), (500*MOD, 480*MOD), (550*MOD, 470*MOD),
]


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
            personaggi[j] = temp
        gap //= 2

def assegna_posizioni(pers, pos):
    for i in range(min(len(pers), len(pos))):
        pers[i]["pos"]["main"]["x_attuale"] = pos[i][0]
        pers[i]["pos"]["main"]["y_attuale"] = pos[i][1]

def DrawMoney(screen, soldi):
    t = font_numeri.render(f"Soldi: {soldi:.1f}", True, BIANCO)
    screen.blit(t, t.get_rect(topright=(screen.get_width() - 35*MOD, 22*MOD)))

def draw_settimana(screen, corrente):
    t = font_numeri.render(f"Settimana: {corrente}/{numero_settimane}", True, BIANCO)
    screen.blit(t, t.get_rect(topright=(screen.get_width() - 20*MOD, 85*MOD)))

def draw_cibo_totale(screen, sat):
    t = font_numeri.render(f"Cibo: {sat:.1f}", True, BIANCO)
    screen.blit(t, t.get_rect(topright=(screen.get_width() - 58*MOD, 147*MOD)))

def draw_cibo_info_box(screen, mouse_pos, sat, acqua, verdura, frutta, carne, rect_cibo):
    if not rect_cibo.collidepoint(mouse_pos):
        return
    r = pygame.Rect(rect_cibo.x + 20*MOD, rect_cibo.y + rect_cibo.height + 19*MOD, 200*MOD, 170*MOD)
    pygame.draw.rect(screen, (161, 88, 0), r, 0, 10)
    pygame.draw.rect(screen, (0, 0, 0), r, 3, 10)

    txt0 = title_font.render("Risorse", True, BIANCO)
    txt1 = title_font.render(f"Cibo totale: {sat:.1f}", True, BIANCO)
    txt2 = title_font.render(f"Acqua: {acqua:.1f}", True, BIANCO)
    txt3 = title_font.render(f"Verdura: {verdura:.1f}", True, BIANCO)
    txt4 = title_font.render(f"Frutta: {frutta:.1f}", True, BIANCO)
    txt5 = title_font.render(f"Carne: {carne:.1f}", True, BIANCO)

    x = r.x + 10*MOD
    screen.blit(txt0, (x, r.y + 10*MOD))
    screen.blit(txt1, (x, r.y + 35*MOD))
    screen.blit(txt2, (x, r.y + 60*MOD))
    screen.blit(txt3, (x, r.y + 85*MOD))
    screen.blit(txt4, (x, r.y + 110*MOD))
    screen.blit(txt5, (x, r.y + 135*MOD))

def draw_equip_info_box(screen, mouse_pos, med, armi, merci_tot, rect_bt):
    if not rect_bt.collidepoint(mouse_pos):
        return
    w, h = int(220*MOD), int(120*MOD)
    r = pygame.Rect(rect_bt.x, rect_bt.y - h - 10*MOD, w, h)
    pygame.draw.rect(screen, (161, 88, 0), r, 0, 10)
    pygame.draw.rect(screen, (0, 0, 0), r, 3, 10)

    txt0 = title_font.render("Equipaggiamento", True, BIANCO)
    txt1 = title_font.render(f"Medicinali: {med}", True, BIANCO)
    txt2 = title_font.render(f"Armi: {armi}", True, BIANCO)
    txt3 = title_font.render(f"Totale merci: {merci_tot}", True, BIANCO)

    x = r.x + 10*MOD
    screen.blit(txt0, (x, r.y + 10*MOD))
    screen.blit(txt1, (x, r.y + 40*MOD))
    screen.blit(txt2, (x, r.y + 70*MOD))
    screen.blit(txt3, (x, r.y + 100*MOD))

def schermata_nera(durata_ms=3000):
    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
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
            if rect_play.collidepoint(pygame.mouse.get_pos()):
                schermata_nera()
                animazione_attiva = False
                schermata = 2

    if schermata == 1:
        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            if p["stats"]["alive"]:
                disegna_animazione(schermo, p["sprites"], "idle", 135,
                                   (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        schermo.blit(SCAFFALE_MONEY, (WIDTH - 260*MOD, -10*MOD))
        DrawMoney(schermo, soldi_rimanenti)
        draw_settimana(schermo, settimana_corrente)
        rect_cibo = pygame.Rect(WIDTH - 240*MOD, 147*MOD, 200*MOD, 30*MOD)
        draw_cibo_totale(schermo, saturazione_totale)
        draw_cibo_info_box(schermo, pygame.mouse.get_pos(),
                           saturazione_totale, acqua_totale, verdura_totale,
                           frutta_totale, carne_totale, rect_cibo)
        schermo.blit(play, rect_play.topleft)
        schermo.blit(bt_wiew_equip, rect_bt_wiew_equip.topleft)
        draw_equip_info_box(schermo, pygame.mouse.get_pos(),
                            totale_medicinali, totale_armi, totale_merci, rect_bt_wiew_equip)

    elif schermata == 2:
        if not animazione_attiva:
            animazione_attiva = True

            if not mazzo_eventi:
                evento_estratto = "NESSUN IMPREVISTO"
            else:
                evento_estratto = random.choice(mazzo_eventi)

            if evento_estratto == "AVVISTAMENTO ALBATRO":
                if albatro_avvistato >= 2:
                    mazzo_eventi.remove(evento_estratto)
            elif evento_estratto != "NESSUN IMPREVISTO":
                mazzo_eventi.remove(evento_estratto)

            if evento_estratto == "UOMO IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[0]["sprites"], WIDTH, HEIGHT,
                                     bg_caduta, f"idle{random.randint(1,2)}",
                                     int(75*MOD), int(96*MOD), ["Un uomo e' caduto in mare!"])
                PERSONAGGI_SCELTI, nome_vittima = evento_uomo_in_mare(PERSONAGGI_SCELTI)

            elif evento_estratto == "VERDURA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[1]["sprites"], WIDTH, HEIGHT,
                                     bg_caduta, "verdura", int(75*MOD), int(96*MOD),
                                     ["Tempesta! Verdura in mare!"])
                verdura_totale -= evento_verdura_in_mare(verdura_totale)
                verdura_totale = max(0.0, verdura_totale)

            elif evento_estratto == "FRUTTA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[2]["sprites"], WIDTH, HEIGHT,
                                     bg_caduta, "frutta", int(75*MOD), int(96*MOD),
                                     ["Tempesta! Frutta in mare!"])
                frutta_totale -= evento_frutta_in_mare(frutta_totale)
                frutta_totale = max(0.0, frutta_totale)

            elif evento_estratto == "CARNE IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[3]["sprites"], WIDTH, HEIGHT,
                                     bg_caduta, "carne", int(75*MOD), int(96*MOD),
                                     ["Tempesta! Carne in mare!"])
                carne_totale -= evento_carne_in_mare(carne_totale)
                carne_totale = max(0.0, carne_totale)

            elif evento_estratto == "ACQUA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[4]["sprites"], WIDTH, HEIGHT,
                                     bg_caduta, "acqua", int(50*MOD), int(86*MOD),
                                     ["Tempesta! Acqua in mare!"])
                acqua_totale -= evento_acqua_in_mare(acqua_totale)
                acqua_totale = max(0.0, acqua_totale)

            elif evento_estratto == "PESCA MIRACOLOSA":
                anima_pescamiracolosa(schermo, clock, EVENTI[5]["sprites"], WIDTH, HEIGHT)
                carne_totale = evento_pesca_miracolosa(carne_totale)

            elif evento_estratto == "TEMPESTA MIRACOLOSA":
                anima_tempesta_miracolosa(schermo, clock, EVENTI[6]["sprites"], WIDTH, HEIGHT,
                                          bg, "barile", int(165*MOD), PERSONAGGI_SCELTI, int(190*MOD))
                acqua_totale = evento_tempesta_miracolosa(acqua_totale)

            elif evento_estratto == "VENTI FAVOREVOLI":
                animazione_divento(schermo, clock, EVENTI[17]["sprites"], WIDTH, HEIGHT,
                                   PERSONAGGI_SCELTI, bg, 5000, title_font, favorevole=True)
                numero_settimane, bonus = evento_venti_favorevoli(numero_settimane)

            elif evento_estratto == "CATTIVO TEMPO":
                anima_cattivo_tempo(schermo, clock, EVENTI[8]["sprites"], WIDTH, HEIGHT,
                                    bg, PERSONAGGI_SCELTI, ["Il cattivo tempo rovescia medicinali!"])
                lista_merci = evento_cattivo_tempo(lista_merci)

            elif evento_estratto == "ONDATA":
                animazione_ondata(schermo, clock, EVENTI[9]["sprites"], WIDTH, HEIGHT,
                                  bg, PERSONAGGI_SCELTI, ["Siete colpiti da un'onda!"])
                lista_merci = evento_ondata(lista_merci)

            elif evento_estratto == "INFESTAZIONE RATTI":
                anima_topo(schermo, clock, EVENTI[10]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                lista_merci = evento_infestazione_ratti(lista_merci)

            elif evento_estratto == "AVVISTAMENTO ALBATRO":
                animazione_albatro(schermo, clock, EVENTI[11]["sprites"], WIDTH, HEIGHT,
                                   PERSONAGGI_SCELTI, bg)
                carne_totale, albatro_avvistato, albatro_ucciso, fortuna_dellalbatro = \
                    evento_avvistamento_albatro(PERSONAGGI_SCELTI, lista_merci, carne_totale,
                                               albatro_avvistato, albatro_ucciso, fortuna_dellalbatro)

            elif evento_estratto == "AVVISTAMENTO SCIALUPPA":
                animazione_scialuppa(schermo, clock, EVENTI[12]["sprites"], WIDTH, HEIGHT)
                PERSONAGGI_SCELTI, lista_merci = evento_scialuppa(
                    PERSONAGGI_SCELTI, lista_merci, PERSONAGGI, MERCI)

            elif evento_estratto == "EPIDEMIA":
                animazione_epidemia(schermo, clock, PERSONAGGI_SCELTI, bg)
                PERSONAGGI_SCELTI, lista_merci = evento_epidemia(PERSONAGGI_SCELTI, lista_merci)

            elif evento_estratto == "ATTACCO PIRATA":
                animazione_attacco_pirata_caduta_proiettili(
                    schermo, clock, EVENTI[14]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                PERSONAGGI_SCELTI, lista_merci = evento_attacco_pirata(PERSONAGGI_SCELTI, lista_merci)

            elif evento_estratto == "DANNI AL TIMONE":
                animazione_timone_rotto(schermo, clock, EVENTI[15]["sprites"], WIDTH, HEIGHT,
                                        bg, PERSONAGGI_SCELTI,
                                        ["Il timone e' stato danneggiato!"], durata_ms=7000)
                numero_settimane = evento_danni_timone(numero_settimane, PERSONAGGI_SCELTI)

            elif evento_estratto == "RAFFICHE DI VENTO":
                animazione_divento(schermo, clock, EVENTI[16]["sprites"], WIDTH, HEIGHT,
                                   PERSONAGGI_SCELTI, bg, 5000, title_font, favorevole=False)
                numero_settimane = evento_raffiche_vento(numero_settimane, PERSONAGGI_SCELTI)

            elif evento_estratto == "AVVISTAMENTO ISOLA":
                animazione_isola(schermo, clock, EVENTI[18]["sprites"], WIDTH, HEIGHT, 5000)
                numero_settimane, totale_medicinali = evento_avvistamento_isola(
                    lista_merci, totale_medicinali, numero_settimane,
                    albatro_avvistato, albatro_ucciso, MERCI)

            else:
                mostra_messaggio_evento("NESSUN IMPREVISTO",
                                        "Il mare e' calmo.",
                                        "Non succede nulla di speciale questa settimana.")

            settimane_rimaste = numero_settimane - settimana_corrente
            if settimane_rimaste < 1:
                settimane_rimaste = 1

            lista_cibo_unificata = []
            for c in CIBO_SCELTO + BIBITE_SCELTE:
                lista_cibo_unificata.append(c)

            razioni_attuali = gestisci_razioni_interattivo(
                lista_cibo_unificata,
                PERSONAGGI_SCELTI,
                settimane_rimaste,
                razioni_attuali,
                PERSONAGGI_SCELTI
            )

            carne_totale, verdura_totale, frutta_totale = carica_totali_cibo(CIBO_SCELTO)
            acqua_totale = carica_acqua_totale(BIBITE_SCELTE)

            morti = applica_morti_morale_zero(PERSONAGGI_SCELTI)
            if morti > 0:
                mostra_messaggio_evento(
                    "MORTI PER DISPERAZIONE!",
                    f"Ci hanno lasciato: {morti} marinai",
                    "Il loro morale e' arrivato a 0."
                )

            if conta_membri_vivi(PERSONAGGI_SCELTI) == 0:
                mostra_messaggio_evento(
                    "GAME OVER",
                    "Tutto l'equipaggio e' morto.",
                    "La nave e' un cimitero galleggiante.",
                    ["Fine"]
                )
                running = False

            totale_medicinali, totale_armi, totale_merci = carica_totali_equip(lista_merci)
            saturazione_totale = aggiorna_saturazione(verdura_totale, acqua_totale,
                                                       carne_totale, frutta_totale)
            vivi_count = conta_membri_vivi(PERSONAGGI_SCELTI)

            info_membri = [
                f"{p['info']['name']} (Morale: {p['stats']['morale']})"
                for p in PERSONAGGI_SCELTI if p["stats"]["alive"]
            ] or ["Nessun superstite"]

            dettaglio = info_membri[0]
            if len(info_membri) > 1:
                dettaglio += " | " + info_membri[1]

            mostra_messaggio_evento(
                f"FINE SETTIMANA {settimana_corrente}",
                f"Vivi: {vivi_count}  |  Cibo: {saturazione_totale:.1f}  |  Merci: {totale_merci}",
                f"Morale: {dettaglio}"
            )

            ammutinamento, punteggio_amm, motivi_amm = step_ammutinamento(
                PERSONAGGI_SCELTI,
                albatro_ucciso,
                numero_settimane,
                razioni_attuali
            )

            numero_settimane = step_ricalcolo_settimane(PERSONAGGI_SCELTI, numero_settimane)

            settimana_corrente += 1

            random.shuffle(posizioni)
            assegna_posizioni(PERSONAGGI_SCELTI, posizioni)
            shell_sort_per_profondita(PERSONAGGI_SCELTI)

            if ammutinamento:
                running = False
            elif settimana_corrente > numero_settimane:
                mostra_messaggio_evento(
                    "VIAGGIO COMPLETATO!",
                    "Siete arrivati a destinazione!",
                    f"Superstiti: {conta_membri_vivi(PERSONAGGI_SCELTI)}  |  Merci: {totale_merci}",
                    ["Fine"]
                )
                running = False

            schermata_nera(durata_ms=3000)
            schermata = 1

    pygame.display.update()
    clock.tick(60)

pygame.quit()