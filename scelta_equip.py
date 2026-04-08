import pygame
import json
import subprocess
import sys
from struttura_dati import PERSONAGGI, CIBO, EQUIPAGGIAMENTO, WIDTH_BUTTON, HEIGHT_BUTTON, WIDTH_INFO_CHARACHTER, HEIGHT_INFO_CHARACHETER
pygame.init()

IMPOSTAZIONI = "./dati/setting.json"
DATI_EQUIP = "./dati/equip.json"
MAIN_GIOCO = "./main.py"

def CaricaSettings(percorso):
    file = open(percorso, "r", encoding="utf-8")
    dati = json.load(file)
    file.close()
    return dati["width"], dati["height"], dati["audio"], dati["mod"]

def SalvaEquipaggiamento (percorso, pers: list, cibo: list, equip: list, soldi: float):
    file = open (percorso, "w", encoding="utf-8")
    dati = {"personaggi": pers, "cibo": cibo, "equip": equip, "soldi": soldi}
    info = json.dumps (dati)
    file.write (info)
    file.close ()

WIDTH, HEIGHT, VOLUME, MOD = CaricaSettings(IMPOSTAZIONI)

BIANCO = (255, 255, 255)
ROSSO_CHIARO = (255, 133, 122)
ROSSO_SCURO =  (255, 0, 0)
GIALLO = (255, 215, 0)
ROSA_SCURO = (255, 20, 147)

schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirates of the see")

pygame.mixer.music.load("./assets/music/menu_music.mp3")
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play(-1)

bg = pygame.image.load("assets/sfondi/default1.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bottone_marrone = pygame.image.load("assets/tasti/arrow_left.png").convert_alpha()
clock = pygame.time.Clock()
font_numeri = pygame.font.Font("assets/fonts/Barrio-Regular.ttf", 24 * MOD)
title_font = pygame.font.Font ("assets/fonts/PixelifySans-Medium.ttf", 18)
info_font = pygame.font.Font("assets/fonts/PixelifySans-SemiBold.ttf", 14 * MOD)

categoria_attiva = "personaggi"
cibo_scelto = []
personaggi_selezionati = []
pers_in_movimento = []
equip_scelto = []
soldi_iniziali = 2000
arrivato = False
tempo_errore = 0

BUTTON_RECTS = [pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(10 * MOD, 125 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(115 * MOD, 125 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
                pygame.rect.Rect(115 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(10 * MOD, 225 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(115 * MOD, 225 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
                pygame.rect.Rect(10 * MOD, 345 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(115 * MOD, 345 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(10 * MOD, 445 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)]
BUTTON_RECT_PLAY = pygame.rect.Rect (10 * MOD, HEIGHT - HEIGHT_BUTTON, 180 * MOD, 90 * MOD)
BUTTON_PLAY = pygame.transform.scale(pygame.image.load ("assets/tasti/play.png"), (BUTTON_RECT_PLAY.width, BUTTON_RECT_PLAY.height))



def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def reset_posizione_personaggio(personaggio_corrente):
    personaggio_corrente["pos"]["x"] = WIDTH // 10
    personaggio_corrente["pos"]["y"] = (HEIGHT // 2) + (HEIGHT // 10)
    personaggio_corrente["pos"]["x_fine"] = (WIDTH // 2) + (WIDTH // 10)
    personaggio_corrente["pos"]["y_fine"] = (HEIGHT // 2) - (HEIGHT // 16)

def riordina_per_profondita(pers):
    n = len(pers)
    for i in range(n - 1):
        n_scambi = 0
        for j in range(n - i - 1):
            if pers[j]["pos"]["y"] > pers[j + 1]["pos"]["y"]:
                pers[j], pers[j + 1] = pers[j + 1], pers[j]
                n_scambi += 1
        if n_scambi == 0:
            pass

def DrawMoney(screen, soldi_correnti):
    testo = font_numeri.render(f"Soldi: {soldi_correnti}", True, GIALLO)
    rett = testo.get_rect(topright=(screen.get_width() - 20, 20))
    screen.blit(testo, rett)

def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64*MOD, 78*MOD), flip=False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)

def disegna_spostamento_personaggio(p, velocita, durata_ms, schermo, flip=False):
    x = p["pos"]["x"]
    y = p["pos"]["y"]
    x_fine = p["pos"]["x_fine"]
    y_fine = p["pos"]["y_fine"]
    if x != x_fine:
        if x < x_fine:
            x += velocita * MOD
            if p["info"]["name"] in ["Mozzo", "Guardone"]:
                flip = True
            if x > x_fine:
                x = x_fine
        elif x > x_fine:
            x -= velocita * MOD
            flip = True
            if p["info"]["name"] == "Guardone":
                flip = False
        disegna_animazione(schermo, p["sprites"], "walk_cycle", durata_ms, (x, y), flip=flip)
    elif y != y_fine:
        if y < y_fine:
            y += velocita * MOD
            if y > y_fine:
                y = y_fine
        elif y > y_fine:
            y -= velocita * MOD
        disegna_animazione(schermo, p["sprites"], "walk_forward", durata_ms, (x, y), flip=flip)
    else:
        disegna_animazione(schermo, p["sprites"], "idle", durata_ms, (x, y), flip=flip)
    p["pos"]["x"] = x
    p["pos"]["y"] = y
    arrivato = (x == x_fine and y == y_fine)
    return arrivato

def Drawtext (schermo, text: list, y_in, x_testo, font_scelto, colore, spazio_tra_righe):
    y = y_in
    for riga in text:
        testo = font_scelto.render(riga, True, colore)
        schermo.blit (testo, (x_testo, y))
        y += spazio_tra_righe

def Drawtext_PFE (schermo, text: list, y_in, x_testo, font_scelto, colore, spazio_tra_righe, testo_colorato, possibilita_colorare):
    y = y_in
    for riga in text:
        if riga in possibilita_colorare:
            testo = font_scelto.render(riga, True, testo_colorato)
        else:
            testo = font_scelto.render(riga, True, colore)
        schermo.blit (testo, (x_testo, y))
        y += spazio_tra_righe

def WrapText (testo: str, font_testo, rect_testo):
    parole = testo.split (" ")
    testo_fin = ""
    riga_corrente = ""
    for parola in parole:
        prova_testo = riga_corrente + parola
        width_testo, height = font_testo.size (prova_testo)
        if width_testo > rect_testo.width - 15 * MOD:
            testo_fin += riga_corrente + "|"
            riga_corrente = parola + " " 
        else:
            riga_corrente += parola + " "
    
    testo_fin += riga_corrente
    testo_lista = testo_fin.split ("|")
    return testo_lista

def ViewInfoEquip(list_info, screen, rects_pulsanti):
    mouse_pos = pygame.mouse.get_pos()
    for pos, el in enumerate(list_info):
        if rects_pulsanti[pos].collidepoint(mouse_pos):
            rect_info = pygame.Rect(rects_pulsanti[pos].x + 100 * MOD, rects_pulsanti[pos].y, WIDTH_INFO_CHARACHTER, HEIGHT_INFO_CHARACHETER)
            pygame.draw.rect(screen, (161, 88, 0), rect_info, 0, 10)
            pygame.draw.rect(screen, (0,0,0), rect_info, 3, 10)
            nome = title_font.render(el["info"]["name"].title(), True, BIANCO)
            cost = font_numeri.render(str(el["stats"]["cost"]), True, ROSSO_CHIARO)
            screen.blit (cost, (rect_info.x + rect_info.width / 4 - cost.get_width(), rect_info.y + 10 * MOD))
            screen.blit(nome, (rect_info.x + rect_info.width/2 - nome.get_width()/2, rect_info.y + 10 * MOD))
            Drawtext (screen, WrapText (el["info"]["descrizione"], info_font, rect_info), rect_info.y + nome.get_height() * 2, rect_info.x + 10 * MOD, info_font, BIANCO, nome.get_height() / 2)
            if list_info == PERSONAGGI:
                Drawtext (screen, WrapText (el["info"]["abilita"], info_font, rect_info), rect_info.y + rect_info.height - nome.get_height() * 2.5, rect_info.x + 10 * MOD, info_font, BIANCO, nome.get_height() / 2)
                
def DrawButtonEquip(list_attiva, screen, rects_pulsanti):
    for pos, el in enumerate(list_attiva):
        raw = el["sprites"]["button"]
        button_img = pygame.transform.scale(raw, (rects_pulsanti[pos].width, rects_pulsanti[pos].height))
        screen.blit(button_img, rects_pulsanti[pos])
        
def DrawErrore(schermo, testo: list, font_scelto, colore, spazio_tra_righe, tempo_errore, durata_ms=2000,x=0,y=0):
    if tempo_errore and pygame.time.get_ticks() - tempo_errore < durata_ms:
        Drawtext(schermo, testo, y, x, font_scelto, colore, spazio_tra_righe)
        return tempo_errore
    return 0

def nuova_destinazione(p, pers):
    riordina_per_profondita(pers)
    p["pos"]["x_fine"] = p["pos"]["x_barca"]
    p["pos"]["y_fine"] = p["pos"]["y_barca"]

def SelectCharacheters(pos_pers, pers_sel, soldi, pers_move, click_mouse, lista_personaggi):
    costo = lista_personaggi[pos_pers]["stats"]["cost"]
    p = lista_personaggi [pos_pers]
    if click_mouse[0]:
        if soldi >= costo and not p in pers_sel:
            pers_move.append(p)
            pers_sel.append(p)
            soldi -= costo
    elif click_mouse[2]:
        if p in pers_move and p in pers_sel:
            pers_move.remove(p)
            pers_sel.remove(p)
            soldi += costo
            reset_posizione_personaggio(p)
    return soldi

def SelectEquipment(pos_equip, equip_sel, soldi, mouse_click, lista_equip):
    costo = lista_equip[pos_equip]["stats"]["cost"]
    e = lista_equip[pos_equip]
    if mouse_click[0]:
        if soldi >= costo and not e in equip_sel:
            equip_sel.append(e)
            soldi -= costo
    elif mouse_click[2]:
        if e in equip_sel:
            equip_sel.remove(e)
            soldi += costo
    return soldi

def SelectCibo(pos_cibi, ciboselezionato, soldi, mouse_click, lista_cibi):
    c = lista_cibi[pos_cibi]
    costo = c["stats"]["cost"]
    if mouse_click[0]:
        if soldi >= costo:
            ciboselezionato.append(c)
            soldi -= costo
    elif mouse_click[2]:
        if c in ciboselezionato:
            ciboselezionato.remove(c)
            soldi += costo

    return soldi

schermata = 1
gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                categoria_attiva = "personaggi"
            elif event.key == pygame.K_c:
                categoria_attiva = "cibo"
            elif event.key == pygame.K_e:
                categoria_attiva = "equipaggiamento"
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if BUTTON_RECT_PLAY.collidepoint (mouse):
                if len(personaggi_selezionati) != 0 and len(cibo_scelto) != 0 and len(equip_scelto) != 0:
                    p_sel = []
                    c_sel = []
                    e_sel = []
                    for p in personaggi_selezionati:
                        p_sel.append (p["info"]["name"])
                    for c in cibo_scelto:
                        c_sel.append (c["info"]["name"])
                    for e in equip_scelto:
                        e_sel.append (e["info"]["name"])
                    SalvaEquipaggiamento (DATI_EQUIP, p_sel, c_sel, e_sel, soldi_iniziali) # SALVA SOLO IL NOME PERCHE' SU JSON NON SI POSSONO SALVARE LE IMMAGINI PYGAME, E QUINDI TUTTO IL SUO DIZIONARIO, salvando il nome si può successivamente riavere il dizionario completo
                    subprocess.Popen([sys.executable, MAIN_GIOCO])
                    sys.exit()
                else:
                    tempo_errore = pygame.time.get_ticks()
                    
            else:
                for pos, el in enumerate (BUTTON_RECTS):
                    if el.collidepoint (mouse):
                        if categoria_attiva == "personaggi":
                            soldi_iniziali = SelectCharacheters (pos, personaggi_selezionati, soldi_iniziali, pers_in_movimento, click, PERSONAGGI)
                        elif categoria_attiva == "cibo":
                            soldi_iniziali = SelectCibo (pos, cibo_scelto, soldi_iniziali, click, CIBO)
                        elif categoria_attiva == "equipaggiamento":
                            soldi_iniziali = SelectEquipment (pos, equip_scelto, soldi_iniziali, click, EQUIPAGGIAMENTO)

    if categoria_attiva == "personaggi":
        lista_attiva = PERSONAGGI
    elif categoria_attiva == "cibo":
        lista_attiva = CIBO
    elif categoria_attiva == "equipaggiamento":
        lista_attiva = EQUIPAGGIAMENTO

    schermo.blit(bg, (0, 0))
    if len(pers_in_movimento) != 0:
        for p in pers_in_movimento:
            arrivato = disegna_spostamento_personaggio(p, 5, 150, schermo)
            if arrivato:
                nuova_destinazione(p, pers_in_movimento)
    DrawMoney(schermo, soldi_iniziali)
    DrawButtonEquip(lista_attiva, schermo, BUTTON_RECTS)
    Drawtext_PFE(schermo, ["P:PC","C:Food","E:Equip"], 15*MOD, 210*MOD,title_font, BIANCO, 20*MOD, ROSA_SCURO,"P:PC" if categoria_attiva == "personaggi" else"C:Food" if categoria_attiva == "cibo" else"E:Equip" if categoria_attiva == "equipaggiamento" else None)
    ViewInfoEquip (lista_attiva, schermo, BUTTON_RECTS)
    tempo_errore = DrawErrore(schermo, ["Seleziona almeno un", "- personaggio","- cibo", "- equipaggiamento!"], title_font, BIANCO, 22 * MOD, tempo_errore, x = WIDTH-200*MOD, y = HEIGHT-100*MOD)
    schermo.blit (BUTTON_PLAY, BUTTON_RECT_PLAY)

    pygame.display.update()
    clock.tick(60)

pygame.quit()