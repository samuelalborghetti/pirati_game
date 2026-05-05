import pygame

pygame.init()

LARGHEZZA, ALTEZZA = 1280, 853
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))

sfondo = pygame.image.load("assets/sfondi/schermata_baratto.png")
sfondo = pygame.transform.scale(sfondo, (LARGHEZZA, ALTEZZA))

SCALA_X = LARGHEZZA / 1536
SCALA_Y = ALTEZZA / 1024

def r(x, y, w, h):
    #Crea una Rect scalata
    return pygame.Rect(int(x * SCALA_X), int(y * SCALA_Y), int(w * SCALA_X), int(h * SCALA_Y))

bottoni = [
    {"nome": "Sale",     "prezzo": 10,  "rect": r(1000, 170, 536, 170)},
    {"nome": "Stoffa",   "prezzo": 25,  "rect": r(1000, 340, 536, 170)},
    {"nome": "Coltelli", "prezzo": 50,  "rect": r(1000, 510, 536, 170)},
    {"nome": "Diamanti", "prezzo": 200, "rect": r(1000, 680, 536, 170)},
]

# UI
FONT_GRANDE = pygame.font.SysFont("Georgia", 32, bold=True)
FONT_MEDIO  = pygame.font.SysFont("Georgia", 24)

COL_BG     = (40, 20, 5)
COL_BORDO  = (180, 130, 60)
COL_TESTO  = (240, 210, 140)
COL_BTN    = (100, 60, 20)
COL_HOVER  = (150, 90, 30)

popup_nome = None
quantita = 1


def trova_bottone(nome):
    for b in bottoni:
        if b["nome"] == nome:
            return b
    return None


def rect_popup():
    pw, ph = 340, 220
    px = LARGHEZZA // 2 - pw // 2
    py = ALTEZZA // 2 - ph // 2
    return pygame.Rect(px, py, pw, ph)


def rect_popup_buttons(pop_rect):
    btn_meno = pygame.Rect(pop_rect.x + 40,  pop_rect.y + 145, 50, 40)
    btn_piu  = pygame.Rect(pop_rect.x + 250, pop_rect.y + 145, 50, 40)
    btn_ok   = pygame.Rect(pop_rect.x + 110, pop_rect.y + 155, 120, 40)
    return btn_meno, btn_piu, btn_ok


def draw_button(rect, text, font):
    mouse = pygame.mouse.get_pos()
    col = COL_HOVER if rect.collidepoint(mouse) else COL_BTN

    pygame.draw.rect(schermo, col, rect, border_radius=6)
    pygame.draw.rect(schermo, COL_BORDO, rect, 2, border_radius=6)

    t = font.render(text, True, COL_TESTO)
    schermo.blit(t, (rect.x + rect.w//2 - t.get_width()//2,
                     rect.y + rect.h//2 - t.get_height()//2))


def disegna_popup(bottone, qta):
    pop = rect_popup()
    pygame.draw.rect(schermo, COL_BG, pop, border_radius=12)
    pygame.draw.rect(schermo, COL_BORDO, pop, 3, border_radius=12)

    titolo = FONT_GRANDE.render(f"Scambia {bottone['nome']}", True, COL_TESTO)
    schermo.blit(titolo, (pop.centerx - titolo.get_width()//2, pop.y + 15))

    totale = bottone["prezzo"] * qta
    t1 = FONT_MEDIO.render(f"Prezzo unitario: {bottone['prezzo']} monete", True, COL_TESTO)
    t2 = FONT_MEDIO.render(f"Totale: {totale} monete", True, COL_TESTO)
    schermo.blit(t1, (pop.x + 20, pop.y + 70))
    schermo.blit(t2, (pop.x + 20, pop.y + 100))

    btn_meno, btn_piu, btn_ok = rect_popup_buttons(pop)
    draw_button(btn_meno, "-", FONT_GRANDE)
    draw_button(btn_piu,  "+", FONT_GRANDE)

    tq = FONT_GRANDE.render(str(qta), True, COL_TESTO)
    schermo.blit(tq, (pop.centerx - tq.get_width()//2, pop.y + 148))

    draw_button(btn_ok, "Conferma", FONT_MEDIO)

    return pop, btn_meno, btn_piu, btn_ok


def gestisci_evento(event, popup_nome, quantita):
    mouse = pygame.mouse.get_pos()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return None, 1

    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return popup_nome, quantita

    if popup_nome is None:
        for b in bottoni:
            if b["rect"].collidepoint(mouse):
                return b["nome"], 1
        return None, quantita

    bottone = trova_bottone(popup_nome)
    pop = rect_popup()
    btn_meno, btn_piu, btn_ok = rect_popup_buttons(pop)

    if btn_meno.collidepoint(mouse):
        quantita = max(1, quantita - 1)
        return popup_nome, quantita

    if btn_piu.collidepoint(mouse):
        return popup_nome, quantita + 1

    if btn_ok.collidepoint(mouse):
        print(f"Scambiato: {quantita}x {popup_nome} per {bottone['prezzo'] * quantita} monete")
        return None, 1

    if not pop.collidepoint(mouse):
        return None, 1

    return popup_nome, quantita


def disegna_schermata(popup_nome, quantita):
    schermo.blit(sfondo, (0, 0))
    if popup_nome:
        bottone = trova_bottone(popup_nome)
        disegna_popup(bottone, quantita)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        popup_nome, quantita = gestisci_evento(event, popup_nome, quantita)

    disegna_schermata(popup_nome, quantita)
    pygame.display.flip()

pygame.quit()