import pygame
import json
import subprocess
import sys
import copy
from struttura_dati import PERSONAGGI, CIBO, BIBITE, EQUIPAGGIAMENTO, BARCA_POS, BUTTON_RECTS
from utility import WIDTH, HEIGHT, VOLUME, MOD, HEIGHT_BUTTON, WIDTH_INFO_CHARACHTER, HEIGHT_INFO_CHARACHETER, DATI_EQUIP, MAIN_GIOCO, BIANCO, ROSSO_CHIARO, ROSA_SCURO, SalvaEquipaggiamento, DrawMoney, WrapText, Drawtext, Drawtext_PFE, draw_con_tempo, disegna_animazione, font_numeri, title_font, info_font

def ordina_barca_pos(barca_pos):
    n = len(barca_pos)
    for i in range(n - 1):
        n_scambi = 0
        for j in range(n - i - 1):
            if barca_pos[j][1] > barca_pos[j + 1][1]:
                barca_pos[j], barca_pos[j + 1] = barca_pos[j + 1], barca_pos[j]
                n_scambi += 1
        if n_scambi == 0:
            break

def disegna_spostamento_personaggio(p, velocita, durata_ms, schermo, flip=False):
    x = p["pos"]["scelta_equip"]["x"]
    y = p["pos"]["scelta_equip"]["y"]
    x_fine = p["pos"]["scelta_equip"]["x_fine"]
    y_fine = p["pos"]["scelta_equip"]["y_fine"]
    if x != x_fine:
        if x < x_fine:
            x += velocita * MOD
            if x > x_fine:
                x = x_fine
        elif x > x_fine:
            x -= velocita * MOD
            flip = True
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
    arrivato = (x == x_fine and y == y_fine)
    return arrivato, x, y

def DrawButtonEquip(list_attiva, screen, rects_pulsanti):
    for pos, el in enumerate(list_attiva):
        if pos >= len(rects_pulsanti):
            break
        raw = el["sprites"]["button"]
        button_img = pygame.transform.scale(raw, (rects_pulsanti[pos].width, rects_pulsanti[pos].height))
        screen.blit(button_img, rects_pulsanti[pos])

def ViewInfoEquip(list_info, screen, rects_pulsanti):
    mouse_pos = pygame.mouse.get_pos()
    for pos, el in enumerate(list_info):
        if pos >= len(rects_pulsanti):
            break
        if rects_pulsanti[pos].collidepoint(mouse_pos):
            rect_info = pygame.Rect(rects_pulsanti[pos].x + 100 * MOD, rects_pulsanti[pos].y, WIDTH_INFO_CHARACHTER, HEIGHT_INFO_CHARACHETER)
            pygame.draw.rect(screen, (161, 88, 0), rect_info, 0, 10)
            pygame.draw.rect(screen, (0, 0, 0), rect_info, 3, 10)
            nome = title_font.render(el["info"]["name"].title(), True, BIANCO)
            cost = title_font.render(str(el["stats"]["cost"]), True, ROSSO_CHIARO)
            if list_info == PERSONAGGI:
                screen.blit(font_numeri.render("x.s.", True, ROSSO_CHIARO), ((rect_info.x + rect_info.width / 2 - nome.get_width() / 2) + 132 * MOD, rect_info.y + 10 * MOD) )
            screen.blit(cost, (rect_info.x + rect_info.width / 4 - cost.get_width(), rect_info.y + 10 * MOD))
            screen.blit(nome, (rect_info.x + rect_info.width / 2 - nome.get_width() / 2, rect_info.y + 10 * MOD))
            Drawtext(screen, WrapText(el["info"]["descrizione"], info_font, rect_info), rect_info.y + nome.get_height() * 3, rect_info.x + 10 * MOD, info_font, BIANCO, nome.get_height() / 2)
            if list_info == PERSONAGGI:
                Drawtext(screen, WrapText(el["info"]["abilita"], info_font, rect_info), rect_info.y + rect_info.height - nome.get_height() * 2.5, rect_info.x + 10 * MOD, info_font, BIANCO, nome.get_height() / 2)

def ViewInfoCibo(list_info, screen, rects_pulsanti, cibo_scelto):
    mouse_pos = pygame.mouse.get_pos()
    for pos, el in enumerate(list_info):
        if pos >= len(rects_pulsanti):
            break
        if rects_pulsanti[pos].collidepoint(mouse_pos):
            rect_info = pygame.Rect(rects_pulsanti[pos].x + 100 * MOD, rects_pulsanti[pos].y, WIDTH_INFO_CHARACHTER, HEIGHT_INFO_CHARACHETER)
            pygame.draw.rect(screen, (161, 88, 0), rect_info, 0, 10)
            pygame.draw.rect(screen, (0, 0, 0), rect_info, 3, 10)
            nome = title_font.render(el["info"]["name"].title(), True, BIANCO)
            cost = font_numeri.render(str(el["stats"]["cost"]), True, ROSSO_CHIARO)
            quantita_totale = sum(c["stats"]["saturazione"] for c in cibo_scelto if c["info"]["name"] == el["info"]["name"])
            quantita_text = title_font.render(f"Qta: {quantita_totale}", True, BIANCO)
            screen.blit(cost, (rect_info.x + rect_info.width / 4 - cost.get_width(), rect_info.y + 10 * MOD))
            screen.blit(nome, (rect_info.x + rect_info.width / 2 - nome.get_width() / 2, rect_info.y + 10 * MOD))
            screen.blit(quantita_text, (rect_info.x + rect_info.width / 2 - quantita_text.get_width() / 2, rect_info.y + 40 * MOD))
            Drawtext(screen, WrapText(el["info"]["descrizione"], info_font, rect_info), rect_info.y + nome.get_height() * 3, rect_info.x + 10 * MOD, info_font, BIANCO, nome.get_height() / 2)


def reset_posizione_personaggio(personaggio_corrente):
    personaggio_corrente["pos"]["scelta_equip"]["x"] = WIDTH // 10
    personaggio_corrente["pos"]["scelta_equip"]["y"] = (HEIGHT // 2) + (HEIGHT // 10)
    personaggio_corrente["pos"]["scelta_equip"]["x_fine"] = (WIDTH // 2) + (WIDTH // 10)
    personaggio_corrente["pos"]["scelta_equip"]["y_fine"] = (HEIGHT // 2) - (HEIGHT // 16)

def nuova_destinazione(p, i, barca_pos=BARCA_POS):
    p["pos"]["scelta_equip"]["x_fine"] = barca_pos[i][0]
    p["pos"]["scelta_equip"]["y_fine"] = barca_pos[i][1]

def SelectCharacheters(pos_pers, pers_sel, soldi, pers_move, click_mouse, lista_personaggi):
    if pos_pers < 0 or pos_pers >= len(lista_personaggi):
        return soldi
    costo = lista_personaggi[pos_pers]["stats"]["cost"]
    p = lista_personaggi[pos_pers]
    if click_mouse[0]:
        if soldi >= costo and len(pers_sel) < len(BARCA_POS):
            p_copy = {
                "stats": copy.deepcopy(p["stats"]),
                "pos": copy.deepcopy(p["pos"]),
                "sprites": p["sprites"],
                "info": p["info"]
            }
            pers_move.append(p_copy)
            pers_sel.append(p_copy)
    elif click_mouse[2]:
        cerca = False
        for trovato in pers_sel:
            if trovato["info"]["name"] == p["info"]["name"] and not cerca:
                pers_move.remove(trovato)
                pers_sel.remove(trovato)
                reset_posizione_personaggio(trovato)
                cerca = True
    return soldi

def SelectEquipment(pos_equip, equip_sel, soldi, mouse_click, lista_equip):
    costo = lista_equip[pos_equip]["stats"]["cost"]
    e = lista_equip[pos_equip]
    if mouse_click[0]:
        if soldi >= costo and e not in equip_sel:
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

pygame.init()
pygame.display.set_icon(pygame.image.load("assets/sfondi/icon.png"))

schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirates of the see")

pygame.mixer.music.load("./assets/music/menu_music.mp3")
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

bg = pygame.image.load("assets/sfondi/default1.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bottone_marrone = pygame.image.load("assets/tasti/arrow_left.png").convert_alpha()

BUTTON_RECT_PLAY = pygame.rect.Rect(10 * MOD, HEIGHT - HEIGHT_BUTTON, 180 * MOD, 90 * MOD)
BUTTON_PLAY = pygame.transform.scale(pygame.image.load("assets/tasti/play.png"), (BUTTON_RECT_PLAY.width, BUTTON_RECT_PLAY.height))
SCAFFALE_MONEY = pygame.transform.scale(pygame.image.load("assets/tasti/scaffale_money.png"), (int(240 * MOD), int(160 * MOD)))


categoria_attiva = "personaggi"
cibo_scelto = []
personaggi_selezionati = []
pers_in_movimento = []
equip_scelto = []
soldi_iniziali = 2000
arrivato = False
tempo_errore = 0

ordina_barca_pos(BARCA_POS)


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
            elif event.key == pygame.K_m:
                categoria_attiva = "equipaggiamento"
            elif event.key == pygame.K_b:
                categoria_attiva = "bibite"
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if BUTTON_RECT_PLAY.collidepoint(mouse):
                if len(personaggi_selezionati) != 0 and len(cibo_scelto) != 0 and len(equip_scelto) != 0:
                    p_sel = [p["info"]["name"] for p in personaggi_selezionati]
                    c_sel = [c["info"]["name"] for c in cibo_scelto]
                    e_sel = [e["info"]["name"] for e in equip_scelto]
                    SalvaEquipaggiamento(DATI_EQUIP, p_sel, c_sel, e_sel, soldi_iniziali)
                    subprocess.Popen([sys.executable, MAIN_GIOCO])
                    sys.exit()
                else:
                    tempo_errore = pygame.time.get_ticks()
            else:
                for pos, el in enumerate(BUTTON_RECTS):
                    if el.collidepoint(mouse):
                        if categoria_attiva == "personaggi":
                            soldi_iniziali = SelectCharacheters(pos, personaggi_selezionati, soldi_iniziali, pers_in_movimento, click, PERSONAGGI)
                        elif categoria_attiva == "cibo":
                            soldi_iniziali = SelectCibo(pos, cibo_scelto, soldi_iniziali, click, CIBO)
                        elif categoria_attiva == "equipaggiamento":
                            soldi_iniziali = SelectEquipment(pos, equip_scelto, soldi_iniziali, click, EQUIPAGGIAMENTO)
                        elif categoria_attiva == "bibite":
                            soldi_iniziali = SelectCibo(pos, cibo_scelto, soldi_iniziali, click, BIBITE)

    if categoria_attiva == "personaggi":
        lista_attiva = PERSONAGGI
    elif categoria_attiva == "cibo":
        lista_attiva = CIBO
    elif categoria_attiva == "equipaggiamento":
        lista_attiva = EQUIPAGGIAMENTO
    elif categoria_attiva == "bibite":
        lista_attiva = BIBITE
    else:
        lista_attiva = PERSONAGGI

    schermo.blit(bg, (0, 0))
    if len(pers_in_movimento) != 0:
        for i, p in enumerate(pers_in_movimento):
            arrivato, x, y = disegna_spostamento_personaggio(p, 5, 150, schermo)
            pers_in_movimento[i]["pos"]["scelta_equip"]["x"] = x
            pers_in_movimento[i]["pos"]["scelta_equip"]["y"] = y
            if arrivato:
                nuova_destinazione(p,i, BARCA_POS)

    DrawMoney(schermo, soldi_iniziali, (WIDTH - 203 * MOD, -47 * MOD), SCAFFALE_MONEY)
    DrawButtonEquip(lista_attiva, schermo, BUTTON_RECTS)
    Drawtext_PFE(schermo, ["P:PC", "C:Food", "M:Merce", "B:Bibite"], 15 * MOD, 210 * MOD, title_font, BIANCO, 20 * MOD, ROSA_SCURO, "P:PC" if categoria_attiva == "personaggi" else "C:Food" if categoria_attiva == "cibo" else "M:Merce" if categoria_attiva == "equipaggiamento" else "B:Bibite" if categoria_attiva == "bibite" else None)
    if categoria_attiva in ["cibo", "bibite"]:
        ViewInfoCibo(lista_attiva, schermo, BUTTON_RECTS, cibo_scelto)
    else:
        ViewInfoEquip(lista_attiva, schermo, BUTTON_RECTS)
    tempo_errore = draw_con_tempo(schermo, ["Seleziona almeno un", "- personaggio", "- cibo", "- equipaggiamento!"], title_font, BIANCO, 22 * MOD, tempo_errore, x=WIDTH - 200 * MOD, y=HEIGHT - 100 * MOD)
    schermo.blit(BUTTON_PLAY, BUTTON_RECT_PLAY)

    pygame.display.update()
    clock.tick(60)

pygame.quit()