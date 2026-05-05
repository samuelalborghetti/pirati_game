import pygame
import json
import random
import copy
from struttura_dati import PERSONAGGI, CIBO, BIBITE, MERCI, EVENTI
from gestione_eventi import *
from utility import HEIGHT, WIDTH, MOD, BIANCO, font_numeri, title_font
from eventi import *


numero_settimane = 8
settimana_corrente = 1
totale_medicinali = 0
totale_armi = 0
totale_merci = 0

albatro_avvistato = 0
albatro_ucciso = None
fortuna_dellalbatro = False

# VARIABILI NUOVE PER IL MORALE E LE SCORTE
diminuzione_morale = 0
razioni_attuali = {"verdura": 1.0, "frutta": 1.0, "carne": 1.0, "acqua": 1.0}

# --- CREAZIONE MAZZO EVENTI ---
mazzo_eventi = [
    "UOMO IN MARE", "VERDURA IN MARE", "FRUTTA IN MARE", "CARNE IN MARE", "ACQUA IN MARE",
    "PESCA MIRACOLOSA", "TEMPESTA MIRACOLOSA", "VENTI FAVOREVOLI", "CATTIVO TEMPO", "ONDATA",
    "INFESTAZIONE RATTI", "AVVISTAMENTO ALBATRO", "AVVISTAMENTO SCIALUPPA", "EPIDEMIA",
    "ATTACCO PIRATA", "DANNI AL TIMONE", "RAFFICHE DI VENTO", "AVVISTAMENTO ISOLA",
    "NESSUN IMPREVISTO", "NESSUN IMPREVISTO", "NESSUN IMPREVISTO", 
    "NESSUN IMPREVISTO", "NESSUN IMPREVISTO", "NESSUN IMPREVISTO"
]


def Carica_equip(percorso):
    file = open(percorso, "r", encoding="utf-8")
    dati = json.loads(file.read())
    file.close()
    return dati["personaggi"], dati["cibo"], dati["equip"], dati["soldi"]

def carica_totali_cibo(Cibo_scelto):
    totale_verdura = 0
    totale_carne = 0
    totale_frutta = 0
    
    for c in Cibo_scelto:
        tipo = c["stats"].get("tipo_cibo", "altro")
        
        if tipo == "verdura":
            totale_verdura += c["stats"]["saturazione"]
        elif tipo == "carne":
            totale_carne += c["stats"]["saturazione"]
        elif tipo == "frutta":
            totale_frutta += c["stats"]["saturazione"]
            
    return totale_carne, totale_verdura, totale_frutta

def carica_acqua_totale(Bibite_scelto):
    acqua_totale = 0
    for b in Bibite_scelto:
        if b["info"]["name"] == "acqua":
            acqua_totale += b["stats"]["saturazione"]
    return acqua_totale


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


CIBO_SCELTO = []
for nome in cibo_scelto:
    for c in CIBO:
        if c["info"]["name"] == nome:
            CIBO_SCELTO.append(c)
    

BIBITE_SCELTE = []
for nome in cibo_scelto:
    for b in BIBITE:
        if b["info"]["name"] == nome:
            BIBITE_SCELTE.append(b)
            

lista_merci  = []
for nome in equip_scelto:
    for e in MERCI:
        if e["info"]["name"] == nome:
            lista_merci.append(e)


carne_totale, verdura_totale, frutta_totale = carica_totali_cibo(CIBO_SCELTO)
acqua_totale = carica_acqua_totale(BIBITE_SCELTE)
saturazione_totale = verdura_totale + acqua_totale + carne_totale + frutta_totale

def aggiorna_saturazione(verdura_totale, acqua_totale, carne_totale, frutta_totale):
    cibo_totale = verdura_totale + acqua_totale + carne_totale + frutta_totale
    return cibo_totale

def carica_totali_equip(equip_scelto):
    totale_medicinali = 0
    totale_armi = 0
    totale_merci = 0
    
    for e in equip_scelto:
        if e["info"]["name"] == "medicinale":
            totale_medicinali += 1
        elif e["info"]["name"] == "armi":
            totale_armi += 1
            
    totale_merci = len(equip_scelto)
    return totale_medicinali, totale_armi, totale_merci

totale_medicinali, totale_armi, totale_merci = carica_totali_equip(lista_merci)


pygame.init()
pygame.display.set_icon(pygame.image.load("assets/sfondi/icon.png"))

schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("main")
clock = pygame.time.Clock()

bg = pygame.transform.scale(pygame.image.load("assets/sfondi/main.png"), (WIDTH, HEIGHT))
bg_caduta = pygame.transform.scale(pygame.image.load("assets/sfondi/sfondo_per_caduta.png"), (WIDTH, HEIGHT))

play = pygame.transform.scale(pygame.image.load("assets/tasti/play.png"), (int(150 * MOD), int(75 * MOD)))
rect_play = play.get_rect(topleft=(WIDTH - 200 * MOD, HEIGHT - 100 * MOD))

bt_wiew_equip = pygame.transform.scale(pygame.image.load("assets/tasti/play.png"), (int(150 * MOD), int(75 * MOD)))
rect_bt_wiew_equip = bt_wiew_equip.get_rect(topleft=(50 * MOD, HEIGHT - 100 * MOD))

SCAFFALE_MONEY = pygame.transform.scale(pygame.image.load("assets/tasti/scaffalemain.png"), (int(330 * MOD), int(210 * MOD)))


posizioni = [
    (400*MOD, 420*MOD), (455*MOD, 420*MOD), (500*MOD, 430*MOD), (550*MOD, 430*MOD),
    (70*MOD,  340*MOD), (165*MOD, 330*MOD), (23*MOD,  365*MOD), (600*MOD, 480*MOD),
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
            personaggi[j]= temp
        gap //= 2

def assegna_posizioni(pers, posizioni):
    for i in range(min(len(pers), len(posizioni))):
        pers[i]["pos"]["main"]["x_attuale"] = posizioni[i][0]
        pers[i]["pos"]["main"]["y_attuale"] = posizioni[i][1]

def DrawMoney(screen, soldi_correnti):
    testo = font_numeri.render(f"Soldi: {soldi_correnti:.1f}", True, BIANCO)
    rett  = testo.get_rect(topright=(screen.get_width() - 35*MOD, 22*MOD))
    screen.blit(testo, rett)

def draw_settimana(screen, settimana_corrente):
    testo = font_numeri.render(f"Settimana: {settimana_corrente}/{numero_settimane}", True, BIANCO)
    rett  = testo.get_rect(topright=(screen.get_width() - 20*MOD, 85*MOD))
    screen.blit(testo, rett)

def draw_cibo_totale(screen, saturazione_totale):
    testo = font_numeri.render(f"Cibo: {saturazione_totale:.1f}", True, BIANCO)
    rett  = testo.get_rect(topright=(screen.get_width() - 58*MOD, 147*MOD))
    screen.blit(testo, rett)

def draw_cibo_info_box(screen, mouse_pos, saturazione_totale, acqua_totale, verdura_totale, frutta_totale, carne_totale, rect_cibo):
    if rect_cibo.collidepoint(mouse_pos):
        rect_info = pygame.Rect(rect_cibo.x + 20*MOD, rect_cibo.y + rect_cibo.height + 19*MOD, 200*MOD, 170*MOD)
        pygame.draw.rect(screen, (161, 88, 0), rect_info, 0, 10)
        pygame.draw.rect(screen, (0, 0, 0), rect_info, 3, 10)
        
        titolo = title_font.render("Risorse", True, BIANCO)
        cibo_text = title_font.render(f"Cibo totale: {saturazione_totale:.1f}", True, BIANCO)
        acqua_text = title_font.render(f"Acqua: {acqua_totale:.1f}", True, BIANCO)
        verdura_text = title_font.render(f"Verdura: {verdura_totale:.1f}", True, BIANCO)
        frutta_text = title_font.render(f"Frutta: {frutta_totale:.1f}", True, BIANCO)
        carne_text = title_font.render(f"Carne: {carne_totale:.1f}", True, BIANCO)
        screen.blit(titolo, (rect_info.x + 10*MOD, rect_info.y + 10*MOD))
        screen.blit(cibo_text, (rect_info.x + 10*MOD, rect_info.y + 40*MOD))
        screen.blit(acqua_text, (rect_info.x + 10*MOD, rect_info.y + 65*MOD))
        screen.blit(verdura_text, (rect_info.x + 10*MOD, rect_info.y + 90*MOD))
        screen.blit(frutta_text, (rect_info.x + 10*MOD, rect_info.y + 115*MOD))
        screen.blit(carne_text, (rect_info.x + 10*MOD, rect_info.y + 140*MOD))

def draw_equip_info_box(screen, mouse_pos, medicinali_totali, armi_totali, strumenti_totali, rect_bt):
    if rect_bt.collidepoint(mouse_pos):
        box_width = 220 * MOD
        box_height = 120 * MOD
        
        rect_info = pygame.Rect(rect_bt.x, rect_bt.y - box_height - 10 * MOD, box_width, box_height)
        
        pygame.draw.rect(screen, (161, 88, 0), rect_info, 0, 10)
        pygame.draw.rect(screen, (0, 0, 0), rect_info, 3, 10)
        
        titolo = title_font.render("Equipaggiamento", True, BIANCO)
        med_text = title_font.render(f"Medicinali: {medicinali_totali}", True, BIANCO)
        armi_text = title_font.render(f"Armi: {armi_totali}", True, BIANCO)
        strum_text = title_font.render(f"totale: {strumenti_totali}", True, BIANCO)
        
        screen.blit(strum_text, (rect_info.x + 10*MOD, rect_info.y + 90*MOD))
        screen.blit(titolo, (rect_info.x + 10*MOD, rect_info.y + 10*MOD))
        screen.blit(med_text, (rect_info.x + 10*MOD, rect_info.y + 40*MOD))
        screen.blit(armi_text, (rect_info.x + 10*MOD, rect_info.y + 65*MOD))
        
        
def DrawButton(schermo, play, x, y):
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
                schermata_nera(schermo, clock)
                animazione_attiva = False
                schermata = 2

    if schermata == 1:
        schermo.blit(bg, (0,0))
        for p in PERSONAGGI_SCELTI:
            if p["stats"]["alive"]:
                disegna_animazione(schermo, p["sprites"], "idle", 135 , (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        schermo.blit(SCAFFALE_MONEY, (WIDTH - 260 * MOD, - 10 * MOD))
        DrawMoney(schermo, soldi_rimanenti)
        draw_settimana(schermo, settimana_corrente)
        rect_cibo = pygame.Rect(WIDTH - 240*MOD, 147*MOD, 200*MOD, 30*MOD)
        draw_cibo_totale(schermo, saturazione_totale)
        draw_cibo_info_box(schermo, pygame.mouse.get_pos(), saturazione_totale, acqua_totale, verdura_totale, frutta_totale, carne_totale, rect_cibo)
        DrawButton(schermo, play, WIDTH - 200 * MOD, HEIGHT - 100 * MOD)
        DrawButton(schermo, bt_wiew_equip, 50 * MOD, HEIGHT - 100 * MOD)
        draw_equip_info_box(schermo, pygame.mouse.get_pos(), totale_medicinali, totale_armi, totale_merci, rect_bt_wiew_equip)
        
    elif schermata == 2:
        if not animazione_attiva:
            animazione_attiva = True 
            
            # --- STEP 1: ESTRAZIONE EVENTO CASUALE ---
            if len(mazzo_eventi) == 0:
                evento_estratto = "NESSUN IMPREVISTO"
            else:
                evento_estratto = random.choice(mazzo_eventi)
            
            # Gestione rimozione dal mazzo
            if evento_estratto == "AVVISTAMENTO ALBATRO":
                if albatro_avvistato >= 2: # Max 3 volte
                    mazzo_eventi.remove(evento_estratto)
            elif evento_estratto != "NESSUN IMPREVISTO":
                mazzo_eventi.remove(evento_estratto)
                
            # --- ESECUZIONE EVENTO ---
            if evento_estratto == "UOMO IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[0]["sprites"], WIDTH, HEIGHT, bg_caduta, f"idle{str(random.randint(1,2))}", int(75*MOD), int(96*MOD), ["Un uomo e' caduto in mare!"])
                PERSONAGGI_SCELTI, nome_morto = evento_uomo_in_mare(PERSONAGGI_SCELTI)
                
            elif evento_estratto == "VERDURA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[1]["sprites"], WIDTH, HEIGHT, bg_caduta, "verdura", int(75*MOD), int(96*MOD), ["Tempesta! Verdura in mare!"])
                verdura_totale -= evento_verdura_in_mare(verdura_totale)
                
            elif evento_estratto == "FRUTTA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[2]["sprites"], WIDTH, HEIGHT, bg_caduta, "frutta", int(75*MOD), int(96*MOD), ["Tempesta! Frutta in mare!"])
                frutta_totale -= evento_frutta_in_mare(frutta_totale)
                
            elif evento_estratto == "CARNE IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[3]["sprites"], WIDTH, HEIGHT, bg_caduta, "carne", int(75*MOD), int(96*MOD), ["Tempesta! Carne in mare!"])
                carne_totale -= evento_carne_in_mare(carne_totale)
                
            elif evento_estratto == "ACQUA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[4]["sprites"], WIDTH, HEIGHT, bg_caduta, "acqua", int(50*MOD), int(86*MOD), ["Tempesta! Acqua in mare!"])
                acqua_totale -= evento_acqua_in_mare(acqua_totale)
                
            elif evento_estratto == "PESCA MIRACOLOSA":
                anima_pescamiracolosa(schermo, clock, EVENTI[5]["sprites"], WIDTH, HEIGHT)
                carne_totale = evento_pesca_miracolosa(carne_totale)
                
            elif evento_estratto == "TEMPESTA MIRACOLOSA":
                anima_tempesta_miracolosa(schermo, clock, EVENTI[6]["sprites"], WIDTH, HEIGHT, bg, "barile", int(165*MOD), PERSONAGGI_SCELTI, int(190*MOD))
                acqua_totale = evento_tempesta_miracolosa(acqua_totale)
                
            elif evento_estratto == "VENTI FAVOREVOLI":
                animazione_divento(schermo, clock, EVENTI[17]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg, 5000, title_font, favorevole=True)
                numero_settimane, bonus = evento_venti_favorevoli(numero_settimane)
                diminuzione_morale += bonus
                
            elif evento_estratto == "CATTIVO TEMPO":
                anima_cattivo_tempo(schermo, clock, EVENTI[8]["sprites"], WIDTH, HEIGHT, bg, PERSONAGGI_SCELTI, ["Il cattivo tempo rovescia medicinali!"])
                lista_merci = evento_cattivo_tempo(lista_merci)
                
            elif evento_estratto == "ONDATA":
                animazione_ondata(schermo, clock, EVENTI[9]["sprites"], WIDTH, HEIGHT, bg, PERSONAGGI_SCELTI, ["Siete colpiti da un'onda!"])
                lista_merci = evento_ondata(lista_merci)
                
            elif evento_estratto == "INFESTAZIONE RATTI":
                anima_topo(schermo, clock, EVENTI[10]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                lista_merci = evento_infestazione_ratti(lista_merci)
                
            elif evento_estratto == "AVVISTAMENTO ALBATRO":
                animazione_albatro(schermo, clock, EVENTI[11]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                carne_totale, albatro_avvistato, albatro_ucciso, fortuna_dellalbatro = evento_avvistamento_albatro(PERSONAGGI_SCELTI, lista_merci, carne_totale, albatro_avvistato, albatro_ucciso, fortuna_dellalbatro)
                
            elif evento_estratto == "AVVISTAMENTO SCIALUPPA":
                animazione_scialuppa(schermo, clock, EVENTI[12]["sprites"], WIDTH, HEIGHT)
                PERSONAGGI_SCELTI, lista_merci = evento_scialuppa(PERSONAGGI_SCELTI, lista_merci, PERSONAGGI, MERCI)
                
            elif evento_estratto == "EPIDEMIA":
                animazione_epidemia(schermo, clock, PERSONAGGI_SCELTI, bg)
                PERSONAGGI_SCELTI, lista_merci = evento_epidemia(PERSONAGGI_SCELTI, lista_merci)
                
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
                numero_settimane, totale_medicinali = evento_avvistamento_isola(lista_merci, totale_medicinali, numero_settimane, albatro_avvistato, albatro_ucciso, MERCI)

            elif evento_estratto == "NESSUN IMPREVISTO":
                mostra_messaggio_evento("NESSUN IMPREVISTO", "Il mare e' calmo.", "Non succede nulla in questa settimana.")
            

            # --- STEP 2: CONSUMO E CONTROLLO SCORTE ---
            vivi_lista = [p for p in PERSONAGGI_SCELTI if p["stats"]["alive"]]
            vivi = len(vivi_lista)
            settimane_rimaste = max(1, numero_settimane - settimana_corrente)

            consumi_base = {"verdura": 0.5, "frutta": 1.0, "carne": 1.0, "acqua": 0.5}
            scorte_attuali = {"verdura": verdura_totale, "frutta": frutta_totale, "carne": carne_totale, "acqua": acqua_totale}

            cuoco_vivo = any(p["info"].get("role") == "cuoco" and p["stats"]["alive"] for p in PERSONAGGI_SCELTI)
            if not cuoco_vivo:
                for res in ["verdura", "frutta", "carne"]:
                    consumi_base[res] *= 1.2 

            for nome, base in consumi_base.items():
                moltiplicatore = razioni_attuali[nome]
                consumo_settimana = base * moltiplicatore * vivi
                
                scorte_attuali[nome] -= consumo_settimana
                
                if scorte_attuali[nome] <= 0:
                    scorte_attuali[nome] = 0
                    diminuzione_morale -= 15
                    for p in PERSONAGGI_SCELTI:
                        if p["stats"]["alive"]:
                            if random.random() < 0.20:  
                                p["stats"]["alive"] = False
                                mostra_messaggio_evento(
                                    f"MORTE PER INEDIA", 
                                    f"{p['info']['name']} è deceduto per mancanza di {nome}.", 
                                    "Il morale dei superstiti crolla."
                                )
                                diminuzione_morale -= 10
                else:
                    futuro_necessario = base * moltiplicatore * vivi * settimane_rimaste-1
                    if scorte_attuali[nome] < futuro_necessario:
                        scelta = mostra_messaggio_evento(
                            f"SCARSEGGIA {nome.upper()}", 
                            f"Residuo: {scorte_attuali[nome]:.1f} | Servono: {futuro_necessario:.1f}",
                            "Dimezzare le razioni? (-5 morale/sett)", 
                            ["Dimezza", "Mantieni"]
                        )
                        if scelta == "Dimezza":
                            razioni_attuali[nome] *= 0.5
                            diminuzione_morale -= MALUS_MORALE_DIMEZZA_RAZIONI
                            mostra_messaggio_evento("RAZIONE DIMEZZATA", f"{nome.upper()} ridotta.", "Morale a terra.")
                    elif scorte_attuali[nome] >= futuro_necessario * 2:
                        scelta = mostra_messaggio_evento(
                            f"ABBONDANZA {nome.upper()}", 
                            f"Residuo: {scorte_attuali[nome]:.1f} | Ne bastano: {futuro_necessario:.1f}",
                            "Raddoppiare le razioni? (+5 morale/sett)", 
                            ["Raddoppia", "Mantieni"]
                        )
                        if scelta == "Raddoppia":
                            razioni_attuali[nome] *= 2.0
                            diminuzione_morale += BONUS_MORALE_RADDOPPIA_RAZIONI
                            mostra_messaggio_evento("RAZIONE RADDOPPIATA", f"{nome.upper()} aumentata.", "Equipaggio felice!")

            verdura_totale = scorte_attuali["verdura"]
            frutta_totale = scorte_attuali["frutta"]
            carne_totale = scorte_attuali["carne"]
            acqua_totale = scorte_attuali["acqua"]

            # --- STEP 3: AGGIORNAMENTO MORALE E MORTI ---
            for p in PERSONAGGI_SCELTI:
                if "morale" in p:
                    morale_corrente = p["morale"]
                else:
                    morale_corrente = p["stats"]["morale"]
                nuovo_morale = max(0, min(100, morale_corrente + diminuzione_morale))
                
                if "morale" in p:
                    p["morale"] = nuovo_morale
                else:
                    p["stats"]["morale"] = nuovo_morale

            morti_questa_settimana = applica_morti_morale_zero(PERSONAGGI_SCELTI)
            if morti_questa_settimana:
                mostra_messaggio_evento(
                    "MORTI PER DISPERAZIONE!",
                    f"Ci hanno lasciato: {', '.join(morti_questa_settimana)}",
                    "Il loro morale e' arrivato a 0."
                )

            if conta_membri_vivi(PERSONAGGI_SCELTI) == 0:
                mostra_messaggio_evento("GAME OVER", "Tutto l'equipaggio e' morto.", "La nave e' un cimitero galleggiante.", ["Fine"])
                print("Tutti morti. Game Over!")
                running = False

            ammutinamento, punteggio, motivi = step_ammutinamento(
                personaggi_selezionati=PERSONAGGI_SCELTI,
                settimane_totali=numero_settimane,
                albatro_ucciso=albatro_ucciso, 
                razioni_attuali=razioni_attuali
            )

            numero_settimane = step_ricalcolo_settimane(PERSONAGGI_SCELTI, numero_settimane)

            random.shuffle(posizioni)
            assegna_posizioni(PERSONAGGI_SCELTI, posizioni)
            shell_sort_per_profondita(PERSONAGGI_SCELTI)
            
            saturazione_totale = aggiorna_saturazione(verdura_totale, acqua_totale, carne_totale, frutta_totale)
            totale_medicinali, totale_armi, totale_merci = carica_totali_equip(lista_merci)
            
            if settimana_corrente > numero_settimane or ammutinamento:
                print("Viaggio Terminato! O sei arrivato o c'è stato l'ammutinamento.")
                running = False

            schermata_nera(schermo, clock)
            schermata = 1
            
    pygame.display.update()
    clock.tick(60)

pygame.quit()