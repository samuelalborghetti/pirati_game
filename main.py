import pygame
import json
import random
import copy
from struttura_dati import PERSONAGGI, CIBO, BIBITE, MERCI, EVENTI
from gestione_eventi import *
from utility import HEIGHT, WIDTH, MOD, BIANCO, font_numeri, title_font, disegna_animazione_non_scale
from eventi import  evento_uomo_in_mare, evento_verdura_in_mare, evento_frutta_in_mare, evento_carne_in_mare, evento_acqua_in_mare, evento_pesca_miracolosa, evento_tempesta_miracolosa, evento_venti_favorevoli, evento_cattivo_tempo, evento_ondata, evento_infestazione_ratti, evento_avvistamento_albatro, evento_scialuppa, evento_epidemia, evento_attacco_pirata, evento_danni_timone, evento_raffiche_vento, evento_avvistamento_isola, step_ricalcolo_settimane, mostra_messaggio_evento, gestisci_razioni_interattivo, step_ammutinamento, disegna_schermata_nera_riepilogo_settimana, e_vivo, hai_bardo, hai_tesoriere

numero_settimane = 8
settimana_corrente = 0
ammutinamento = False
albatro_avvistato = 0
albatro_ucciso = None
bonus_morale = 0



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

totale_medicinali, totale_armi, totale_merci = carica_totali_equip(lista_merci)

razioni_attuali = {"verdura": verdura_totale, "frutta": frutta_totale, "carne": carne_totale, "acqua": acqua_totale}
saturazione_totale = razioni_attuali["verdura"] +  razioni_attuali["acqua"] +  razioni_attuali["carne"] +  razioni_attuali["frutta"]
merce_attuale = {"medicinali": totale_medicinali, "armi": totale_armi, "totale": totale_merci}
consumi_base = {"verdura": 0.5, "frutta": 1.0, "carne": 1.0, "acqua": 0.5}
flag_dimezzamento_razioni = {"verdura": False, "frutta": False, "carne": False, "acqua": False}

pygame.init()
pygame.display.set_icon(pygame.image.load("assets/sfondi/icon.png"))
schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirates of the Sea")
clock = pygame.time.Clock()

bg = pygame.transform.scale(pygame.image.load("assets/sfondi/main.png"), (WIDTH, HEIGHT))
bg_caduta = pygame.transform.scale(pygame.image.load("assets/sfondi/sfondo_per_caduta.png"), (WIDTH, HEIGHT))

play = pygame.transform.scale(pygame.image.load("assets/tasti/burrom_skip.png"), (int(150*MOD), int(75*MOD)))
rect_play = play.get_rect(topleft=(WIDTH - 200*MOD, HEIGHT - 100*MOD))
bt_wiew_equip = pygame.transform.scale(pygame.image.load("assets/tasti/butto_wiew_equiip.png"), (int(150*MOD), int(75*MOD)))
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

def draw_cibo_info_box(screen, mouse_pos, sat, acqua = razioni_attuali["acqua"], verdura = razioni_attuali["verdura"], frutta = razioni_attuali["frutta"], carne = razioni_attuali["carne"], rect_cibo =(WIDTH - 240*MOD, 147*MOD, 200*MOD, 30*MOD)):
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
    txt1 = title_font.render(f"Medicinali: {med:.1f}", True, BIANCO)
    txt2 = title_font.render(f"Armi: {armi:.1f}", True, BIANCO)
    txt3 = title_font.render(f"Totale merci: {merci_tot:.1f}", True, BIANCO)

    x = r.x + 10*MOD
    screen.blit(txt0, (x, r.y + 10*MOD))
    screen.blit(txt1, (x, r.y + 40*MOD))
    screen.blit(txt2, (x, r.y + 67*MOD))
    screen.blit(txt3, (x, r.y + 92*MOD))

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
                disegna_animazione_non_scale(schermo, p["sprites"], "idle", 135,(p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        schermo.blit(SCAFFALE_MONEY, (WIDTH - 260*MOD, -10*MOD))
        DrawMoney(schermo, soldi_rimanenti)
        draw_settimana(schermo, settimana_corrente)
        rect_cibo = pygame.Rect(WIDTH - 240*MOD, 147*MOD, 200*MOD, 30*MOD)
        draw_cibo_totale(schermo, saturazione_totale)
        draw_cibo_info_box(schermo, pygame.mouse.get_pos(),saturazione_totale, razioni_attuali["acqua"],razioni_attuali["verdura"],razioni_attuali["frutta"], razioni_attuali["carne"], rect_cibo)
        schermo.blit(play, rect_play.topleft)
        schermo.blit(bt_wiew_equip, rect_bt_wiew_equip.topleft)
        draw_equip_info_box(schermo, pygame.mouse.get_pos(), merce_attuale["medicinali"], merce_attuale["armi"], merce_attuale["totale"], rect_bt_wiew_equip)

    elif schermata == 2:
        if not animazione_attiva:
            animazione_attiva = True

            if not mazzo_eventi:
                evento_estratto = "NESSUN IMPREVISTO"
            else:
                evento_estratto = random.choice(mazzo_eventi)

            if evento_estratto == "AVVISTAMENTO ALBATRO":
                albatro_avvistato += 1
                if albatro_avvistato >= 2:
                    mazzo_eventi.remove(evento_estratto)
            elif evento_estratto != "NESSUN IMPREVISTO":
                mazzo_eventi.remove(evento_estratto)

            if evento_estratto == "UOMO IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[0]["sprites"], WIDTH, HEIGHT, bg_caduta, f"idle{random.randint(1,2)}", int(75*MOD), int(96*MOD), ["Un uomo e' caduto in mare!"])
                PERSONAGGI_SCELTI, nome_vittima = evento_uomo_in_mare(PERSONAGGI_SCELTI)

            elif evento_estratto == "VERDURA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[1]["sprites"], WIDTH, HEIGHT,bg_caduta, "verdura", int(75*MOD), int(96*MOD),["Tempesta! Verdura in mare!"])
                razioni_attuali["verdura"] -= evento_verdura_in_mare(razioni_attuali["verdura"])
                

            elif evento_estratto == "FRUTTA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[2]["sprites"], WIDTH, HEIGHT,bg_caduta, "frutta", int(75*MOD), int(96*MOD),["Tempesta! Frutta in mare!"])
                razioni_attuali["frutta"] -= evento_frutta_in_mare(razioni_attuali["frutta"])

            elif evento_estratto == "CARNE IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[3]["sprites"], WIDTH, HEIGHT,bg_caduta, "carne", int(75*MOD), int(96*MOD),["Tempesta! Carne in mare!"])
                razioni_attuali["carne"] -= evento_carne_in_mare(razioni_attuali["carne"])

            elif evento_estratto == "ACQUA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[4]["sprites"], WIDTH, HEIGHT,bg_caduta, "acqua", int(50*MOD), int(86*MOD),["Tempesta! Acqua in mare!"])
                razioni_attuali["acqua"] -= evento_acqua_in_mare(razioni_attuali["acqua"])

            elif evento_estratto == "PESCA MIRACOLOSA":
                anima_pescamiracolosa(schermo, clock, EVENTI[5]["sprites"], WIDTH, HEIGHT)
                razioni_attuali["carne"] = evento_pesca_miracolosa(razioni_attuali["carne"])

            elif evento_estratto == "TEMPESTA MIRACOLOSA":
                anima_tempesta_miracolosa(schermo, clock, EVENTI[6]["sprites"], WIDTH, HEIGHT, bg, "barile", int(165*MOD), PERSONAGGI_SCELTI, int(190*MOD))
                razioni_attuali["acqua"] = evento_tempesta_miracolosa(razioni_attuali["acqua"])

            elif evento_estratto == "VENTI FAVOREVOLI":
                animazione_divento(schermo, clock, EVENTI[17]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg, 5000, title_font, favorevole=True)
                numero_settimane, bonus_morale = evento_venti_favorevoli(numero_settimane, bonus_morale)

            elif evento_estratto == "CATTIVO TEMPO":
                anima_cattivo_tempo(schermo, clock, EVENTI[8]["sprites"], WIDTH, HEIGHT,bg, PERSONAGGI_SCELTI, ["Il cattivo tempo rovescia medicinali!"])
                lista_merci = evento_cattivo_tempo(lista_merci)

            elif evento_estratto == "ONDATA":
                animazione_ondata(schermo, clock, EVENTI[9]["sprites"], WIDTH, HEIGHT, bg, PERSONAGGI_SCELTI, ["Siete colpiti da un'onda!"])
                lista_merci = evento_ondata(lista_merci)

            elif evento_estratto == "INFESTAZIONE RATTI":
                anima_topo(schermo, clock, EVENTI[10]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                lista_merci = evento_infestazione_ratti(lista_merci)

            elif evento_estratto == "AVVISTAMENTO ALBATRO":
                animazione_albatro(schermo, clock, EVENTI[11]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                razioni_attuali["carne"], albatro_avvistato, albatro_ucciso = evento_avvistamento_albatro(PERSONAGGI_SCELTI, lista_merci, razioni_attuali["carne"], albatro_avvistato, albatro_ucciso)

            elif evento_estratto == "AVVISTAMENTO SCIALUPPA":
                animazione_scialuppa(schermo, clock, EVENTI[12]["sprites"], WIDTH, HEIGHT)
                PERSONAGGI_SCELTI, lista_merci = evento_scialuppa(
                    PERSONAGGI_SCELTI, lista_merci, PERSONAGGI, MERCI)

            elif evento_estratto == "EPIDEMIA":
                animazione_epidemia(schermo, clock, PERSONAGGI_SCELTI, bg)
                PERSONAGGI_SCELTI, lista_merci = evento_epidemia(PERSONAGGI_SCELTI, lista_merci)
                n_vivi = 0
                for p in PERSONAGGI_SCELTI:
                    if p["stats"]["alive"]:
                        n_vivi += 1
                if n_vivi == 0:
                    mostra_messaggio_evento(
                        titolo="TUTTI MORTI EPIDEMIA TI HA DISTRUTTO!",
                        domanda="Tutti i membri dell'equipaggio sono morti!",
                        motivo="La nave e' alla deriva senza nessuno a guidarla. ",
                        scelte=["Fine partita"]
                    )
                    running = False

            elif evento_estratto == "ATTACCO PIRATA":
                animazione_attacco_pirata_caduta_proiettili(schermo, clock, EVENTI[14]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                PERSONAGGI_SCELTI, lista_merci = evento_attacco_pirata(PERSONAGGI_SCELTI, lista_merci)

            elif evento_estratto == "DANNI AL TIMONE":
                animazione_timone_rotto(schermo, clock, EVENTI[15]["sprites"], WIDTH, HEIGHT, bg, PERSONAGGI_SCELTI, ["Il timone e' stato danneggiato!"], durata_ms=7000)
                numero_settimane = evento_danni_timone(numero_settimane, PERSONAGGI_SCELTI)

            elif evento_estratto == "RAFFICHE DI VENTO":
                animazione_divento(schermo, clock, EVENTI[16]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg, 5000, title_font, favorevole=False)
                numero_settimane = evento_raffiche_vento(numero_settimane, PERSONAGGI_SCELTI)

            elif evento_estratto == "AVVISTAMENTO ISOLA":
                animazione_isola(schermo, clock, EVENTI[18]["sprites"], WIDTH, HEIGHT, 5000)
                numero_settimane, merce_attuale["medicinali"] = evento_avvistamento_isola(lista_merci, merce_attuale["medicinali"], numero_settimane,albatro_avvistato, albatro_ucciso, MERCI)

            else:
                mostra_messaggio_evento("NESSUN IMPREVISTO", "Il mare e' calmo.", "Non succede nulla di speciale questa settimana.")
            hai_bardo(PERSONAGGI_SCELTI)
            hai_tesoriere(PERSONAGGI_SCELTI, lista_merci, MERCI)
            n_vivi = 0
            for p in PERSONAGGI_SCELTI:
                if p["stats"]["alive"]:
                    n_vivi += 1
            if n_vivi == 0:
                mostra_messaggio_evento(
                    titolo="TUTTI MORTI!",
                    domanda="Tutti i membri dell'equipaggio sono morti!",
                    motivo="La nave e' alla deriva senza nessuno a guidarla.  ",
                    scelte=["Fine partita"]
                )
                running = False

            merce_attuale["medicinali"],merce_attuale["armi"],merce_attuale["totale"] = carica_totali_equip(lista_merci)
            saturazione_totale = razioni_attuali["verdura"] +  razioni_attuali["acqua"] +  razioni_attuali["carne"] +  razioni_attuali["frutta"]

            settimane_rimaste = numero_settimane - settimana_corrente 
            razioni_attuali, consumi_base, bonus_morale, flag_dimezzamento_razioni = gestisci_razioni_interattivo(PERSONAGGI_SCELTI, settimane_rimaste, razioni_attuali, consumi_base, bonus_morale, flag_dimezzamento_razioni)
            for pers in PERSONAGGI_SCELTI:
                if e_vivo(pers):
                    pers["stats"]["morale"] += bonus_morale
                    if pers["stats"]["morale"] > 100:
                        pers["stats"]["morale"] = 100
            saturazione_totale = razioni_attuali["verdura"] +  razioni_attuali["acqua"] +  razioni_attuali["carne"] +  razioni_attuali["frutta"]
            ammutinamento = step_ammutinamento(flag_dimezzamento_razioni, PERSONAGGI_SCELTI, albatro_ucciso, numero_settimane)
            
            numero_settimane = step_ricalcolo_settimane(PERSONAGGI_SCELTI,numero_settimane)
            disegna_schermata_nera_riepilogo_settimana(PERSONAGGI_SCELTI, razioni_attuali, consumi_base, merce_attuale)
            
            if ammutinamento:
                mostra_messaggio_evento(
                    titolo="AMMUTINAMENTO!",
                    domanda="L'equipaggio si e' ammutinato contro di te!",
                    motivo="L'equipaggio abbandona la nave.  ",
                    scelte=["Fine partita"]
                )
                running = False
                
            if settimana_corrente >= numero_settimane:
                mostra_messaggio_evento(
                    titolo="VIAGGIO COMPLETATO!",
                    domanda="Congratulazioni, avete completato il viaggio!",
                    motivo="L'equipaggio raggiunge la destinazione sano e salvo.  ",
                    scelte=["vai al nuovo mondo!"]
                )
                running = False
            
            settimana_corrente += 1
            assegna_posizioni(PERSONAGGI_SCELTI, posizioni)
            shell_sort_per_profondita(PERSONAGGI_SCELTI)
           
            schermata_nera(durata_ms=3000)
            schermata = 1
        
        elif schermata == 3:
            def baratto():
                LARGHEZZA, ALTEZZA = 1280, 853
                schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
                
                sfondo = pygame.image.load("assets/sfondi/schermata_baratto.png")
                sfondo = pygame.transform.scale(sfondo, (LARGHEZZA, ALTEZZA))
                
                SCALA_X = LARGHEZZA / 1536
                SCALA_Y = ALTEZZA / 1024
                
                # inventario del socio, le quantità sono a caso
                inventario = {
                    "sale": 100, 
                    "stoffa": 0,   
                    "coltelli": 80,  
                    "diamanti": 10,  
                }
                
                #tassi di cambio
                tassi = {
                    #              perle   manufatti  spezie
                    "sale":     [  0.5,     0.5,      1.0  ],  
                    "stoffa":   [  5,       7,        3    ],  
                    "coltelli": [  1,       3,        6    ],  
                    "diamanti": [  2,       4,        4    ],  
                }
                
                valore_patria = {
                    "perle":     2,
                    "manufatti": 2,
                    "spezie":    1,
                }
                
                VALUTE = ["perle", "manufatti", "spezie"]
                MERCI  = ["sale", "stoffa", "coltelli", "diamanti"]
                
                FONT_GRANDE = pygame.font.SysFont("Georgia", 28, bold=True)
                FONT_GRANDE2= pygame.font.SysFont("Georgia", 23, bold=True)
                FONT_MEDIO  = pygame.font.SysFont("Georgia", 20)
                FONT_PICCOLO= pygame.font.SysFont("Georgia", 17)
                
                COL_BG      = (30, 15, 5)
                COL_BORDO   = (180, 130, 60)
                COL_BORDO2  = (220, 170, 80)
                COL_TESTO   = (240, 210, 140)
                COL_TESTO2  = (200, 165, 100)
                COL_BTN     = (80, 45, 12)
                COL_HOVER   = (130, 75, 22)
                COL_VERDE   = (100, 200, 100)
                COL_GIALLO  = (240, 200, 80)
                COL_ROSSO   = (220, 80, 80)
                COL_SEL     = (60, 100, 40)
                COL_SEL_BRD = (100, 180, 70)
                
                #stato del baratto
                #- "scelta_merce" --> mostra i bottoni
                #- "scelta_opzione" --> mostra le 3 opzioni di baratto
                #- "fine" --> baratto completato
                
                fase = "scelta_merce"
                merce_corrente = None       
                opzione_scelta = None       
                merci_da_fare  = []         
                
                carico_nave = {}
                
                
                def calc_offerte(merce, quantita):
                    offerte = []
                    for i, valuta in enumerate(VALUTE):
                        tasso = tassi[merce][i]         
                        quantità   = math.floor(quantita / tasso)
                        profitto = quantità * valore_patria[valuta]
                        offerte.append({
                            "valuta":   valuta,
                            "quantita": quantità,
                            "profitto": profitto,
                        })
                    return offerte
                
                
                def draw_rect_alpha(surface, color, rect, alpha=180, radius=10):
                    s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
                    pygame.draw.rect(s, (*color, alpha), (0, 0, rect.w, rect.h), border_radius=radius)
                    surface.blit(s, (rect.x, rect.y))
                
                
                def draw_button(rect, text, font, selected=False, best=False):
                    mouse = pygame.mouse.get_pos()
                    if selected:
                        bg  = COL_SEL
                        brd = COL_SEL_BRD
                    elif rect.collidepoint(mouse):
                        bg  = COL_HOVER
                        brd = COL_BORDO2
                    else:
                        bg  = COL_BTN
                        brd = COL_BORDO
                
                    pygame.draw.rect(schermo, bg,  rect, border_radius=8)
                    pygame.draw.rect(schermo, brd, rect, 2, border_radius=8)
                
                    if best:
                        star = FONT_MEDIO.render("★", True, COL_GIALLO)
                        schermo.blit(star, (rect.x + 6, rect.y + rect.h//2 - star.get_height()//2))
                
                    t = font.render(text, True, COL_TESTO)
                    schermo.blit(t, (rect.x + rect.w//2 - t.get_width()//2,
                                     rect.y + rect.h//2 - t.get_height()//2))
                
                
                def testo_centrato(testo, font, y, colore=None):
                    colore = colore or COL_TESTO
                    t = font.render(testo, True, colore)
                    schermo.blit(t, (LARGHEZZA//2 - t.get_width()//2, y))
                
                
                def disegna_schermata_merci():
                
                    pw, ph = 520, 500
                    px = LARGHEZZA//2 - pw//2 - 320
                    py = ALTEZZA//2 - ph//2 + 80
                    draw_rect_alpha(schermo, COL_BG, pygame.Rect(px, py, pw, ph), 210, 16)
                    pygame.draw.rect(schermo, COL_BORDO, pygame.Rect(px, py, pw, ph), 2, border_radius=16)
                
                    # Titolo centrato nel riquadro
                    t1 = FONT_GRANDE.render("Il Capo Tribù è pronto a trattare", True, COL_TESTO)
                    schermo.blit(t1, (px + pw//2 - t1.get_width()//2, py + 20))
                    
                    # Sottotitolo centrato nel riquadro
                    t2 = FONT_MEDIO.render("Scegli la merce da barattare", True, COL_TESTO2)
                    schermo.blit(t2, (px + pw//2 - t2.get_width()//2, py + 58))
                
                    merci_nomi = {
                        "sale": "Sacchi di Sale",
                        "stoffa": "Teli di Stoffa",
                        "coltelli": "Coltelli",
                        "diamanti": "Diamanti",
                    }
                
                    bottone_rects = {}
                    for i, merce in enumerate(MERCI):
                        qta = inventario.get(merce, 0)
                        bx = px + 40
                        by = py + 110 + i * 85
                        bw = pw - 80
                        bh = 65
                        rect = pygame.Rect(bx, by, bw, bh)
                        bottone_rects[merce] = rect
                
                        disponibile = qta > 0
                        col_bg  = COL_BTN  if disponibile else (25, 12, 5)
                        col_brd = COL_BORDO if disponibile else (80, 55, 20)
                        mouse   = pygame.mouse.get_pos()
                
                        if disponibile and rect.collidepoint(mouse):
                            col_bg = COL_HOVER
                
                        pygame.draw.rect(schermo, col_bg, rect, border_radius=8)
                        pygame.draw.rect(schermo, col_brd, rect, 2, border_radius=8)
                
                        nome_t = FONT_MEDIO.render(merci_nomi[merce], True,
                                                   COL_TESTO if disponibile else (100, 75, 40))
                        schermo.blit(nome_t, (rect.x + 20, rect.y + rect.h//2 - nome_t.get_height()//2))
                
                        if disponibile:
                            qta_t = FONT_MEDIO.render(f"x{qta}", True, COL_GIALLO)
                        else:
                            qta_t = FONT_MEDIO.render("Non disponibile", True, (100, 75, 40))
                        schermo.blit(qta_t, (rect.right - qta_t.get_width() - 20,
                                             rect.y + rect.h//2 - qta_t.get_height()//2))
                
                    # Testo finale centrato nel riquadro
                    t3 = FONT_PICCOLO.render("Clicca su una merce per avviare il baratto", True, COL_TESTO2)
                    schermo.blit(t3, (px + pw//2 - t3.get_width()//2, py + ph - 35))
                
                    return bottone_rects    
                
                
                def disegna_schermata_opzioni():
                    global opzione_scelta
                
                    quantità  = inventario.get(merce_corrente, 0)
                    offerte = calc_offerte(merce_corrente, quantità)
                
                    migliore = max(range(3), key=lambda i: offerte[i]["profitto"])
                
                    pw, ph = 620, 530
                    px = LARGHEZZA//2 - pw//2 - 320
                    py = ALTEZZA//2 - ph//2 + 80
                    draw_rect_alpha(schermo, COL_BG, pygame.Rect(px, py, pw, ph), 215, 16)
                    pygame.draw.rect(schermo, COL_BORDO, pygame.Rect(px, py, pw, ph), 2, border_radius=16)
                
                    # Titolo centrato nel riquadro
                    t1 = FONT_GRANDE.render(f"Baratto: {merce_corrente} (x{quantità})", True, COL_TESTO)
                    schermo.blit(t1, (px + pw//2 - t1.get_width()//2, py + 18))
                    
                    # Sottotitolo centrato nel riquadro
                    t2 = FONT_MEDIO.render("Il Capo Tribù propone tre scambi:", True, COL_TESTO2)
                    schermo.blit(t2, (px + pw//2 - t2.get_width()//2, py + 55))
                
                    btn_rects  = []
                    btn_ok_rect = None
                
                    for i, offerta in enumerate(offerte):
                        bx = px + 30
                        by = py + 95 + i * 118
                        bw = pw - 60
                        bh = 100
                
                        rect = pygame.Rect(bx, by, bw, bh)
                        btn_rects.append(rect)
                
                        selezionato = (opzione_scelta == i)
                        è_migliore  = (i == migliore)
                        mouse = pygame.mouse.get_pos()
                
                        if selezionato:
                            col_bg  = COL_SEL
                            col_brd = COL_SEL_BRD
                        elif rect.collidepoint(mouse):
                            col_bg  = COL_HOVER
                            col_brd = COL_BORDO2
                        else:
                            col_bg  = COL_BTN
                            col_brd = COL_BORDO
                
                        pygame.draw.rect(schermo, col_bg, rect, border_radius=8)
                        pygame.draw.rect(schermo, col_brd, rect, 2, border_radius=8)
                
                        numero_opzione = FONT_GRANDE.render(f"{i+1})", True, COL_TESTO2)
                        schermo.blit(numero_opzione, (rect.x + 14, rect.y + 14))
                
                        valuta_nome = offerta["valuta"].capitalize()
                        desc = f"{offerta['quantita']} {valuta_nome}"
                        desc_t = FONT_GRANDE.render(desc, True, COL_TESTO)
                        schermo.blit(desc_t, (rect.x + 55, rect.y + 14))
                
                        prof_col = COL_VERDE if è_migliore else COL_TESTO2
                        prof_t = FONT_MEDIO.render(
                            f"Profitto stimato: {offerta['profitto']} monete d'oro", True, prof_col)
                        schermo.blit(prof_t, (rect.x + 55, rect.y + 55))
                
                        if è_migliore:
                            star_t = FONT_MEDIO.render("★ Miglior offerta", True, COL_GIALLO)
                            schermo.blit(star_t, (rect.right - star_t.get_width() - 14,
                                                   rect.y + 14))
                
                    btn_ok_y = py + ph - 62
                    btn_ok_rect = pygame.Rect(LARGHEZZA//2 - 160 - 100, btn_ok_y, 220, 45)
                    if opzione_scelta is not None:
                        draw_button(btn_ok_rect, "Conferma scelta", FONT_MEDIO)
                    else:
                        pygame.draw.rect(schermo, (40, 25, 8), btn_ok_rect, border_radius=8)
                        pygame.draw.rect(schermo, (70, 50, 20), btn_ok_rect, 2, border_radius=8)
                        t = FONT_MEDIO.render("Scegli un'opzione", True, (100, 80, 40))
                        schermo.blit(t, (btn_ok_rect.centerx - t.get_width()//2,
                                         btn_ok_rect.centery - t.get_height()//2))
                
                    btn_back = pygame.Rect(px + 20, btn_ok_y, 120, 45)
                    draw_button(btn_back, "<-- Indietro", FONT_MEDIO)
                
                    return btn_rects, btn_ok_rect, btn_back
                
                def disegna_Schermata_fine():
                    pw, ph = 500, 400
                    px = LARGHEZZA//2 - pw//2 
                    py = ALTEZZA//2 - ph//2
                
                    draw_rect_alpha(schermo, COL_BG, pygame.Rect(px, py, pw, ph), 215, 16)
                    pygame.draw.rect(schermo, COL_BORDO, pygame.Rect(px, py, pw, ph), 2, border_radius=16)
                
                    # Titolo centrato nel riquadro
                    t1 = FONT_GRANDE.render("Baratto completato!", True, COL_TESTO)
                    schermo.blit(t1, (px + pw//2 - t1.get_width()//2, py + 22))
                
                
                    # Sottotitolo centrato nel riquadro
                    t2 = FONT_MEDIO.render("Carico sulla nave:", True, COL_TESTO2)
                    schermo.blit(t2, (px + pw//2 - t2.get_width()//2, py + 65))
                    
                    profitto_totale = 0
                    y_off = py + 105
                    if not carico_nave:
                        t = FONT_MEDIO.render("Nessuna merce barattata.", True, COL_TESTO2)
                        schermo.blit(t, (px + 40, y_off))
                    else:
                        for valuta, qty in carico_nave.items():
                            prof = qty * valore_patria[valuta]
                            profitto_totale += prof
                            riga = f"{valuta.capitalize()}: {qty}  →  ~{prof} monete d'oro"
                            t = FONT_MEDIO.render(riga, True, COL_TESTO)
                            schermo.blit(t, (px + 40, y_off))
                            y_off += 38
                        
                    sep_y = py + ph - 130
                    pygame.draw.line(schermo, COL_BORDO, (px+30, sep_y), (px+pw-30, sep_y), 1)
                    
                    tot_t = FONT_GRANDE2.render(
                        f"Profitto totale stimato: {profitto_totale} monete d'oro", True, COL_VERDE)
                    schermo.blit(tot_t, (px + pw//2 - tot_t.get_width()//2, sep_y + 14))
                
                    # Nota centrata nel riquadro
                    t3 = FONT_PICCOLO.render("(I valori possono variare prima del ritorno)", True, COL_TESTO2)
                    schermo.blit(t3, (px + pw//2 - t3.get_width()//2, sep_y + 45))
                
                    btn_esci = pygame.Rect(LARGHEZZA//2 - 100, py + ph - 60, 200, 45)
                    draw_button(btn_esci, "Salpare!", FONT_MEDIO)
                    return btn_esci
                
                def avvia_prossima_merce():
                    global merce_corrente, fase, merci_da_fare
                    while merci_da_fare:
                        merce = merci_da_fare.pop(0)
                        if inventario.get(merce, 0) > 0:
                            merce_corrente = merce
                            fase = "scelta_opzione"
                            return
                    fase = "fine"
                
                
                merci_da_fare = list(MERCI)
                
                running = True
                while running:
                    schermo.blit(sfondo, (0, 0))
                
                    btn_merci  = {}
                    btn_opzioni = []
                    btn_ok = btn_back = btn_esci = None
                
                    # ── Disegno ──
                    if fase == "scelta_merce":
                        btn_merci = disegna_schermata_merci()
                
                    elif fase == "scelta_opzione":
                        btn_opzioni, btn_ok, btn_back = disegna_schermata_opzioni()
                
                    elif fase == "fine":
                        btn_esci = disegna_Schermata_fine()
                    
                    # ── Eventi ──
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            if fase == "scelta_opzione":
                                fase = "scelta_merce"
                                opzione_scelta = None
                                merci_da_fare = list(MERCI)
                
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            mouse = pygame.mouse.get_pos()
                
                            if fase == "scelta_merce":
                                for merce, rect in btn_merci.items():
                                    if rect.collidepoint(mouse) and inventario.get(merce, 0) > 0:
                                    
                                        idx = MERCI.index(merce)
                                        merci_da_fare = list(MERCI[idx:])
                                        avvia_prossima_merce()
                                        opzione_scelta = None
                
                            elif fase == "scelta_opzione":
                            
                                for i, rect in enumerate(btn_opzioni):
                                    if rect.collidepoint(mouse):
                                        opzione_scelta = i
                
                                # Conferma
                                if btn_ok and btn_ok.collidepoint(mouse) and opzione_scelta is not None:
                                    qta     = inventario[merce_corrente]
                                    offerte = calc_offerte(merce_corrente, qta)
                                    scelta  = offerte[opzione_scelta]
                
                                    valuta = scelta["valuta"]
                                    carico_nave[valuta] = carico_nave.get(valuta, 0) + scelta["quantita"]
                
                                    print(f"[BARATTO] {qta}x {merce_corrente} → "
                                          f"{scelta['quantita']} {valuta} "
                                          f"(profitto stimato: {scelta['profitto']} monete)")
                
                                    opzione_scelta = None
                                    avvia_prossima_merce()
                
                                # Indietro
                                if btn_back and btn_back.collidepoint(mouse):
                                    fase = "scelta_merce"
                                    opzione_scelta = None
                                    merci_da_fare = list(MERCI)
                
                            elif fase == "fine":
                                if btn_esci and btn_esci.collidepoint(mouse):
                                    print("[FINE BARATTO] Carico nave:", carico_nave)
                                    running = False
                
                    pygame.display.flip()
                
                pygame.quit()
                
            baratto()
            

    pygame.display.update()
    clock.tick(60)

pygame.quit()