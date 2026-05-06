import pygame
import math

pygame.init()

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
    btn_ok_rect = pygame.Rect(LARGHEZZA//2 - 110, btn_ok_y, 220, 45)
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
        pass
    
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